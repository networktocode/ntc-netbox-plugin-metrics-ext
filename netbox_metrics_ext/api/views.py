"""Django views for Prometheus metric collection and reporting."""
import time
import logging
from collections.abc import Iterable

from pydoc import locate
import prometheus_client

from django.conf import settings
from django.http import HttpResponse

from prometheus_client.core import CollectorRegistry

from netbox_metrics_ext import __REGISTRY__
from netbox_metrics_ext.metrics import collect_extras_metric, metric_reports, metric_models

logger = logging.getLogger(__name__)
PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["netbox_metrics_ext"]


class CustomCollector:
    """Collector class for collecting plugin and extras metrics."""

    def collect(self):  # pylint: disable=no-self-use
        """Collect metrics for all plugins and extras."""
        start = time.time()
        if "queues" in PLUGIN_SETTINGS and PLUGIN_SETTINGS["queues"]:
            for metric in metric_rq():
                yield metric

        if "reports" in PLUGIN_SETTINGS and PLUGIN_SETTINGS["reports"]:
            for metric in metric_reports():
                yield metric

        if "models" in PLUGIN_SETTINGS:
            for metric in metric_models(PLUGIN_SETTINGS["models"]):
                yield metric

        # --------------------------------------------------------------
        # Extras Function defined in configuration.py or the Regristry
        # # --------------------------------------------------------------
        if "extras" in PLUGIN_SETTINGS:
            for metric in collect_extras_metric(PLUGIN_SETTINGS["extras"]):
                yield metric

        for metric in collect_extras_metric(__REGISTRY__):
            yield metric

        gauge = GaugeMetricFamily("netbox_app_metrics_processing_ms", "Time in ms to generate the app metrics endpoint")
        duration = time.time() - start
        gauge.add_metric([], format(duration * 1000, ".5f"))
        yield gauge


registry = CollectorRegistry()
collector = CustomCollector()
registry.register(collector)


def ExportToDjangoView(request):  # pylint: disable=invalid-name
    """Exports /api/plugins/metrics-ext/app-metrics as a Django view."""
    metrics_page = prometheus_client.generate_latest(registry)
    return HttpResponse(metrics_page, content_type=prometheus_client.CONTENT_TYPE_LATEST)
