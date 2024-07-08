from contextlib import asynccontextmanager
from typing import AsyncIterator
from aiohttp import ClientSession

from openai_agent.registry import RegistryValue


http_client = RegistryValue[ClientSession]()


@asynccontextmanager
async def use_http_client() -> AsyncIterator[ClientSession]:
    async with ClientSession() as client:
        http_client.set(client)
        yield client


@asynccontextmanager
async def use_all() -> AsyncIterator[None]:
    async with use_http_client():
        yield
