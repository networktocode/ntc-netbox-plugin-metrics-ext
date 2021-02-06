"""Test cases for nautobot_metrics_ext app metric function registry."""
from django.test import TestCase
from nautobot_metrics_ext import register_metric_func, __REGISTRY__


class RegistryTests(TestCase):
    """Test cases for ensuring the registry is working properly."""

    def test_register_metric_func(self):
        """Ensure the function to add functions to the registry is working properly."""

        def myfunction():
            """Dummy metric function."""

        self.assertRaises(TypeError, register_metric_func, "test")
        self.assertRaises(TypeError, register_metric_func, dict(test="test"))
        self.assertRaises(TypeError, register_metric_func, [1, 2, 3])

        register_metric_func(myfunction)
        self.assertEqual(__REGISTRY__[-1], myfunction)
