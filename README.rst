Django Datadog Metrics
=======================

A app to send metrics to the datadog service.

Inspired by https://github.com/bitmazk/django-influxdb-metrics

Installation

To get the latest commit from GitHub

pip install -e git+git://github.com/marcusmartins/django-datadog-metrics.git#egg=influxdb_metrics

Settings

You need to set the following settings:

DATADOG_API_KEY = 'myapikey'
DATADOG_APP_NAME = 'myapp'

Add datadog_metrics to your INSTALLED_APPS

INSTALLED_APPS = (
    ...,
    'datadog_metrics',
)

Add datadog_metrics middleware to time your views:

MIDDLEWARE_CLASSES = (
    'datadog_metrics.middleware.MetricsRequestMiddleware',
) + MIDDLEWARE_CLASSES

Add a default set of tags that you would like to be set on every request.

DATADOG_METRICS_DEFAULT_TAGS = {
    'environment': 'staging',
    'version': '1.0.2'
}
