import subprocess
import time
from pathlib import Path

from backends.base_backend import ExecutionBackend
from models.execution_request import ExecutionRequest
from models.test_result import TestResult


class SubprocessBackend(ExecutionBackend):
    def run(self, request: ExecutionRequest) -> TestResult:

        repo = Path(request.repo_path).resolve()

        cmd = ["poetry", "run", "pytest", request.test_path, "-q"]

        start_time = time.time()

        result = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True)

        duration = time.time() - start_time

        return TestResult(
            name=request.name,
            category=request.category,
            problem=request.name,
            success=(result.returncode == 0),
            return_code=result.returncode,
            duration=duration,
            stdout=result.stdout,
            stderr=result.stderr,
            error=str(result.returncode),
        )
