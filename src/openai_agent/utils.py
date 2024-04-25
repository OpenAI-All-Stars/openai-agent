import asyncio
import functools
from typing import Callable


def async_command(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorator(*args, **kwargs) -> None:
        asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
    return decorator
