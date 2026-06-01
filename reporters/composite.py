from typing import List

from models.test_result import TestResult
from reporters.base import Reporter


class CompositeReporter(Reporter):

    def __init__(self, reporters: List[Reporter]):
        self.reporters = reporters

    def report(self, results: List[TestResult]):
        for reporter in self.reporters:
            reporter.report(results)
