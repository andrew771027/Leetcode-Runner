import os
from pathlib import Path


class Discovery:
    def __init__(self, bath_path: str):
        self.bath_path = Path(bath_path)

    def all_tests(self) -> list:
        """Return list of (category, Path) for test_*.py files.

        Uses os.walk with an onerror handler so permission errors are
        skipped instead of raising and terminating the run.
        """
        tests: list[tuple[str, Path]] = []

        def _onerror(err):
            # ignore permission errors while walking
            return None

        for root, dirs, files in os.walk(self.bath_path, onerror=_onerror):
            for fname in files:
                if fname.startswith("test_") and fname.endswith(".py"):
                    p = Path(root) / fname
                    tests.append((p.parent.name, p))

        return tests
