Агент для локального запуска, позволяет ChatGPT работать с локальными файлами.

## Установка

```
pipx install git+https://github.com/OpenAI-All-Stars/openai-agent.git
```

В файле ~/.openai-agent нужно будет прописать openai ключ и прокси:

```
OPENAI_API_KEY=xxx
PROXY=zzz
```

## Пример использования

```
openai-agent run --task 'что находится в текущей папке'
```
