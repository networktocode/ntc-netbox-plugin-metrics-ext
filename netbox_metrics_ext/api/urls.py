"""Django URL patterns for netbox_metrics_ext plugin."""

from django.urls import path
from . import views

urlpatterns = [
    path("app-metrics", views.ExportToDjangoView, name="netbox_metrics_ext_app_view"),
]
