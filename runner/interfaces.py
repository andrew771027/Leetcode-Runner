from abc import ABC, abstractmethod

from models.test_result import TestResult
from runner.request_factory import ExecutionRequest


class BaseBackend(ABC):
    @abstractmethod
    def execute(self, request: ExecutionRequest) -> TestResult:
        pass


class BaseReporter(ABC):
    @abstractmethod
    def report(self, results):
        pass


class BaseMiddleware(ABC):
    @abstractmethod
    def wrap(self, backend: BaseBackend):
        pass

    @abstractmethod
    def execute(self, request: ExecutionRequest) -> TestResult:
        pass
