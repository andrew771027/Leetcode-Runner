from abc import ABC, abstractmethod
from typing import Callable

from contracts.backend import ExecutionBackend
from models.execution_request import ExecutionRequest
from models.test_result import TestResult

NextHandler = Callable[[ExecutionRequest], TestResult]


class ExecutionMiddleware(ABC):
    @abstractmethod
    def execute(self, request: ExecutionRequest, next_handler: NextHandler) -> TestResult:
        pass
