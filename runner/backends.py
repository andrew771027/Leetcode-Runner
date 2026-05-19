import subprocess
import time
from abc import ABC, abstractmethod
from typing import List

from runner.models import TestResult


class ExecutionBackend(ABC):
    @abstractmethod
    def run(self, cmd: List[str]) -> int:
        pass


class SubprocessBackend(ExecutionBackend):
    def run(self, cmd: List[str], category: str, problem: str) -> TestResult:
        start_time = time.time()

        result = subprocess.run(cmd)

        duration = time.time() - start_time

        return TestResult(
            name=f"{category} {problem}",
            category=category,
            problem=problem,
            success=(result.returncode == 0),
            return_code=result.returncode,
            duration=duration,
        )


class DockerBackend(ExecutionBackend):
    def run(self, cmd: List[str]) -> int:
        pass
