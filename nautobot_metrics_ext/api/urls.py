"""Django URL patterns for nautobot_metrics_ext plugin."""

from django.urls import path
from . import views

urlpatterns = [
    path("app-metrics", views.ExportToDjangoView, name="nautobot_metrics_ext_app_view"),
]
