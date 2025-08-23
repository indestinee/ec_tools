import logging
import time
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, List, Optional


class CustomThreadPoolExecutor(ThreadPoolExecutor):
    futures: List[Future]

    def __init__(
        self,
        max_workers=None,
        thread_name_prefix="",
        initializer=None,
        ignore_exception: bool = False,
        initargs=(),
    ):
        self.futures = []
        self.ignore_exception = ignore_exception
        super().__init__(max_workers, thread_name_prefix, initializer, initargs)

    def submit(self, fn, /, *args, **kwargs):
        future = super().submit(self.try_execute, func=fn, *args, **kwargs)
        self.futures.append(future)
        return future

    def try_execute(self, func: Callable, *args, **kwargs) -> Optional[Any]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if not self.ignore_exception:
                raise e
            logging.error("[ThreadPool] try to run failed with %s", e)
            return None

    def join(self, log_time: int = 5, clear_after_wait: bool = True) -> List[Any]:
        initial_time = time.time()
        initial_task_left = self._work_queue.qsize()
        while True:
            tasks_left = self._work_queue.qsize()
            time_cost = time.time() - initial_time
            eta = time_cost / max(1, initial_task_left - tasks_left) * tasks_left
            if tasks_left > 0:
                logging.info(
                    "[ThreadPool] waiting for %s tasks to complete, time cost: %.2f, eta: %.2f",
                    tasks_left,
                    time_cost,
                    eta,
                )
                time.sleep(log_time)
            else:
                break
        results = [future.result() for future in self.futures]
        if clear_after_wait:
            self.futures.clear()
        logging.info("[ThreadPool] all futures complete")
        return results
