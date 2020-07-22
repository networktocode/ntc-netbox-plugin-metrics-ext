"""Plugin declaration for netbox_app_metrics."""

__version__ = "0.1.0"

from extras.plugins import PluginConfig

# Registry of functions that can generate additional application metrics
# All functions in the registry should take no argument and return an Iterator (or list) of prometheus Metric Object
# The Registry can be populated from the configuration file or using register_metric_func()
__REGISTRY__ = []


def register_metric_func(func):
    """Register additional function to generate application metrics

    Args:
        func: python function, taking no argument that return a list of Prometheus Metric Object
    """
    if not callable(func):
        raise TypeError(
            f"Trying to register a {type(func)} into the application metric registry, only function (callable) are supporter"
        )

    __REGISTRY__.append(func)


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
    default_settings = {
        "models": {"dcim": {"Site": True, "Rack": True, "Device": True,}, "ipam": {"IPAddress": True, "Prefix": True}},
        "reports": True,
        "queues": True,
    }
    caching_config = {}


config = AppMetricsConfig  # pylint:disable=invalid-name
