"""Implementation of the Django management "rqworker_prom" command."""
from os import environ

from django_rq.management.commands.rqworker import Command as DjangoRqCommand
from prometheus_client import start_http_server, CollectorRegistry, multiprocess


class Command(DjangoRqCommand):
    """Inherit from the default DjangoRqCommand to start a prometheus endpoint with the worker."""

    def add_arguments(self, parser):
        """Add an additional argument to define the port number for prometheus."""
        parser.add_argument(
            "--prom-port",
            action="store",
            type=int,
            default=8001,
            dest="prom_port",
            help="Port for the prometheus endpoint",
        )
        super().add_arguments(parser)

    def handle(self, *args, **options):
        """Handler for the rqworker_metrics command."""

        if environ.get("prometheus_multiproc_dir") is None:
            exit(
                "The mandatory environ variable 'prometheus_multiproc_dir' is not defined, "
                "please configure it or use the default 'rqworker' command instead."
            )

        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        prom_port = options.get("prom_port")
        start_http_server(prom_port, registry=registry)
        super().handle(*args, **options)
