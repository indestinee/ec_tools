import datetime
import time

import ec_tools
from ec_tools.basic_tools.colorful_log import ec_tools_local_logger


class Procedure:
    def __init__(self, msg: str, logger=ec_tools_local_logger):
        self.logger = logger
        self.logs = [msg]
        self.time = time.time()

    def __enter__(self):
        self.logger.info(*self.logs)
        return self

    def add_log(self, *args):
        self.logs += args

    def __exit__(self, type, value, traceback):
        log = self.logger.info if traceback is None else self.logger.error
        log(ec_tools.colorful_str(
            *self.logs,
            ec_tools.colorful_str.done,
            'cost time: (#b){}'.format(
                datetime.timedelta(seconds=time.time() - self.time))))
