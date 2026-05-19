import time


class Benchmark:
    def measure(self, func, *args, repeat=3):
        results = []
        durations = []

        for _ in range(repeat):
            start = time.perf_counter()
            result = func(*args)
            durations.append(time.perf_counter() - start)
            results.append(result)

        min_idx = durations.index(min(durations))
        return results[min_idx], min(durations)
