from typing import List

from middleware.base import ExecutionMiddleware
from models.execution_request import ExecutionRequest


class RetryMiddleware(ExecutionMiddleware):

    def __init__(self, wrapper, retries=2):
        self.wrapper = wrapper
        self.retries = retries

    def run(self, requests: List[ExecutionRequest]):
        last_error = None

        for _ in range(self.retries):
            try:
                self.wrapper.run(requests)
            except Exception as e:
                last_error = e

        raise last_error
