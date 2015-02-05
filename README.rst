Django Beagle
=======================

A reusable Django app to send metrics to the datadog service.

Inspired by https://github.com/bitmazk/django-influxdb-metrics

The app is currently tied to the datadog python api (https://github.com/DataDog/dogapi). That might change in the future to expose a more generic interface to other services like InfluxDB.

Installation
------------

To get the latest commit from GitHub

.. code-block:: bash
    pip install -e git+git://github.com/marcusmartins/django-datadog-metrics.git#egg=influxdb_metrics

Settings
--------

You need to set the following settings::

    DATADOG_API_KEY = 'myapikey'
    DATADOG_APP_NAME = 'myapp'

Add beagle to your INSTALLED_APPS::

    INSTALLED_APPS = (
        ...,
        'beagle',
    )

Add beagle middleware as close to the top of your MIDDLEWARE_CLASSES to time your views as possible::

    MIDDLEWARE_CLASSES = (
        'beagle.middleware.MetricsRequestMiddleware',
        ...
    )

Add a dictionary of tags that you would like to be set on every request. It's useful to set environment wide values like the version of the project.::

    BEAGLE_DEFAULT_TAGS = {
        'environment': 'staging',
        'version': '1.0.2'
    }

If the dictionary is not set, no global tags will be sent with the request.
