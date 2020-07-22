from django.urls import path
from . import views

urlpatterns = [
    path("", views.ExportToDjangoView, name="netbox_app_metrics_view"),
]
