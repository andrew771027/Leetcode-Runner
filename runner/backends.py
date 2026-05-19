import subprocess
from typing import List, Protocol


class ExecutionBackend(Protocol):
    def run(self, cmd: List[str]) -> int:
        ...

class SubprocessBackend:
    def run(self, cmd: List[str]) -> int:
        result = subprocess.run(cmd)
        return result.returncode
