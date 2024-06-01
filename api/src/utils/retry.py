import time
import logging

from functools import wraps

logger = logging.getLogger(__name__)


def retry(max_retries, timeout=5, retry_exc_class=Exception, raise_exc_class=Exception):
    def retry_decorator(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            exc = retry_exc_class("root")

            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except retry_exc_class as ex:
                    logger.warning(f"{func.__name__} | {ex}")
                    exc = ex
                    logger.warning(
                        f"Wait {timeout} seconds. {max_retries-1-i} retries left"
                    )
                    time.sleep(timeout)

            raise raise_exc_class(
                f"Cannot run func {func.__name__} after {max_retries} tries"
            ) from exc

        return _wrapper

    return retry_decorator
