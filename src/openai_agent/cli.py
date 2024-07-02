from getpass import getpass
import logging
import os

import click
from colorama import init
from dotenv import load_dotenv, set_key

from openai_agent.services import ai_agent
from openai_agent.utils import async_command


@click.group()
def cli() -> None:
    init()
    dotenv_path = os.path.expanduser('~/.openai-agent')
    if not os.path.exists(dotenv_path):
        with open(dotenv_path, 'w'):
            pass
    load_dotenv(dotenv_path)

    key_name = 'OPENAI_API_KEY'
    key = os.getenv(key_name)
    if not key:
        key = getpass(f'{key_name}: ')
        set_key(dotenv_path, key_name, key)
        print(f'Секрет {key_name} сохранён в {dotenv_path}.')

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
