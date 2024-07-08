import logging

import click
import colorama

from openai_agent import deps
from openai_agent.repositories import dotenv
from openai_agent.services import cli_loop
from openai_agent.utils import async_command


@click.command()
@click.option('--task')
@click.option('--context/--no-context', default=False, help='Load previous context.')
@async_command
async def cli(task: str, context: bool) -> None:
    try:
        logging.basicConfig(level=logging.ERROR)

        colorama.init()
        dotenv.init()

        dotenv.set_secret('OPENAI_API_KEY')
        dotenv.set_secret('PROXY')

        async with deps.use_all():
            await cli_loop.run(task, context)
    except KeyboardInterrupt:
        pass
