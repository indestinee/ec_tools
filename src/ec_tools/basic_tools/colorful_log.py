import logging
import os

from ec_tools.basic_tools.colorful_str import colorful_str
from ec_tools import basic_tools

DEFAULT_LOG_FORMAT = '[(#y)%(levelname)s(#) (#b)%(filename)s/%(module)s/%(funcName)s/#L%(lineno)d(#)' \
                     ' (#g)%(asctime)s(#)]: %(message)s'


def create_stream_handle(level, formatter: str):
    stream_handle = logging.StreamHandler()
    stream_handle.setLevel(level)
    stream_handle.setFormatter(
        logging.Formatter(colorful_str(formatter)))
    return stream_handle


def create_file_handle(path: str, level: int, formatter: str):
    file_handle = logging.FileHandler(path)
    file_handle.setLevel(level)
    file_handle.setFormatter(
        logging.Formatter(colorful_str.clean(formatter)))
    return file_handle


class ColorfulLog(logging.Logger):
    def __init__(
            self,
            log_level=logging.INFO,
            log_formatter=DEFAULT_LOG_FORMAT,
            log_dir='logs',
            log_name='colorful_log',
    ):
        super().__init__(log_name, log_level)

        if log_dir is None:
            self.log_path = None
        else:
            self.log_path = os.path.join(
                log_dir, basic_tools.touch_suffix(log_name, '.log'))
            basic_tools.mkdir(self.log_path)
            self.addHandler(
                create_file_handle(path=self.log_path,
                                   level=log_level,
                                   formatter=log_formatter))
        self.addHandler(
            create_stream_handle(level=log_level, formatter=log_formatter))


logger = ColorfulLog(log_dir=None, log_name='ec_tools')
