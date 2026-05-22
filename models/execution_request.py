from dataclasses import dataclass


@dataclass
class ExecutionRequest:
    repo_path: str
    test_path: str
    name: str
    category: str | None = None
