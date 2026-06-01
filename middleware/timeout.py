import signal

from runner.interfaces import BaseBackend, BaseMiddleware
from middleware.registry import MiddlewareRegistry
from models.test_result import TestResult
from runner.request_factory import ExecutionRequest


@MiddlewareRegistry.register("timeout")
class TimeoutMiddleware(BaseMiddleware):

    def __init__(self, seconds: int = 10):
        self.wrapped = None
        self.seconds = seconds

    def wrap(self, backend: BaseBackend):
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
