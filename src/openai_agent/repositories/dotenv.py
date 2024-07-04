from getpass import getpass
import os

import dotenv


ENV_PATH = os.path.expanduser('~/.openai-agent')


def init():
    if not os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'w'):
            pass
    dotenv.load_dotenv(ENV_PATH)


def set_secret(key_name: str):
    key = os.getenv(key_name)
    if not key:
        key = getpass(f'{key_name}: ')
        dotenv.set_key(ENV_PATH, key_name, key)
        print(f'{ENV_PATH} updated')
