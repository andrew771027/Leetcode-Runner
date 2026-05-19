from runner.executor import Executor
from runner.tools import run_pytest


class Runner:

    def __init__(self, backend):
        self.backend = Executor()

    def run_test(self, category_name:str, problem_name:str):
        path = f"/Users/poyuan/Desktop/andrew771027/LeetCode/tests/{category_name}/{problem_name}.py"

        cmd = run_pytest(path)

        result = self.backend.run(cmd)

        if result.returncode == 0:
            print(f"✅ {problem_name} PASS")
        else:
            print(f"❌ {problem_name} FAIL")

    def run_all_tests(self):
        print("🚀 running all problems...")
        # 先簡化，之後再做 discovery
