"""Tests for the middlewares of the influxdb_metrics app."""
from django.test import TestCase

from beagle.client import get_client, NullReporter


class ClientTestCase(TestCase):
    """Tests for the ``client`` model."""

    def test_get_without_api_key(self):
        with self.settings(DATADOG_API_KEY=None):
            client = get_client()
            self.assertIsInstance(client.reporter, NullReporter)
            self.assertTrue(client._disabled)

    def test_get_with_api_key(self):
        with self.settings(DATADOG_API_KEY='fdsjkfdshfds'):
            client = get_client()
            self.assertNotIsInstance(client.reporter, NullReporter)
            self.assertFalse(client._disabled)
