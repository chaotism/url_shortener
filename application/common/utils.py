"""
Collection for common help function in project.
"""
import asyncio
import contextvars
import time
from functools import partial, wraps
from itertools import count
from typing import Callable, Coroutine, List

from aiomisc import asyncretry, cancel_tasks
from loguru import logger

from common.constants import INFINITY


def async_wrapper(func: Callable) -> Callable:
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


def duration_measure(func: Callable) -> Callable:
    """
    Decorator for logging execution time of the func.
    """
    start_time_var: contextvars.ContextVar[float] = contextvars.ContextVar('start_time')

    def on_done(fut):
        start_time = start_time_var.get('start_time')
        end_time = time.time()
        logger.info(
            f'Completed {func.__name__}. Elapsed time: {end_time - start_time} seconds'
        )

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        if not asyncio.iscoroutinefunction(func):
            end_time = time.time()
            logger.info(
                f'Completed {func.__name__}. Elapsed time: {end_time - start_time} seconds'
            )
            return result
        start_time_var.set(start_time)
        fut = asyncio.ensure_future(result)
        fut.add_done_callback(on_done)
        return fut

    return wrapper


def retry_by_exception(max_tries=3, exceptions=(Exception,), **kwargs):
    """
    Retry executing func if `exception` occurs.
    """
    if max_tries == INFINITY:
        max_tries = None
    if not isinstance(exceptions, (tuple, list)):
        exceptions = (exceptions,)

    def retry_decorator(func: Callable):
        @asyncretry(max_tries=max_tries, exceptions=exceptions, **kwargs)
        async def log_exception(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as ex:
                logger.error(
                    f'Function {func.__name__} raised exception {ex.__class__.__name__}({ex}). Restarting'
                )
                raise

        return log_exception

    return retry_decorator


async def gather_tasks(
    tasks: List[Coroutine], timeout=10
) -> List:  # TODO: use in background task
    """
    Work around for running tasks in parallel and logging errors.
    """
    success_results = []
    finished_tasks, pending_tasks = await asyncio.wait(tasks, timeout=timeout)
    if pending_tasks:
        raise TimeoutError(pending_tasks)
    for idx, task in enumerate(finished_tasks):
        if task.exception():
            logger.error(
                f'Task {tasks[idx]} raised exception {task.exception()} during execution'
            )
            continue
        success_results.append(task.result())
    return success_results


def cancel_all_tasks_wrapper(
    func: Callable,
) -> Callable:  # TODO: use in background task
    """
    Decorator for stopping all running task before start func.
    """

    @wraps(func)
    async def run(*args, **kwargs):
        await cancel_tasks(
            [t for t in asyncio.all_tasks() if not (t.done() or asyncio.current_task())]
        )
        logger.debug('Current tasks already stopped')
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        return func(*args, **kwargs)

    return run


def message_number_gen() -> Callable:  # TODO: use in background task
    """
    Returns increment int generator.
    """
    cnt = count()

    def get_next_number() -> int:
        return next(cnt)

    return get_next_number
