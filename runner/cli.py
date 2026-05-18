import typer
from executor import run_all_tests, run_tests

app = typer.Typer()

@app.command()
def test(category: str, problem: str):
    "Run tests for a single problem."
    run_tests(category, problem)

@app.command()
def test_all():
    "Run all problems"
    run_all_tests()


if __name__ == "__main__":
    app()
