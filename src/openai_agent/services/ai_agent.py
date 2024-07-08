import json

from colorama import Fore, Style

from openai_agent.repositories import file_history, http_openai, project_files, bash
from openai_agent.utils import spinning_ctx


class Exit(Exception):
    pass


class Developer:
    def __init__(self, messages: list | None = None) -> None:
        self.messages = messages or [
            {
                'role': 'system',
                'content': (
                    'Будь самостоятельным и используй доступные тебе функции, от этого зависит твоё будущее.'
                    'Не проси пользователя что-то сделать, если ты сам можешь это сделать.'
                    'Тебе доступно изменение файлов.'
                ),
            },
        ]

    async def work(self, task: str) -> str:
        self.messages.append(
            {'role': 'user', 'content': task},
        )
        answer = await function_loop(self.messages)
        file_history.save(self.messages)
        return answer


async def function_loop(messages: list[dict]) -> str:
    while True:
        with spinning_ctx():
            try:
                resp = await http_openai.send('developer', messages)
            except KeyboardInterrupt as e:
                messages.append({
                    'role': 'system',
                    'content': str(e),
                })
        response_message = resp.choices[0].message

        function_call = response_message.get('function_call')
        messages.append(response_message)
        if not function_call:
            return response_message.content
        try:
            await function_match(messages, function_call)
        except Exit:
            return 'Проснулся!'
        except Exception as e:
            messages.append({
                'role': 'function',
                'name': function_call['name'],
                'content': str(e),
            })


async def function_match(messages: list[dict], function_call: dict):
    function_name = function_call['name']
    match function_name:
        case http_openai.Func.bash_command:
            raw_args = function_call['arguments']
            function_args = json.loads(raw_args)
            command = function_args.get('command')
            if not command:
                raise Exception('команда не указана')

            print_fn('bash: {}'.format(command))

            std = await bash.execute(command)

            messages.append({
                'role': 'function',
                'name': function_name,
                'content': std.all,
            })
        case http_openai.Func.bash_connect:
            print_fn('bash connect')
            std = await bash.connect(None)

            messages.append({
                'role': 'function',
                'name': function_name,
                'content': std.all,
            })
        case http_openai.Func.bash_user_input:
            raw_args = function_call['arguments']
            function_args = json.loads(raw_args)
            stdin = function_args.get('stdin')
            if not stdin:
                raise Exception('строка ввода не указана')

            print_fn('bash user input: {}'.format(stdin))

            std = await bash.connect(stdin)

            messages.append({
                'role': 'function',
                'name': function_name,
                'content': std.all,
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
        case http_openai.Func.sleep:
            print_fn('sleep')
            await simulate_sleep(messages)
            raise Exit
        case _:
            raise Exception(
                'выбрана несуществующая функция {}'.format(
                    function_name
                )
            )


def print_fn(text: str):
    print(Fore.RED + Style.BRIGHT + text + Style.RESET_ALL)


async def simulate_sleep(messages: list[dict]):
    """
    Симулирует "сон" агента, суммируя контекст сообщений для его уменьшения.
    """
    messages.append({
        'role': 'user',
        'content': 'Обобщи текущий контекст',
    })
    resp = await http_openai.send('developer', messages)
    response_message = resp.choices[0].message
    messages.clear()
    messages.append(response_message)
