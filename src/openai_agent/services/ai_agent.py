import json
from openai_agent.repositories import bash, http_openai


from openai.openai_object import OpenAIObject


class Developer:
    def __init__(self) -> None:
        self.messages = [
            {
                'role': 'system',
                'content': (
                    'Представь что ты старший разработчик на python. '
                    'После завершения работы над задачей, '
                    'напиши как её проверить.'
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


class Reviewer:
    def __init__(self, task: str) -> None:
        self.messages = [
            {
                'role': 'system',
                'content': (
                    'Представь что ты старший разработчик на python. '
                    'Тебе нужно проверить результат работы '
                    'другого программиста.'
                    'Если ты считаешь что задача решена правильно, '
                    'то пиши `готово`, иначе пиши комментарий по исправлению.'
                ),
            },
            {'role': 'user', 'content': task},
        ]

    async def check_work(self, result: str) -> str | None:
        self.messages.append(
            {'role': 'user', 'content': result},
        )
        tmp_messages = self.messages.copy()
        response_message = await function_loop(tmp_messages)
        self.messages.append(response_message)
        if response_message.content.lower() == 'готово':
            return None
        return response_message.content


async def function_loop(messages: list[dict]) -> OpenAIObject:
    while True:
        resp = await http_openai.send('developer', messages)
        response_message = resp.choices[0].message

        function_call = response_message.get('function_call')
        if not function_call:
            return response_message
        match function_call['name']:
            case http_openai.Func.bash:
                raw_args = function_call['arguments']
                function_args = json.loads(raw_args)
                command = function_args.get('command')
                if not command:
                    raise Exception('пустая команда')
                bash_result = await bash.execute(command)
                messages.append({
                    'role': 'function',
                    'name': function_call['name'],
                    'content': '{}\n{}'.format(
                        bash_result.stderr,
                        bash_result.stdout,
                    ),
                })
            case http_openai.Func.python:
                raw_args = function_call['arguments']
                function_args = json.loads(raw_args)
                code = function_args.get('code')
                if not code:
                    raise Exception('пустой код')
                messages.append({
                    'role': 'function',
                    'name': function_call['name'],
                    'content': str(eval(code)),
                })
            case _:
                raise Exception(
                    'выбрана несуществующая функция {}'.format(
                        function_call['name']
                    )
                )
