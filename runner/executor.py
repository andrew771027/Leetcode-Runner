import os
import subprocess

BASE_PATH = "../leetcode-solutions/problems"

def run_tests(problem_name:str) -> None:
    # problem_path = os.path.join(BASE_PATH, problem_name)
    problem_path = "/Users/poyuan/Desktop/andrew771027/LeetCode/tests/array/test_lc_001_two_sum.py"
    # cmd = ["python", "-m", "pytest", problem_path, "-v"]
    cmd = ["poetry", "run", "pytest", problem_path, "-v"]
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print(f"✅ {problem_name} PASS")
    else:
        print(f"❌ {problem_name} FAIL")
