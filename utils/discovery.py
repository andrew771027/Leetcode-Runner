import os
from pathlib import Path


class Discovery:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def find_all(self) -> list:
        """Return list of (category, Path) for test_*.py files.

        Uses os.walk with an onerror handler so permission errors are
        skipped instead of raising and terminating the run.
        """
        tests: list[tuple[str, Path]] = []

        def _onerror(err):
            # ignore permission errors while walking
            return None

        for root, dirs, files in os.walk(self.base_path, onerror=_onerror):
            for fname in files:
                if fname.startswith("test_") and fname.endswith(".py"):
                    p = Path(root) / fname
                    tests.append((p.parent.name, p))

        return tests
