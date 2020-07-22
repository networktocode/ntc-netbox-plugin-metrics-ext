from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class AppMetricEndpointTests(TestCase):
    """
    Test cases for ensuring application metric endpoint is working properly
    """

    def setUp(self):
        """
        Basis setup to create API client for test case
        """

        self.app_metric_url = reverse("plugins-api:netbox_app_metrics-api:netbox_app_metrics_view")
        self.client = APIClient()

    def test_endpoint(self):
        """
        Ensures the endpoint is working properly and is not protected by authentication
        """
        r = self.client.get(self.app_metric_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
