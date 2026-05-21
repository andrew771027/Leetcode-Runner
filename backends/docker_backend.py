import subprocess
import time
from pathlib import Path

from backends.base_backend import ExecutionBackend
from models.test_result import TestResult


class DockerBackend(ExecutionBackend):

    def __init__(self, image: str = "leetcode-runner-base"):
        self.image = image

    def run(self, repo_path: str, test_path: str, name: str) -> TestResult:
        start = time.perf_counter()

        repo = Path(repo_path).resolve()

        start = time.perf_counter()

        cmd = [
            "docker",
            "run",
            "--rm",
            # mount repo
            "-v",
            f"{repo}:/workspace",
            # working dir
            "-w",
            "/workspace",
            self.image,
            "bash",
            "-c",
            ("poetry install --no-interaction && " f"poetry run pytest {test_path} -q"),
        ]

        process = subprocess.run(cmd, capture_output=True, text=True)

        duration = time.perf_counter() - start

        # derive category and problem from test_path when possible
        try:
            category = Path(test_path).parent.name
            problem = Path(test_path).stem
        except Exception:
            category = ""
            problem = name or ""

        return TestResult(
            name=name,
            category=category,
            problem=problem,
            success=(process.returncode == 0),
            return_code=process.returncode,
            duration=duration,
            stdout=process.stdout,
            stderr=process.stderr,
            error="" if process.returncode == 0 else process.stderr,
        )
