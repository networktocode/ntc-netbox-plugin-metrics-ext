from django.test import TestCase
from netbox_app_metrics import register_metric_func, __REGISTRY__


class registryTests(TestCase):
    """
    Test cases for ensuring the registry is working properly
    """

    def test_register_metric_func(self):
        """
        Ensures the function to add function to the registry is working properly
        """

        def myfunction():
            pass

        self.assertRaises(TypeError, register_metric_func, "test")
        self.assertRaises(TypeError, register_metric_func, dict(test="test"))
        self.assertRaises(TypeError, register_metric_func, [1, 2, 3])

        register_metric_func(myfunction)
        self.assertEqual(__REGISTRY__[-1], myfunction)
