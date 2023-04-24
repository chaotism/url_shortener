"""
Common caching functionality.

https://memoize.readthedocs.io/en/latest/
"""
from datetime import timedelta
from memoize.configuration import DefaultInMemoryCacheConfiguration
from memoize.invalidation import InvalidationSupport
from memoize.wrapper import memoize


CALL_TIMEOUT = 1  # min
REFRESH_INTERVAL = 30  # min
IGNORE_UNREFRESHED_AFTER = REFRESH_INTERVAL * 2  # min


invalidation = InvalidationSupport()


def async_cache(func):  # TODO: think about using
    """
    Cache coroutine function results.
    """
    return memoize(
        configuration=DefaultInMemoryCacheConfiguration(
            method_timeout=timedelta(minutes=CALL_TIMEOUT),
            update_after=timedelta(minutes=REFRESH_INTERVAL),
            expire_after=timedelta(minutes=IGNORE_UNREFRESHED_AFTER),
        ),
        invalidation=invalidation,
    )(func)
