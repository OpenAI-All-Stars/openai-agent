import asyncio
import json

from colorama import Fore, Style
from openai.openai_object import OpenAIObject

from openai_agent.repositories import http_openai, project_files


class Developer:
    def __init__(self) -> None:
        self.messages = [
            {
                'role': 'system',
                'content': (
                    'Ты ведущий программист на python.'
                    'Будь самостоятельным и используй доступные тебе функции, от этого зависит твоё будущее.'
                ),
            },
        ]

    async def work(self, task: str) -> str:
        self.messages.append(
            {'role': 'user', 'content': task},
        )
        tmp_messages = self.messages.copy()
        response_message = await function_loop(tmp_messages)
        self.messages.append(response_message)
        return response_message.content


async def function_loop(messages: list[dict]) -> OpenAIObject:
    while True:
        resp = await http_openai.send('developer', messages)
        response_message = resp.choices[0].message

        function_call = response_message.get('function_call')
        if not function_call:
            return response_message
        messages.append(response_message)
        function_name = function_call['name']
        match function_name:
            case http_openai.Func.bash_command:
                raw_args = function_call['arguments']
                function_args = json.loads(raw_args)
                command = function_args.get('command')
                if not command:
                    raise Exception('команда не указана')

                print_fn('bash: {}'.format(command))
                
                proc = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()

                messages.append({
                    'role': 'function',
                    'name': function_name,
                    'content': '\n'.join((stdout.decode('utf-8'), stderr.decode('utf-8'))),
                })
            case http_openai.Func.list_files:
                raw_args = function_call['arguments']
                function_args = json.loads(raw_args)
                path = function_args.get('path')
                if not path:
                    raise Exception('путь не указан')
                print_fn('list files {}'.format(path))
                messages.append({
                    'role': 'function',
                    'name': function_name,
                    'content': project_files.list_files(path),
                })
            case http_openai.Func.make_folder:
                raw_args = function_call['arguments']
                function_args = json.loads(raw_args)
                path = function_args.get('path')
                if not path:
                    raise Exception('путь не указан')
                print_fn('make folder {}'.format(path))
                project_files.make_folder(path)
                messages.append({
                    'role': 'function',
                    'name': function_name,
                    'content': f'folder {path} was created',
                })
            case http_openai.Func.make_file:
                raw_args = function_call['arguments']
                function_args = json.loads(raw_args)
                path = function_args.get('path')
                if not path:
                    raise Exception('путь не указан')
                source = function_args.get('source')
                if not source:
                    raise Exception('содержимое файла не указано')
                print_fn('make file {}'.format(path))
                project_files.make_file(path, source)
                messages.append({
                    'role': 'function',
                    'name': function_name,
                    'content': f'file {path} was created',
                })
            case http_openai.Func.show_file:
                raw_args = function_call['arguments']
                function_args = json.loads(raw_args)
                path = function_args.get('path')
                if not path:
                    raise Exception('путь не указан')
                print_fn('show file {}'.format(path))
                messages.append({
                    'role': 'function',
                    'name': function_name,
                    'content': project_files.show_file(path),
                })
            case _:
                raise Exception(
                    'выбрана несуществующая функция {}'.format(
                        function_name
                    )
                )


def print_fn(text: str):
    print(Fore.RED + Style.BRIGHT + text + Style.RESET_ALL)
