import readline

from colorama import Fore, Style
from openai_agent.services import ai_agent


async def run(task: str):
    readline.parse_and_bind("tab: complete")

    developer = ai_agent.Developer()
    if not task:
        task = input_with_history()
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
