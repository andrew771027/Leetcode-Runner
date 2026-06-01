from typing import List

from models.test_result import TestResult
from runner.interfaces import BaseReporter
from reporters.registry import ReporterRegistry


@ReporterRegistry.register("storage")
class StorageReporter(BaseReporter):

    def __init__(self, storage):
        self.storage = storage

    def report(self, results: List[TestResult]):
        for r in results:
            self.storage.append(r)
