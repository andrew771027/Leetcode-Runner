import typer

from runner.aggregator import Aggregator
from runner.analytics import Analytics
from runner.backends import SubprocessBackend
from runner.core import Runner
from runner.discovery import Discovery
from runner.logger import EventLogger
from runner.models import TestResult
from runner.report import Reporter

BASE_PATH = "/Users/poyuan/Desktop/andrew771027/LeetCode/tests"

app = typer.Typer()
backend = SubprocessBackend()
discovery = Discovery(BASE_PATH)
logger = EventLogger()
analytics = Analytics()
runner = Runner(
    base_path=BASE_PATH, backend=backend, discovery=discovery, logger=logger, analytics=analytics
)
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
    analytics = runner.analyze(results)

    print("\n📊 Summary")
    print(summary)

    print("\n📊 Analytics")
    print(analytics)


if __name__ == "__main__":
    app()
