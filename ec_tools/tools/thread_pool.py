import logging
import time
from concurrent.futures import ThreadPoolExecutor, Future
from typing import List, Callable, Any, Optional


class CustomThreadPoolExecutor(ThreadPoolExecutor):
    futures: List[Future]

    def __init__(
        self,
        max_workers=None,
        thread_name_prefix="",
        initializer=None,
        initargs=(),
    ):
        self.futures = []
        super().__init__(max_workers, thread_name_prefix, initializer, initargs)

    def submit(self, fn, ignore_exception: bool = False, **kwargs):
        future = super().submit(
            self.try_execute, func=fn, ignore_exception=ignore_exception, **kwargs
        )
        self.futures.append(future)
        return future

    @classmethod
    def try_execute(
        cls, func: Callable, ignore_exception: bool, **kwargs
    ) -> Optional[Any]:
        try:
            return func(**kwargs)
        except Exception as e:
            if not ignore_exception:
                raise e
            logging.error(f"[ThreadPool] try to run failed with %s", e)
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

    def __del__(self):
        logging.info("[ThreadPool] stopping")
        self.join()
        logging.info("[ThreadPool] stopped")
