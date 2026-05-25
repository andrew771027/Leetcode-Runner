from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, List


class ParallelExecutor:

    def run(self, func: Callable, items: List[Any], max_workers: int = 4):
        results = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(func, item) for item in items]

            for future in as_completed(futures):
                results.append(future.result())

        return results
