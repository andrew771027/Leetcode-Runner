import os
import subprocess

BASE_PATH = "../leetcode-solutions/problems"

def run_tests(category_name: str, problem_name:str) -> None:
    path = f"/Users/poyuan/Desktop/andrew771027/LeetCode/tests/{category_name}/{problem_name}.py"

    cmd = ["python", "-m", "pytest", path, "-v"]

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print(f"✅ {problem_name} PASS")
    else:
        print(f"❌ {problem_name} FAIL")

def run_all_tests() -> None:
    print("🚀 running all problems...")
    # 先簡化，之後再做 discovery
