import os
import openai
from openai.openai_object import OpenAIObject
from enum import Enum
import backoff


class Func(str, Enum):
    bash_command = 'bash_command'
    list_files = 'list_files'
    make_folder = 'make_folder'
    make_file = 'make_file'
    show_file = 'show_file'
    sleep = 'sleep'


FUNCTIONS = [
    {
        'name': Func.bash_command,
        'description': 'Execute bash command, returns output after execution completes or after 1 second',
        'parameters': {
            'type': 'object',
            'properties': {
                'stdin': {
                    'type': 'string',
                    'description': (
                        'Bash command line or user input line.'
                        'Can be skipped if new output needs to be viewed.'
                    ),
                },
            },
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
]


@backoff.on_exception(backoff.expo, Exception, max_tries=2)
async def send(user: str, messages: list[dict]) -> OpenAIObject:
    openai.proxy = os.getenv('PROXY')  # type: ignore
    return await openai.ChatCompletion.acreate(
        api_key=os.getenv('OPENAI_API_KEY'),
        model='gpt-4o',
        messages=messages,
        functions=FUNCTIONS,
        function_call='auto',
        user=user,
    )
