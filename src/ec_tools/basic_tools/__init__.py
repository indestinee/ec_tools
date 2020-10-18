import os
import time


def touch_prefix(target: str, prefix: str) -> str:
    return target if target.startswith(prefix) else (prefix + target)


def touch_suffix(target: str, suffix: str) -> str:
    return target if target.endswith(suffix) else (target + suffix)


def mkdir(path: str, dirname_check=True):
    dir_path = os.path.dirname(path) if dirname_check else path
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)


def get_cur_time(time_format='%Y-%m-%d %H:%M:%S'):
    return time.strftime(time_format, time.localtime())
