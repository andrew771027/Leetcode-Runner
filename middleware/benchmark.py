import time

from middleware.base import ExecutionMiddleware
from models.execution_request import ExecutionRequest
from models.test_result import TestResult


class BenchmarkMiddleware(ExecutionMiddleware):

    def __init__(self, wrapper):
        self.wrapper = wrapper

    def run(self, request: ExecutionRequest) -> TestResult:
        start = time.perf_counter()

        result = self.wrapper.run(request)

        result.duration = time.perf_counter() - start

        return result
