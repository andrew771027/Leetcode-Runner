from runner.tools import run_file, run_pytest


class Runner:

    def __init__(self, base_path: str, backend, discovery):
        self.base_path = base_path
        self.backend = backend
        self.discovery = discovery

    def run_test(self, category_name: str, problem_name: str):
        path = f"{self.base_path}/{category_name}/{problem_name}.py"

        cmd = run_pytest(path)

        return self.backend.run(cmd, category_name, problem_name)

    def run_all_tests(self):
        results = []

        for categoty, test_file in self.discovery.all_tests():

            print(categoty, test_file)
            cmd = run_file(test_file)
            _result = self.backend.run(cmd, categoty, test_file.stem)
            results.append(_result)

        return results
