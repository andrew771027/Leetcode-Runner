import signal

from contracts.backend import ExecutionBackend
from contracts.middleware import ExecutionMiddleware
from middleware.registry import MiddlewareRegistry
from models.execution_request import ExecutionRequest
from models.test_result import TestResult


@MiddlewareRegistry.register("timeout")
class TimeoutMiddleware(ExecutionMiddleware):

    def __init__(self, seconds: int = 10):
        self.wrapped = None
        self.seconds = seconds

    def wrap(self, backend: ExecutionBackend):
        self.backend = backend
        return self

    def execute(self, request: ExecutionRequest) -> TestResult:
        def handler(signum, frame):
            raise TimeoutError()

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(self.seconds)

        try:
            return self.wrapped.execute(request)
        finally:
            signal.alarm(0)
