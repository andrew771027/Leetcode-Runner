import time

from backends.base import ExecutionBackend


class BenchmarkBackend(ExecutionBackend):

    def __init__(self, wrapper: ExecutionBackend):
        self.wrapper = wrapper

    def run(self, request):
        start = time.perf_counter()

        result = self.wrapper.run(request)

        result.duration = time.perf_counter() - start

        return result
