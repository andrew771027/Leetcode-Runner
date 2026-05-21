import subprocess
import time
from typing import List

from backends.base_backend import ExecutionBackend
from models.test_result import TestResult


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
            stdout=result.stdout,
            stderr=result.stderr,
            error=str(result.returncode),
        )
