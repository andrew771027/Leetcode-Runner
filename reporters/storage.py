from typing import List
from reporters.base import Reporter
from models.test_result import TestResult

class StorageReporter(Reporter):

    def __init__(self, storage):
        self.storage = storage
    
    def report(self, results: List[TestResult]):
        for r in results:
            self.storage.append(r)