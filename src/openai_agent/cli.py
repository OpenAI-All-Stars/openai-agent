import logging

import click
import colorama

from openai_agent.repositories import dotenv
from openai_agent.services import cli_loop
from openai_agent.utils import async_command


@click.group()
def cli() -> None:
    colorama.init()
    dotenv.init()

    dotenv.set_secret('OPENAI_API_KEY')
    dotenv.set_secret('PROXY')

    logging.basicConfig(level=logging.INFO)
    openai_logger = logging.getLogger('openai')
    openai_logger.setLevel(logging.ERROR)


@cli.command()
@click.option('--task')
@async_command
async def run(task: str) -> None:
    try:
        await cli_loop.run(task)
    except KeyboardInterrupt:
        pass
