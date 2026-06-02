from typing import List

from contracts.reporter import ExecutionReporter
from models.test_result import TestResult
from reporters.formatter import ResultFormatter
from reporters.registry import ReporterRegistry


@ReporterRegistry.register("log")
class LoggerReporter(ExecutionReporter):

    def __init__(self, logger):
        self.logger = logger

    def report(self, results: List[TestResult]):
        self.logger.info(ResultFormatter.console(results))
