import typer

from runner.backends import SubprocessBackend
from runner.core import Runner

app = typer.Typer()
backend = SubprocessBackend()
runner = Runner(backend)

@app.command()
def test(category: str, problem: str):
    "Run tests for a single problem."
    runner.run_test(category, problem)

@app.command()
def test_all():
    "Run all problems"
    runner.run_all_tests()


if __name__ == "__main__":
    app()
