import logging
from typing import Dict, Any, Optional


def remove_none_from_dict(obj: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in obj.items() if v is not None}


def get_logger(
    level: int = logging.DEBUG,
    logger_name: Optional[str] = None,
    formatter: str = "[%(levelname)s] %(message)s",
    fp: Optional[str] = None,
) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    if fp:
        logger.addHandler(__create_file_handle(fp, level, formatter))
    logger.addHandler(__create_stream_handle(level, formatter))
    logger.setLevel(level)
    return logger


def __create_stream_handle(level: int, formatter: str):
    stream_handle = logging.StreamHandler()
    stream_handle.setLevel(level)
    stream_handle.setFormatter(logging.Formatter(formatter))
    return stream_handle


def __create_file_handle(path: str, level: int, formatter: str):
    file_handle = logging.FileHandler(path)
    file_handle.setLevel(level)
    file_handle.setFormatter(logging.Formatter(formatter))
    return file_handle
