import os
from typing import Callable, List, Set


def list_files(path: str, eligible: Callable[[str], bool]) -> List[str]:
    result = []
    for dp, _, fns in os.walk(path):
        for fn in fns:
            fp = os.path.join(dp, fn)
            if eligible(fp):
                result.append(fp)
    return result


def list_files_with_extensions(path: str, extensions: Set[str]) -> List[str]:
    return list_files(path, lambda fp: fp.split(".")[-1] in extensions)
