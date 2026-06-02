from models.execution_request import ExecutionRequest


class RequestFactory:
    def __init__(self, base_path: str, timeout: int | None = None):
        self.base_path = base_path
        self.timeout = timeout

    def create(self, category: str, problem: str) -> ExecutionRequest:
        return ExecutionRequest(
            category=category,
            problem=problem,
            test_path=f"{self.base_path}/tests/{category}/{problem}.py",
            repo_path=self.base_path,
            timeout=self.timeout,
        )
