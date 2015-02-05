import logging

from django.conf import settings
from dogapi import dog_stats_api
from dogapi.stats.reporters import Reporter


logger = logging.getLogger(__name__)


class NullReporter(Reporter):
    """
    A DogAPI to nowhere.
    """

    def flush(self, metrics):
        pass


def get_client():
    """ Return a started instance of the datadog client api.
    If a 'DATADOG_API_KEY' is not set or it's None, we will disable
    collection and flushing of metrics - useful for development.
    """
    api_key = getattr(settings, 'DATADOG_API_KEY', None)
    if api_key is None:
        logger.debug("DATADOG_API_KEY not set, disabling it")
        dog_stats_api.start(disabled=True)
        dog_stats_api.reporter = NullReporter()
    else:
        # if we have the DATADOG_API_KEY set, we use that
        dog_stats_api.start(api_key=api_key)

    return dog_stats_api
