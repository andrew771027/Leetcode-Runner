from pathlib import Path

from runner.benchmark import Benchmark
from runner.parallel import ParallelExecutor
from runner.storage import Storage
from runner.tools import run_file, run_pytest


class Runner:

    def __init__(self, base_path: str, backend, discovery):
        self.base_path = base_path
        self.backend = backend
        self.discovery = discovery
        self.parallel = ParallelExecutor()
        self.benchmark = Benchmark()
        self.storage = Storage()

    def run_test(self, category_name: str, problem_name: str):
        path = f"{self.base_path}/{category_name}/{problem_name}.py"

        cmd = run_pytest(path)

        return self.backend.run(cmd, category_name, problem_name)

    def _run_test_file(self, test_file: tuple):
        category = test_file[0]
        problem = Path(test_file[1]).stem
        cmd = run_file(test_file[1])

        result, duration = self.benchmark.measure(self.backend.run, cmd, category, problem)

        # Update duration in result
        result.duration = duration
        return result

    def run_all_tests(self):
        files = self.discovery.all_tests()
        results = self.parallel.run(self._run_test_file, files)

        for r in results:
            self.storage.append(r)

        return results
