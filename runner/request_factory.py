from models.execution_request import ExecutionRequest 

class RequestFactory:
    def __init__(self, base_path:str):
        self.base_path = base_path
    
    def build(self, category: str, problem:str) -> ExecutionRequest:
        return ExecutionRequest(
            name = problem,
            category= category,
            repo_path=self.base_path,
            test_path=f"tests/{category}/{problem}.py"
        )