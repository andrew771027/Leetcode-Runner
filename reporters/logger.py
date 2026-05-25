from typing import List
from reporters.base import Reporter
from models.test_result import TestResult

class LoggerReporter(Reporter):

    def __init__(self, logger):
        self.logger = logger
    
    def report(self, results: List[TestResult]):
        for r in results:
            self.logger.log_result(r)