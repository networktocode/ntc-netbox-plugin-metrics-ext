"""Test cases for nautobot_metrics_ext views."""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class AppMetricEndpointTests(TestCase):
    """Test cases for ensuring application metric endpoint is working properly."""

    def setUp(self):
        """Basic setup to create API client for test case."""
        self.app_metric_url = reverse("plugins-api:nautobot_metrics_ext-api:nautobot_metrics_ext_app_view")
        self.client = APIClient()

    def test_endpoint(self):
        """Ensure the endpoint is working properly and is not protected by authentication."""
        resp = self.client.get(self.app_metric_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
