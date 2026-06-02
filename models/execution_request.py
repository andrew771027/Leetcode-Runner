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
