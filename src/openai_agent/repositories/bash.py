from dataclasses import dataclass

from openai_agent.utils import Process


PROC = Process()


@dataclass
class BashResult:
    stdout: str
    stderr: str

    @property
    def all(self) -> str:
        return '\n'.join((self.stdout, self.stderr))


async def execute(command: str) -> BashResult:
    global PROC
    if PROC.was_run:
        raise Exception('Сейчас уже есть запущенная bash команда')
    else:
        await PROC.shell(command)
    stdout, stderr = await PROC.wait()
    return BashResult(
        stdout=stdout,
        stderr=stderr,
    )


async def connect(stdin: str | None) -> BashResult:
    global PROC
    if PROC.was_run:
        await PROC.user_input(stdin)
    else:
        raise Exception('Сейчас нет запущенной bash команды')
    stdout, stderr = await PROC.wait()
    return BashResult(
        stdout=stdout,
        stderr=stderr,
    )


async def terminate():
    global PROC
    if PROC.was_run:
        await PROC.terminate()
