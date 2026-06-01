from typing import List

from models.test_result import TestResult
from reporters.registry import ReporterRegistry
from runner.interfaces import BaseReporter


@ReporterRegistry.register("log")
class LoggerReporter(BaseReporter):

    def __init__(self, logger):
        self.logger = logger

    def report(self, results: List[TestResult]):
        for r in results:
            self.logger.log_result(r)
