"""Middlewares for the beagle app."""
import inspect
import time

from django.conf import settings
from dogapi import dog_stats_api

# init datadog api
dog_stats_api.start(api_key=settings.DATADOG_API_KEY)


DEFAULT_TAGS_DICT = getattr(settings, 'BEAGLE_DEFAULT_TAGS', {})


class MetricsRequestMiddleware(object):
    """
    Measures request time and sends metric to Datadog.

    Credits go to: https://github.com/bitmazk/django-influxdb-metrics/blob/master/influxdb_metrics/middleware.py  # NOQA
    """
    def __init__(self):
        app_name = settings.DATADOG_APP_NAME
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
        self._record_time(request)
        return response

    def _record_time(self, request):
        if hasattr(request, '_start_time'):
            request_time = time.time() - request._start_time
            is_ajax = request.is_ajax()
            is_authenticated = False
            is_staff = False
            is_superuser = False
            if request.user.is_authenticated():
                is_authenticated = True
                if request.user.is_staff:
                    is_staff = True
                if request.user.is_superuser:
                    is_superuser = True

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
                'full_path': request.get_full_path,
                'path': request.path})

            tags = ['{}:{}'.format(key, val) for key, val in tags_dict.iteritems()]

            dog_stats_api.histogram(self.timing_metric, request_time, tags=tags)
