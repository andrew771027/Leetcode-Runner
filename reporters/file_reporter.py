from typing import List

from contracts.reporter import ExecutionReporter
from models.test_result import TestResult
from reporters.registry import ReporterRegistry


@ReporterRegistry.register("file")
class FileReporter(ExecutionReporter):

    def __init__(self, storage):
        self.storage = storage

    def report(self, results: List[TestResult]):
        for r in results:
            self.storage.append(r)
