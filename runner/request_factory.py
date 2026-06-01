from dataclasses import dataclass


@dataclass
class ExecutionRequest:
    category: str
    problem: str
    test_path: str
    repo_path: str

    @property
    def name(self):
        return self.problem


class RequestFactory:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def create(self, category: str, problem: str) -> ExecutionRequest:
        return ExecutionRequest(
            category=category,
            problem=problem,
            test_path=f"{self.base_path}/tests/{category}/{problem}.py",
            repo_path=self.base_path,
        )
