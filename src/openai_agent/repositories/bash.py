from asyncio import create_subprocess_shell, subprocess
from dataclasses import dataclass


@dataclass
class BashResult:
    stdout: str
    stderr: str


async def execute(command: str) -> BashResult:
    proc = await create_subprocess_shell(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return BashResult(
        stdout=stdout.decode(),
        stderr=stderr.decode(),
    )
