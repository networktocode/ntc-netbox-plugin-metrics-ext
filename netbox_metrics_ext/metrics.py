from prometheus_client.core import Metric, GaugeMetricFamily

from django_rq.utils import get_statistics
from extras.models import ReportResult


def metric_rq():
    """Return stats about RQ Worker in Prometheus Metric format.

    Return:
        Iterator[GaugeMetricFamily]
            netbox_queue_number_jobs: Nbr Job per RQ queue and status
            netbox_queue_number_workers: Nbr worker per queue
    """
    queue_stats = get_statistics()

    job = GaugeMetricFamily(
        "netbox_queue_number_jobs", "Number of Job per RQ queue and status", labels=["name", "status"]
    )
    worker = GaugeMetricFamily("netbox_queue_number_workers", "Number of worker per queue", labels=["name"])

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
    """Return Reports results in Prometheus Metric format.

    Return:
        Iterator[GaugeMetricFamily]
            netbox_report_stats: with report name and status as labels
    """
    report_results = ReportResult.objects.all()
    gauge = GaugeMetricFamily("netbox_report_stats", "Per report statistics", labels=["name", "status"])
    for result in report_results:
        for report_name, stats in result.data.items():
            for status in ["success", "warning", "failure", "info"]:
                gauge.add_metric([report_name, status], stats[status])
    yield gauge


def metric_models(params):
    """Return Models count in Prometheus Metric format.

    Args:
        params (dict): list of models to return organized per application

    Return:
        Iterator[GaugeMetricFamily]
            netbox_model_count: with model name and application name as labels
    """
    gauge = GaugeMetricFamily("netbox_model_count", "Per NetBox Model count", labels=["app", "name"])
    for app, _ in params.items():
        for model, _ in params[app].items():
            model_class = locate(f"{app}.models.{model}")
            gauge.add_metric([app, model], model_class.objects.count())
    yield gauge


def collect_extras_metric(funcs):
    """Collect Third party functions to generate additional Metrics.

    Args:
        funcs (list): list of functions to execute

    Return:
        List[GaugeMetricFamily]
            netbox_model_count: with model name and application name as labels
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
