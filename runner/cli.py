import typer

from runner.aggregator import Aggregator
from runner.backends import SubprocessBackend
from runner.core import Runner
from runner.discovery import Discovery
from runner.models import TestResult
from runner.report import Reporter

BASE_PATH = "/Users/poyuan/Desktop/andrew771027/LeetCode/tests"

app = typer.Typer()
backend = SubprocessBackend()
discovery = Discovery(BASE_PATH)
runner = Runner(BASE_PATH, backend, discovery)
agg = Aggregator()

reporter = Reporter()


@app.command()
def test(category: str, problem: str):
    "Run tests for a single problem."
    results: TestResult = runner.run_test(category, problem)

    Reporter.print([results])
    Reporter.to_json([results])


@app.command()
def test_all():
    "Run all problems"
    results = runner.run_all_tests()
    ranked = agg.rank(results)
    summary = agg.summary(results)
    reporter.print_rank(ranked)

    print("\n📊 Summary")
    print(summary)


if __name__ == "__main__":
    app()
