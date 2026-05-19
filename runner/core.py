from pathlib import Path
from typing import List

from runner.benchmark import Benchmark
from runner.models import TestResult
from runner.parallel import ParallelExecutor
from runner.storage import Storage
from runner.tools import run_file, run_pytest


class Runner:

    def __init__(self, base_path: str, backend, discovery, logger, analytics):
        self.base_path = base_path
        self.backend = backend
        self.discovery = discovery
        self.parallel = ParallelExecutor()
        self.benchmark = Benchmark()
        self.storage = Storage()
        self.logger = logger
        self.analytics = analytics

    def run_test(self, category_name: str, problem_name: str):
        path = f"{self.base_path}/{category_name}/{problem_name}.py"

        cmd = run_pytest(path)

        result = self.backend.run(cmd, category_name, problem_name)

        self.logger.log(
            {
                "type": "test_run",
                "name": f"{category_name} {problem_name}",
                "success": result.success,
                "duration": result.duration,
            }
        )
        return result

    def _run_test_file(self, test_file: tuple):
        category = test_file[0]
        problem = Path(test_file[1]).stem
        cmd = run_file(test_file[1])

        result, duration = self.benchmark.measure(self.backend.run, cmd, category, problem)

        # Update duration in result
        result.duration = duration

        self.logger.log(
            {
                "type": "test_run",
                "name": f"{category} {problem}",
                "success": result.success,
                "duration": result.duration,
            }
        )
        return result

    def run_all_tests(self):
        files = self.discovery.all_tests()
        results = self.parallel.run(self._run_test_file, files)

        for r in results:
            self.storage.append(r)

        return results

    def analyze(self, results: List[TestResult]):
        return self.analytics.summary(results)
