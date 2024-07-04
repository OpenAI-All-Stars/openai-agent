import os


def list_files(root: str) -> str:
    try:
        return '\n'.join(os.listdir(root))
    except FileNotFoundError as e:
        return str(e)


def make_folder(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def make_file(path: str, source: str) -> None:
    dir = os.path.dirname(path)
    if dir:
        os.makedirs(dir, exist_ok=True)
    with open(path, 'w') as f:
        f.write(source)


def show_file(path: str) -> str:
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError as e:
        return str(e)
