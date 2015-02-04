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
    """ Return an instance of the datadog client api.
    If a 'DATADOG_API_KEY' is not set, it will use the
    NullReporter and discard any data. It's useful for development.
    """
    try:
        dog_stats_api.start(api_key=settings.DATADOG_API_KEY)
    except AttributeError:
        logger.debug("DATADOG_API_KEY not available, using NullReporter")
        dog_stats_api.start()
        dog_stats_api.reporter = NullReporter()

    return dog_stats_api
