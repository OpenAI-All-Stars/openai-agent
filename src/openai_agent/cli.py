import logging

import click
from colorama import init

from openai_agent.services import ai_agent
from openai_agent.utils import async_command


@click.group()
def cli() -> None:
    init()
    logging.basicConfig(level=logging.INFO)
    openai_logger = logging.getLogger('openai')
    openai_logger.setLevel(logging.ERROR)


@cli.command()
@click.option('--task', required=True)
@async_command
async def run(task: str) -> None:
    try:
        developer = ai_agent.Developer()
        while True:
            result = await developer.work(task)
            print(result)
            task = input('> ')
            if not task:
                break
    except KeyboardInterrupt:
        pass
