from pathlib import Path
from typing import List

from models.config import RunnerConfig
from models.execution_request import ExecutionRequest
from models.test_result import TestResult
from runner.benchmark import Benchmark
from runner.parallel import ParallelExecutor
from runner.storage import Storage


class Runner:

    def __init__(self, config: RunnerConfig, backend, discovery, logger):
        self.base_path = config.base_path
        self.backend = backend
        self.discovery = discovery
        self.parallel = ParallelExecutor()
        self.benchmark = Benchmark()
        self.storage = Storage()
        self.logger = logger

    def run_test(self, category: str, problem: str) -> TestResult:

        request = ExecutionRequest(
            name=problem,
            category=category,
            repo_path=self.base_path,
            test_path=f"tests/{category}/{problem}.py",
        )

        result = self.backend.run(request)

        self._log_result(result)

        return result

    def run_all_tests(self) -> List[TestResult]:
        files = self.discovery.all_tests()
        results = self.parallel.run(self._run_test_file, files)

        for r in results:
            self.storage.append(r)

        return results

    def _run_test_file(self, test_file: tuple):
        category = test_file[0]
        problem = Path(test_file[1]).stem

        request = ExecutionRequest(
            name=problem,
            category=category,
            repo_path=self.base_path,
            test_path=f"tests/{category}/{problem}.py",
        )

        result, duration = self.benchmark.measure(self.backend.run, request)  # repo_path

        # Update duration in result
        result.duration = duration

        self._log_result(result)

        return result

    def _log_result(self, result: TestResult):
        self.logger.log(
            {
                "type": "test_run",
                "name": result.name,
                "success": result.success,
                "duration": result.duration,
            }
        )
