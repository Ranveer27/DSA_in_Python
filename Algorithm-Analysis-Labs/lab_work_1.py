import csv
import math
import platform
import random
import statistics
import sys
import timeit
from pathlib import Path

import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
TRIALS = 7
SEED = 42


def list_index(a):
    return a[len(a) // 2]


def binary_search(a, target):
    low = 0
    high = len(a) - 1

    while low <= high:
        mid = (low + high) // 2

        if a[mid] == target:
            return mid
        if a[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def linear_search(a, target):
    for i in range(len(a)):
        if a[i] == target:
            return i
    return -1


def merge(a, b):
    c = []
    i = 0
    j = 0

    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1

    c.extend(a[i:])
    c.extend(b[j:])
    return c


def merge_sort(a):
    if len(a) <= 1:
        return a

    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    return merge(left, right)


def pair_counter(a):
    count = 0

    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            count += 1

    return count


def subset_enumeration(n):
    count = 0

    for _ in range(1 << n):
        count += 1

    return count


def measure(fn, number):
    times = timeit.repeat(fn, repeat=TRIALS, number=number)
    return statistics.median(times) / number


def growth_value(name, n):
    if name == "List indexing":
        return 1
    if name == "Binary search":
        return math.log2(n)
    if name == "Linear search":
        return n
    if name == "Merge sort":
        return n * math.log2(n)
    if name == "Pair counter":
        return n ** 2
    return 2 ** n


def benchmark(name, sizes, input_fn, algorithm, target_fn, number, complexity, notes):
    rows = []

    for n in sizes:
        data = input_fn(n)
        target = target_fn(data, n)
        elapsed = measure(lambda: algorithm(data, target), number)
        normal = elapsed / growth_value(name, n)

        rows.append({
            "algorithm": name,
            "complexity": complexity,
            "n": n,
            "time_seconds": elapsed,
            "time_milliseconds": elapsed * 1000,
            "normalized_microseconds": normal * 1_000_000,
            "input_characteristics": notes
        })

    return rows


def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    rng = random.Random(SEED)

    assert list_index([4, 7, 9]) == 7
    assert binary_search([1, 3, 5, 7], 5) == 2
    assert binary_search([1, 3, 5, 7], 8) == -1
    assert linear_search([1, 3, 5, 7], 7) == 3
    assert linear_search([1, 3, 5, 7], 8) == -1
    assert merge_sort([5, 2, 8, 1, 3]) == [1, 2, 3, 5, 8]
    assert pair_counter([1, 2, 3, 4]) == 6
    assert subset_enumeration(4) == 16

    data = []

    data += benchmark(
        "List indexing",
        [1000, 5000, 10000, 50000, 100000, 200000],
        lambda n: list(range(n)),
        lambda a, target: list_index(a),
        lambda a, n: None,
        10000,
        "O(1)",
        "Integer list; access the middle element repeatedly"
    )

    data += benchmark(
        "Binary search",
        [128, 512, 2048, 8192, 32768, 131072],
        lambda n: list(range(n)),
        binary_search,
        lambda a, n: n,
        1000,
        "O(log n)",
        "Sorted integer list; absent target above the largest value"
    )

    data += benchmark(
        "Linear search",
        [100, 500, 1000, 2000, 4000, 8000, 16000],
        lambda n: list(range(n)),
        linear_search,
        lambda a, n: n,
        1,
        "O(n)",
        "Integer list; absent target forces a full scan"
    )

    data += benchmark(
        "Merge sort",
        [128, 256, 512, 1024, 2048, 4096, 8192],
        lambda n: rng.sample(range(n * 10), n),
        lambda a, target: merge_sort(a),
        lambda a, n: None,
        1,
        "O(n log n)",
        "Deterministically shuffled integer list; sorting does not modify input"
    )

    data += benchmark(
        "Pair counter",
        [100, 200, 400, 800, 1200, 1600],
        lambda n: list(range(n)),
        lambda a, target: pair_counter(a),
        lambda a, n: None,
        1,
        "O(n^2)",
        "Integer list; count all index pairs with i less than j"
    )

    data += benchmark(
        "Subset enumeration",
        [4, 6, 8, 10, 12, 14, 16, 18, 20],
        lambda n: n,
        lambda n, target: subset_enumeration(n),
        lambda n, size: None,
        1,
        "O(2^n)",
        "Enumerate all bitmasks; n is restricted to at most 20"
    )

    csv_path = RESULTS_DIR / "lab1_timing.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print("LAB WORK 1: BENCHMARKING ALGORITHMIC GROWTH RATES")
    print("Python version:", sys.version.split()[0])
    print("Platform:", platform.platform())
    print(f"Python trials per measurement: {TRIALS}")
    print("Reported time is the median time per algorithm call.")
    print("Input generation is outside the timed region.\n")
    print(f"{'Algorithm':<21} {'Complexity':<12} {'n':>8} {'Time (ms)':>14} {'T(n)/g(n) (us)':>19}")
    print("-" * 78)

    for row in data:
        print(
            f"{row['algorithm']:<21} {row['complexity']:<12} "
            f"{row['n']:>8} {row['time_milliseconds']:>14.6f} "
            f"{row['normalized_microseconds']:>19.6f}"
        )

    plt.figure(figsize=(10, 6))
    for name in dict.fromkeys(row["algorithm"] for row in data):
        rows = [row for row in data if row["algorithm"] == name]
        sizes = [row["n"] for row in rows]
        times = [row["time_seconds"] for row in rows]
        plt.plot(sizes, times, marker="o", label=name)

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Input size (n)")
    plt.ylabel("Execution time (seconds)")
    plt.title("Benchmarking Algorithmic Growth Rates")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "lab1_growth_rates.png", dpi=300)
    plt.show()

    plt.figure(figsize=(10, 6))
    for name in dict.fromkeys(row["algorithm"] for row in data):
        rows = [row for row in data if row["algorithm"] == name]
        sizes = [row["n"] for row in rows]
        values = [row["normalized_microseconds"] for row in rows]
        plt.plot(sizes, values, marker="o", label=name)

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Input size (n)")
    plt.ylabel("Normalized time (microseconds)")
    plt.title("Measured Time Divided by Theoretical Growth Function")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "lab1_normalized_times.png", dpi=300)
    plt.show()

    print(f"\nTiming data saved to: {csv_path}")
    print(f"Plots saved in: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
