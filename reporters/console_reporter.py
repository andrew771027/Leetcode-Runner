from typing import List

from contracts.reporter import ExecutionReporter
from models.test_result import TestResult
from reporters.formatter import ResultFormatter
from reporters.registry import ReporterRegistry


@ReporterRegistry.register("console")
class ConsoleReporter(ExecutionReporter):

    def report(self, results: List[TestResult]):
        print(ResultFormatter.console(results))
