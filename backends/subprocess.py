import subprocess
from pathlib import Path

from runner.interfaces import BaseBackend
from backends.registry import BackendRegistry
from models.test_result import TestResult
from runner.request_factory import ExecutionRequest


@BackendRegistry.register("subprocess")
class SubprocessBackend(BaseBackend):
    def execute(self, request: ExecutionRequest) -> TestResult:

        repo = Path(request.repo_path).resolve()

        cmd = ["poetry", "run", "pytest", request.test_path, "-q"]

        result = subprocess.run(cmd, cwd=str(repo), capture_output=True, text=True)

        return TestResult(
            name=request.name,
            category=request.category,
            problem=request.problem,
            success=(result.returncode == 0),
            return_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            error=str(result.returncode),
        )
