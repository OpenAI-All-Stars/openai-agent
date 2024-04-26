from enum import Enum
import openai
from openai.openai_object import OpenAIObject
from simple_settings import settings


class Func(str, Enum):
    bash = 'bash'
    python = 'python'


FUNCTIONS = [
    {
        'name': Func.bash,
        'description': 'Execute any bash command in Linux',
        'parameters': {
            'type': 'object',
            'properties': {
                'command': {
                    'type': 'string',
                    'description': 'Bash command body',
                },
            },
            'required': ['command'],
        },
    },
    {
        'name': Func.python,
        'description': 'Execute python code',
        'parameters': {
            'type': 'object',
            'properties': {
                'code': {
                    'type': 'string',
                    'description': 'Code',
                },
            },
            'required': ['code'],
        },
    },
]


async def send(user: str, messages: list[dict]) -> OpenAIObject:
    return await openai.ChatCompletion.acreate(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL,
        messages=messages,
        functions=FUNCTIONS,
        function_call='auto',
        user=user,
    )
