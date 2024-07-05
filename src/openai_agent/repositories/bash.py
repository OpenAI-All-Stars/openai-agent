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


async def execute(command: str | None) -> BashResult:
    global PROC
    if PROC.was_run:
        await PROC.user_input(command)
    else:
        assert command is not None
        await PROC.shell(command)
    stdout, stderr = await PROC.wait()
    return BashResult(
        stdout=stdout,
        stderr=stderr,
    )
