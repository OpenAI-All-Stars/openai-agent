import os
import pickle


STORE_PATH = '.openai-agent-history'


def save(messages: list):
    with open(STORE_PATH, 'wb') as f:
        pickle.dump(messages, f)


def load() -> list:
    with open(STORE_PATH, 'rb') as f:
        return pickle.load(f)


def exists() -> bool:
    return os.path.exists(STORE_PATH)
