"""
Collection for common help function in project.
"""
import asyncio
import contextvars
import logging
from datetime import datetime, timedelta
from functools import lru_cache, partial, wraps
from importlib import import_module
from typing import Callable, Coroutine, Type

from loguru import logger


def async_wrapper(func: Callable) -> Callable:  # is not used
    """
    Decorator for calling sync function in thread executor and mimic func to async.
    """

    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs) -> Coroutine:
        if loop is None:
            loop = asyncio.get_event_loop()
        p_func = partial(func, *args, **kwargs)
        func_context = contextvars.copy_context()
        p_func_with_context = partial(func_context.run, p_func)
        return await loop.run_in_executor(executor, p_func_with_context)

    return run


async def process(func, *args, **params):
    """
    Wrapper for calling sync and async func in same style.
    """
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **params)
    else:
        return func(*args, **params)


def async_lru_cache_decorator(func: Callable) -> Callable:  # is not used
    """
    Wrapper for caching the result of async func call.
    """

    @lru_cache()
    @wraps(func)
    def cached_async_function(*args, **kwargs):
        coroutine = func(*args, **kwargs)
        return asyncio.ensure_future(coroutine)

    return cached_async_function


def duration_measure(func: Callable) -> Callable:  # is not used
    """
    Decorator for logging execution time of the func.
    """
    fn_logger = getattr(import_module(func.__module__), 'logger', logger)

    @wraps(func)
    async def duration_measure_wrapper(*args, **kwargs):
        start_time = datetime.utcnow()
        fn_result = await process(func, *args, **kwargs)
        end_time = datetime.utcnow()
        fn_logger.info(
            'Completed %s. Elapsed time: %s', func.__name__, end_time - start_time
        )
        return fn_result

    return duration_measure_wrapper


def retry_by_exception(
    times: int = 3, exception: Type[BaseException] = BaseException
) -> Callable:  # noqa: CCR001
    """
    Retry executing func `times` times if `exception` occurs.
    """

    def retry_decorator(func: Callable):  # noqa: CCR001
        @wraps(func)
        async def wrapper(*args, **kwargs):
            repeats = times
            while True:
                try:
                    return await process(func, *args, **kwargs)
                except exception as err:
                    repeats = repeats - 1
                    if repeats <= 0:
                        raise
                    logger.warning(err)

        return wrapper

    return retry_decorator


async def cancel_all_tasks(timeout: int = 10):
    start_time = datetime.utcnow()
    # from aiomisc import cancel_tasks
    for task in asyncio.all_tasks():
        if task.done():
            continue
        if task is asyncio.current_task():
            continue
        if start_time + timedelta(seconds=timeout) > datetime.utcnow():
            logging.debug('Current timeout for stopping task %s is over: exiting')
            return
        task.cancel()

    logging.debug('Current tasks are already stopped')
