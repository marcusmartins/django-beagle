"""Tests for the middlewares of the influxdb_metrics app."""
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User

from beagle.middleware import MetricsRequestMiddleware


class MetricsRequestMiddlewareTestCase(TestCase):
    """Tests for the ``MetricsRequestMiddleware`` middleware."""

    def setUp(self):
        super(MetricsRequestMiddlewareTestCase, self).setUp()
        self.staff = User.objects.create(username='staff', is_staff=True)
        self.superuser = User.objects.create(
            username='superuser', is_superuser=True)

    def tearDown(self):
        super(MetricsRequestMiddlewareTestCase, self).tearDown()

    def test_get(self):
        req = RequestFactory().get('/')
        req.user = AnonymousUser()
        mware = MetricsRequestMiddleware()
        mware.process_view(req, 'view_funx', 'view_args', 'view_kwargs')
        resp = mware.record_time(req)
        self.assertIsNotNone(resp)
        timing, tags = resp
        self.assertGreater(timing, 0.000)
        self.assertIn('is_authenticated:False', tags)
        self.assertIn('is_superuser:False', tags)
        self.assertIn('is_staff:False', tags)
        self.assertIn('is_ajax:False', tags)
        self.assertIn('path:/', tags)
        self.assertIn('method:GET', tags)

    def test_get_long_path(self):
        req = RequestFactory().get('/mysuper/long/path')
        req.user = AnonymousUser()
        mware = MetricsRequestMiddleware()
        mware.process_view(req, 'view_funx', 'view_args', 'view_kwargs')
        resp = mware.record_time(req)
        self.assertIsNotNone(resp)
        timing, tags = resp
        self.assertGreater(timing, 0.000)
        self.assertIn('path:/mysuper/long/path', tags)

    def test_post(self):
        req = RequestFactory().post('/')
        req.user = AnonymousUser()
        mware = MetricsRequestMiddleware()
        mware.process_view(req, 'view_funx', 'view_args', 'view_kwargs')
        resp = mware.record_time(req)
        self.assertIsNotNone(resp)
        timing, tags = resp
        self.assertGreater(timing, 0.000)
        self.assertIn('method:POST', tags)

    def test_as_staff(self):
        req = RequestFactory().get('/')
        req.user = self.staff
        mware = MetricsRequestMiddleware()
        mware.process_view(req, 'view_funx', 'view_args', 'view_kwargs')
        resp = mware.record_time(req)
        self.assertIsNotNone(resp)
        timing, tags = resp
        self.assertGreater(timing, 0.000)
        self.assertIn('is_authenticated:True', tags)
        self.assertIn('is_staff:True', tags)

    def test_without_user(self):
        req = RequestFactory().get('/')
        req.user = None
        mware = MetricsRequestMiddleware()
        mware.process_view(req, 'view_funx', 'view_args', 'view_kwargs')
        resp = mware.record_time(req)
        self.assertIsNotNone(resp)
        timing, tags = resp
        self.assertGreater(timing, 0.000)
        self.assertIn('is_authenticated:False', tags)
        self.assertIn('is_staff:False', tags)
        self.assertIn('is_superuser:False', tags)
