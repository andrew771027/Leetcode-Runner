import subprocess
from pathlib import Path

from backends.registry import BackendRegistry
from models.test_result import TestResult
from runner.interfaces import BaseBackend
from runner.request_factory import ExecutionRequest


@BackendRegistry.register("docker")
class DockerBackend(BaseBackend):

    def __init__(self, image: str = "leetcode-runner-base"):
        self.image = image

    def execute(self, request: ExecutionRequest) -> TestResult:

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

        process = subprocess.run(cmd, capture_output=True, text=True)

        return TestResult(
            name=request.name,
            category=request.category,
            problem=request.problem,
            success=(process.returncode == 0),
            return_code=process.returncode,
            stdout=process.stdout,
            stderr=process.stderr,
            error="" if process.returncode == 0 else process.stderr,
        )
