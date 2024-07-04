import asyncio
from contextlib import contextmanager
import functools
import signal
import sys
import time
from typing import Callable

from threading import Thread

from colorama import Fore, Style


def async_command(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorator(*args, **kwargs) -> None:
        asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
    return decorator


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


class SpinningThread(Thread):

    def __init__(self):
        super().__init__()
        self.stop = False

    def run(self):
        spinner = spinning_cursor()

        while not self.stop:
            sys.stdout.write(Fore.RED + Style.BRIGHT + next(spinner) + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')


@contextmanager
def spinning_ctx():
    t = SpinningThread()
    t.start()

    def signal_handler(sig, frame):
        t.stop = True
        t.join()
        sys.stdout.write('\b\b')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        yield
    finally:
        if not t.stop:
            t.stop = True
            t.join()
