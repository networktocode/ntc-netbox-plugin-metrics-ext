"""Metrics libraries for the nautobot_metrics_ext plugin."""
import logging
import importlib
from collections.abc import Iterable
from packaging import version
from django.conf import settings

from prometheus_client.core import Metric, GaugeMetricFamily

from django_rq.utils import get_statistics


logger = logging.getLogger(__name__)

nautobot_version = version.parse(settings.VERSION)


def metric_rq():
    """Return stats about RQ Worker in Prometheus Metric format.

    Return:
        Iterator[GaugeMetricFamily]
            nautobot_queue_number_jobs: Nbr Job per RQ queue and status
            nautobot_queue_number_workers: Nbr worker per queue
    """
    queue_stats = get_statistics()

    job = GaugeMetricFamily(
        "nautobot_queue_number_jobs", "Number of Job per RQ queue and status", labels=["name", "status"]
    )
    worker = GaugeMetricFamily("nautobot_queue_number_workers", "Number of worker per queue", labels=["name"])

    if "queues" in queue_stats:
        for queue in queue_stats["queues"]:
            for status in ["finished", "started", "deferred", "failed", "scheduled"]:
                if f"{status}_jobs" not in queue.keys():
                    continue
                job.add_metric([queue["name"], status], queue[f"{status}_jobs"])

            if "workers" in queue.keys():
                worker.add_metric([queue["name"]], queue["workers"])

    yield job
    yield worker


def metric_reports():
    """Return CustomJobs results in Prometheus Metric format.

    Return:
        Iterator[GaugeMetricFamily]
            nautobot_customjob_stats: with custom job module, name and status as labels
    """
    from django.contrib.contenttypes.models import ContentType  # pylint: disable=import-outside-toplevel
    from extras.models import CustomJob, JobResult  # pylint: disable=import-outside-toplevel,no-name-in-module

    report_results = JobResult.objects.filter(obj_type=ContentType.objects.get_for_model(CustomJob))

    gauge = GaugeMetricFamily("nautobot_customjob_stats", "Per Custom Job statistics", labels=["module", "name", "status"])
    for result in report_results:
        if not result.data:
            continue

        for report_name, stats in result.data.items():
            for status in ["success", "warning", "failure", "info"]:
                gauge.add_metric([result.name, report_name, status], stats[status])
    yield gauge


def metric_models(params):
    """Return Models count in Prometheus Metric format.

    Args:
        params (dict): list of models to return organized per application

    Return:
        Iterator[GaugeMetricFamily]
            nautobot_model_count: with model name and application name as labels
    """
    gauge = GaugeMetricFamily("nautobot_model_count", "Per Nautobot Model count", labels=["app", "name"])
    for app, _ in params.items():
        for model, _ in params[app].items():
            try:
                models = importlib.import_module(f"{app}.models")
                model_class = getattr(models, model)
                gauge.add_metric([app, model], model_class.objects.count())
            except ModuleNotFoundError:
                logger.warning("Unable to find the python library %s.models", app)
            except AttributeError:
                logger.warning("Unable to load the module %s from the python library %s.models", model, app)

    yield gauge


def collect_extras_metric(funcs):
    """Collect Third party functions to generate additional Metrics.

    Args:
        funcs (list): list of functions to execute

    Return:
        List[GaugeMetricFamily]
            nautobot_model_count: with model name and application name as labels
    """
    for func in funcs:
        if not callable(func):
            logger.warning("Extra metric is not a function, skipping ... ")
            continue

        results = func()

        if not isinstance(results, Iterable):
            logger.warning("Extra metric didn't return a list, skipping ... ")
            continue

        for metric in results:
            if not Metric in type(metric).__bases__:
                logger.warning("Extra metric didn't return a Metric object, skipping ... ")
                continue
            yield metric
