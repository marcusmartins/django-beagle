"""Middlewares for the beagle app."""
import inspect
import time

from django.conf import settings

from .client import get_client


DEFAULT_TAGS_DICT = getattr(settings, 'BEAGLE_DEFAULT_TAGS', {})


class MetricsRequestMiddleware(object):
    """
    Measures request time and sends metric to Datadog.

    Credits go to: https://github.com/bitmazk/django-influxdb-metrics/blob/master/influxdb_metrics/middleware.py  # NOQA
    """
    api_client = get_client()

    def __init__(self):
        app_name = getattr(settings, 'DATADOG_APP_NAME', 'beagle')
        self.timing_metric = '{0}.django.request'.format(app_name)

    def process_view(self, request, view_func, view_args, view_kwargs):
        view = view_func
        if not inspect.isfunction(view_func):
            view = view.__class__
        try:
            request._view_module = view.__module__
            request._view_name = view.__name__
            request._start_time = time.time()
        except AttributeError:  # pragma: no cover
            pass

    def process_response(self, request, response):
        try:
            timing, tags = self.record_time(request)
        except TypeError:
            # if we don't get a timing, don't send any timing
            pass
        else:
            # datadog swallow any exception
            # http://pydoc.datadoghq.com/en/latest/#doghttpapi
            self.api_client.histogram(self.timing_metric, timing, tags=tags)
        return response

    def record_time(self, request):
        if hasattr(request, '_start_time'):
            request_time = time.time() - request._start_time
            is_ajax = request.is_ajax()
            is_authenticated = False
            is_staff = False
            is_superuser = False

            if request.user is not None:
                is_authenticated = request.user.is_authenticated()
                is_staff = request.user.is_staff
                is_superuser = request.user.is_superuser

            # create new tags dictionary that merge the default
            # and the request specific tags.
            tags_dict = {}
            tags_dict.update(DEFAULT_TAGS_DICT)
            tags_dict.update({
                'is_ajax': is_ajax,
                'is_authenticated': is_authenticated,
                'is_staff': is_staff,
                'is_superuser': is_superuser,
                'method': request.method,
                'module': request._view_module,
                'view': request._view_name,
                'path': request.path})

            tags = ['{}:{}'.format(k, v) for k, v in tags_dict.iteritems()]
            return request_time, tags
