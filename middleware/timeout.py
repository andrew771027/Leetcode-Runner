import signal

from middleware.base import ExecutionMiddleware
from models.execution_request import ExecutionRequest


class TimeoutMiddleware(ExecutionMiddleware):

    def __init__(self, wrapped, seconds: int = 10):
        self.wrapped = wrapped
        self.seconds = seconds

    def run(self, request: ExecutionRequest):
        def handler(signum, frame):
            raise TimeoutError()

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(self.seconds)

        try:
            self.wrapped.run(request)
        finally:
            signal.alarm(0)
