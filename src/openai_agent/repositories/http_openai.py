import os
import openai
from openai.openai_object import OpenAIObject
from enum import Enum
import backoff


class Func(str, Enum):
    bash_command = 'bash_command'
    bash_connect = 'bash_connect'
    bash_terminate = 'bash_terminate'
    bash_user_input = 'bash_user_input'
    list_files = 'list_files'
    make_folder = 'make_folder'
    make_file = 'make_file'
    show_file = 'show_file'
    sleep = 'sleep'
    web_search = 'web_search'
    web_read = 'web_read'


FUNCTIONS = [
    {
        'name': Func.bash_command,
        'description': (
            'Execute bash command, returns output after execution '
            'completes or after 1 second (for next output use bash_connect)'
        ),
        'parameters': {
            'type': 'object',
            'properties': {
                'command': {
                    'type': 'string',
                    'description': (
                        'Bash command line.'
                    ),
                },
            },
            'required': ['command'],
        },
    },
    {
        'name': Func.bash_connect,
        'description': 'Show new output of running bash command.',
        'parameters': {},
    },
    {
        'name': Func.bash_terminate,
        'description': 'Terminate running bash command.',
        'parameters': {},
    },
    {
        'name': Func.bash_user_input,
        'description': 'Input line to stdin for running bash command.',
        'parameters': {
            'type': 'object',
            'properties': {
                'stdin': {
                    'type': 'string',
                    'description': 'User input line.'
                },
            },
            'required': ['stdin'],
        },
    },
    {
        'name': Func.list_files,
        'description': 'List folders and files',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {
                    'type': 'string',
                    'description': 'Path for list',
                },
            },
            'required': ['path'],
        },
    },
    {
        'name': Func.make_folder,
        'description': 'Make folder in project',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {
                    'type': 'string',
                    'description': 'Path to folder',
                },
            },
            'required': ['path'],
        },
    },
    {
        'name': Func.make_file,
        'description': 'Create or replace file in project',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {
                    'type': 'string',
                    'description': 'Path with filename',
                },
                'source': {
                    'type': 'string',
                    'description': 'Source of file',
                },
            },
            'required': ['path', 'source'],
        },
    },
    {
        'name': Func.show_file,
        'description': 'Show file in project',
        'parameters': {
            'type': 'object',
            'properties': {
                'path': {
                    'type': 'string',
                    'description': 'Path to file',
                },
            },
            'required': ['path'],
        },
    },
    {
        'name': Func.sleep,
        'description': 'Simulate sleep and summarize the context to reduce its size.',
        'parameters': {},
    },
    {
        'name': Func.web_read,
        'description': 'Open url and read it, return text as markdown',
        'parameters': {
            'type': 'object',
            'properties': {
                'url': {
                    'type': 'string',
                },
            },
            'required': ['url'],
        },
    },
]

YANDEX_FUNCTIONS = [
    {
        'name': Func.web_search,
        'description': 'Internet search engine Yandex',
        'parameters': {
            'type': 'object',
            'properties': {
                'quary': {
                    'type': 'string',
                    'description': 'Search quary',
                },
            },
            'required': ['quary'],
        },
    },
]


@backoff.on_exception(backoff.expo, Exception, max_tries=2)
async def send(user: str, messages: list[dict]) -> OpenAIObject:
    openai.proxy = os.getenv('PROXY')  # type: ignore
    fns = FUNCTIONS.copy()
    if os.getenv('YANDEX_SEARCH_API_KEY') and os.getenv('YANDEX_FOLDERID'):
        fns.extend(YANDEX_FUNCTIONS)
    return await openai.ChatCompletion.acreate(
        api_key=os.getenv('OPENAI_API_KEY'),
        model='gpt-4o',
        messages=messages,
        functions=fns,
        function_call='auto',
        user=user,
    )
