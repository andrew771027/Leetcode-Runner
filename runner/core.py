from runner.executor import Executor
from runner.tools import run_pytest


class Runner:

    def __init__(self, backend):
        self.backend = backend

    def run_test(self, category_name:str, problem_name:str):
        path = f"/Users/poyuan/Desktop/andrew771027/LeetCode/tests/{category_name}/{problem_name}.py"

        cmd = run_pytest(path)

        return self.backend.run(cmd, category_name, problem_name)


    def run_all_tests(self):
        print("🚀 running all problems...")
        # 先簡化，之後再做 discovery
