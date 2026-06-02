from typing import List

from contracts.backend import ExecutionBackend
from contracts.middleware import ExecutionMiddleware, NextHandler
from models.execution_request import ExecutionRequest
from models.test_result import TestResult

class MiddlewarePipeline:

    def __init__(self, 
                 backend: ExecutionBackend, 
                 middlewares: List[ExecutionMiddleware]
    ):
        self.backend = backend
        self.middlewares = middlewares
    
    def execute(self, request: ExecutionRequest) -> TestResult:
        handler = self.backend.execute

        for middleware in reversed(self.middlewares):
            next_handler: NextHandler = handler

            def make_handler(mw: ExecutionMiddleware, nxt: NextHandler):
                return lambda req: mw.execute(req, nxt)
        
            handler = make_handler(middleware, next_handler)
        
        return handler(request)