from enum import Enum
import os
import openai
from openai.openai_object import OpenAIObject


class Func(str, Enum):
    bash_command = 'bash_command'
    list_files = 'list_files'
    make_folder = 'make_folder'
    make_file = 'make_file'
    show_file = 'show_file'


FUNCTIONS = [
    {
        'name': Func.bash_command,
        'description': 'Execute bash command',
        'parameters': {
            'type': 'object',
            'properties': {
                'command': {
                    'type': 'string',
                    'description': 'Bash command line',
                },
            },
            'required': ['command'],
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
]


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
