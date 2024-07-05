Агент для локального запуска, позволяет ChatGPT работать с локальными файлами.

## Установка

```
pipx install git+https://github.com/OpenAI-All-Stars/openai-agent.git
```

В файле ~/.openai-agent хранятся секреты:

```
OPENAI_API_KEY=xxx
PROXY=zzz
```

OPENAI_API_KEY - ваш ключ от openai api
PROXY - прокси, если нужен, можно оставить пустым

## Пример использования

```
openai-agent run --task 'что находится в текущей папке?'
```
