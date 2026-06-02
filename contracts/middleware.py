from abc import ABC, abstractmethod

from contracts.backend import ExecutionBackend
from models.execution_request import ExecutionRequest
from models.test_result import TestResult


class ExecutionMiddleware(ABC):
    @abstractmethod
    def wrap(self, backend: ExecutionBackend):
        pass

    @abstractmethod
    def execute(self, request: ExecutionRequest) -> TestResult:
        pass
