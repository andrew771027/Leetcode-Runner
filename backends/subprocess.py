import subprocess
from pathlib import Path

from backends.registry import BackendRegistry
from contracts.backend import ExecutionBackend
from models.execution_request import ExecutionRequest
from models.test_result import TestResult


@BackendRegistry.register("subprocess")
class SubprocessBackend(ExecutionBackend):
    def execute(self, request: ExecutionRequest) -> TestResult:

        repo = Path(request.repo_path).resolve()

        cmd = ["poetry", "run", "pytest", request.test_path, "-q"]

        try:
            result = subprocess.run(
                cmd, 
                cwd=str(repo), 
                capture_output=True, 
                text=True,
                timeout=request.timeout)

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
        
        except subprocess.TimeoutExpired as e:
            return TestResult(
                name=request.name,
                category=request.category,
                problem=request.problem,
                success=False,
                return_code=-1,
                stdout=e.stdout or "",
                stderr=e.stderr or "",
                error=f"Timeout after {request.timeout}s",
            )