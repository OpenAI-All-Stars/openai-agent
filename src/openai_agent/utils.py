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
        asyncio.run(f(*args, **kwargs))
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


async def read_stream(reader, buffer: list[str]):
    while True:
        line = await reader.readline()
        if not line:
            break
        buffer.append(line.decode())


class Process:
    def __init__(self) -> None:
        self.proc: asyncio.subprocess.Process | None = None
        self.stdout_buffer: list[str] = []
        self.stderr_buffer: list[str] = []

    @property
    def was_run(self) -> bool:
        return self.proc is not None

    async def shell(self, line: str):
        self.proc = await asyncio.create_subprocess_shell(
            line,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE,
        )
        asyncio.create_task(read_stream(self.proc.stdout, self.stdout_buffer))
        asyncio.create_task(read_stream(self.proc.stderr, self.stderr_buffer))

    async def user_input(self, line: str | None):
        if line is None:
            return
        assert self.proc is not None
        assert self.proc.stdin is not None
        self.proc.stdin.write(line.encode() + b'\n')
        await self.proc.stdin.drain()

    def clear_buffer(self):
        self.stdout_buffer.clear()
        self.stderr_buffer.clear()

    async def wait(self, seconds: float = 1) -> tuple[str, str]:
        assert self.proc is not None
        start_time = time.time()
        while self.proc.returncode is None and time.time() - start_time < seconds:
            await asyncio.sleep(0.1)

        if self.proc.returncode is not None:
            self.proc = None

        stdout = '\n'.join(self.stdout_buffer)
        stderr = '\n'.join(self.stderr_buffer)
        self.clear_buffer()
        return stdout, stderr
