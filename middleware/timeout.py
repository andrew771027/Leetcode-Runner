# NOTE:
# This signal-based timeout only works in the main thread.
# It is not compatible with ThreadPoolExecutor-based parallel execution.
# Keep this middleware for future refactor.

import signal

from contracts.backend import ExecutionBackend
from contracts.middleware import ExecutionMiddleware, NextHandler
from middleware.registry import MiddlewareRegistry
from models.execution_request import ExecutionRequest
from models.test_result import TestResult


@MiddlewareRegistry.register("timeout")
class TimeoutMiddleware(ExecutionMiddleware):

    def __init__(self, seconds: int = 10):
        self.seconds = seconds

    def execute(self, 
                request: ExecutionRequest, 
                next_handler: NextHandler
        ) -> TestResult:
        
        def handler(signum, frame):
            raise TimeoutError()

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(self.seconds)

        try:
            return next_handler(request)
        finally:
            signal.alarm(0)
