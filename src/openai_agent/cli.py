import logging

import click

from openai_agent.services import ai_agent
from openai_agent.utils import async_command


@click.group()
def cli() -> None:
    logging.basicConfig(level=logging.INFO)


@cli.command()
@click.option('--task', required=True)
@async_command
async def run(task: str) -> None:
    try:
        developer = ai_agent.Developer()
        reviewer = ai_agent.Reviewer(task)
        comments = task
        while True:
            result = await developer.work(comments)
            print(result)
            comments = await reviewer.check_work(result)
            if not comments:
                break
            print(comments)
    except KeyboardInterrupt:
        pass
