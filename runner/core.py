from pathlib import Path
from typing import List

from models.test_result import TestResult
from runner.config import RunnerConfig
from backends.base import ExecutionBackend
from runner.request_factory import RequestFactory

class Runner:

    def __init__(self, 
                 config: RunnerConfig, 
                 backend: ExecutionBackend, 
                 discovery,
                 executor, 
                 request_factory:RequestFactory):
        self.config = config
        self.backend = backend
        self.discovery = discovery
        self.executor = executor
        self.request_factory = request_factory
    
    def run_test(self, category: str, problem: str) -> TestResult:

        request = self.request_factory.build(category=category, problem=problem)

        return self.backend.run(request)

    def run_all_tests(self) -> List[TestResult]:
        files = self.discovery.find_all()

        return self.executor.run(
            self._execute,
            files,
            max_workers=self.config.workers,
        )

    def _execute(self, test_file):
        category, path = test_file
        problem = Path(path).stem

        request = self.request_factory.build(category=category, problem=problem)
        return self.backend.run(request)

