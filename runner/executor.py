import subprocess

BASE_PATH = "../leetcode-solutions/problems"

class Executor:
    def run(self, cmd:list[str]):
        return subprocess.run(cmd)
