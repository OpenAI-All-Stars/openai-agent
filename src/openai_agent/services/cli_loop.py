import readline

from colorama import Fore, Style
from openai_agent.repositories import file_history
from openai_agent.services import ai_agent


async def run(task: str, context: bool):
    readline.parse_and_bind("tab: complete")

    messages = []
    if context and file_history.exists():
        messages = file_history.load()

    developer = ai_agent.Developer(messages)
    if not task:
        task = input_with_history()
        if not task:
            return
    while True:
        result = await developer.work(task)
        print(Fore.GREEN + Style.BRIGHT + result + Style.RESET_ALL)
        task = input_with_history()
        if not task:
            break


def input_with_history(prompt: str = '> ') -> str:
    user_input = input(prompt)
    if user_input.strip():
        readline.add_history(user_input)
    return user_input
