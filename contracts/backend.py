from abc import ABC, abstractmethod

from models.execution_request import ExecutionRequest
from models.test_result import TestResult


class ExecutionBackend(ABC):
    @abstractmethod
    def execute(self, request: ExecutionRequest) -> TestResult:
        pass
