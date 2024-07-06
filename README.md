Агент для локального запуска, позволяет ChatGPT работать с локальными файлами.

## Установка

```
pipx install git+https://github.com/OpenAI-All-Stars/openai-agent.git
```

## Предварительная настройка

В файле ~/.openai-agent хранятся секреты. При первом запуске, агент предложит их заполнить.

* OPENAI_API_KEY - ваш ключ от openai api
* PROXY - прокси, если нужен, можно оставить пустым

## Пример использования

```
openai-agent run
```
