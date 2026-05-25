import subprocess
import time
from pathlib import Path

from backends.base import ExecutionBackend
from models.execution_request import ExecutionRequest
from models.test_result import TestResult


class DockerBackend(ExecutionBackend):

    def __init__(self, image: str = "leetcode-runner-base"):
        self.image = image

    def run(self, request: ExecutionRequest) -> TestResult:

        repo = Path(request.repo_path).resolve()

        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{repo}:/workspace",
            "-w",
            "/workspace",
            self.image,
            "bash",
            "-c",
            ("poetry install --no-interaction && " f"poetry run pytest {request.test_path} -q"),
        ]

        start = time.perf_counter()

        process = subprocess.run(cmd, capture_output=True, text=True)

        duration = time.perf_counter() - start

        return TestResult(
            name=request.name,
            category=request.category,
            problem=request.name,
            success=(process.returncode == 0),
            return_code=process.returncode,
            duration=duration,
            stdout=process.stdout,
            stderr=process.stderr,
            error="" if process.returncode == 0 else process.stderr,
        )
