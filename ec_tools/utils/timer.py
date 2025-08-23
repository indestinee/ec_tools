import logging
import time

from colorama import Fore, Style


class Timer:
    msg: str
    start_time: float
    muted: bool

    def __init__(self, msg: str):
        self.msg = msg
        self.muted = False
        self.start_time = time.time()
        logging.info(f"{Fore.CYAN}{msg}{Style.RESET_ALL}")
        logging.info("=" * 32)

    def __enter__(self):
        return self

    def mute(self):
        self.muted = True

    def __exit__(self, *args):
        if self.muted:
            return
        elapsed = time.time() - self.start_time
        logging.info("=" * 32)
        if elapsed < 1:
            logging.info(f"{Fore.CYAN}$ # finished in {elapsed * 1000:.2f}ms{Style.RESET_ALL}")
        elif elapsed < 60:
            logging.info(f"{Fore.CYAN}$ # finished in {elapsed:.3f}s{Style.RESET_ALL}")
        else:
            logging.info(f"{Fore.CYAN}$ # finished in {elapsed / 60}m {elapsed % 60}s{Style.RESET_ALL}")
        logging.info("\n")
