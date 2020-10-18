import os

from ec_tools.basic_tools.colorful_log import ColorfulLog
from ec_tools.basic_tools.replace_dict import ReplaceDict


def touch_suffix(target: str, suffix: str) -> str:
    return target if target.endswith(suffix) else (target + suffix)


def mkdir(path: str, dirname_check=True):
    dir_path = os.path.dirname(path) if dirname_check else path
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
