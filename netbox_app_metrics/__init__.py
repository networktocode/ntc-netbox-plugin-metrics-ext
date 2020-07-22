"""Plugin declaration for netbox_app_metrics."""

__version__ = "0.1.0"

from extras.plugins import PluginConfig


class AppMetricsConfig(PluginConfig):
    """Plugin configuration for the netbox_app_metrics plugin."""

    name = "netbox_app_metrics"
    verbose_name = "Application Metrics Plugin"
    version = __version__
    author = "Network to Code, LLC"
    description = "Plugin to expose application level metrics using open telemetry format/prometheus."
    base_url = "app-metrics"
    required_settings = []
    min_version = "2.8.1"
    default_settings = {}
    caching_config = {}


config = AppMetricsConfig  # pylint:disable=invalid-name
