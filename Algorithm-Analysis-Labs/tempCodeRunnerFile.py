import csv
import math
import platform
import statistics
import sys
import timeit
from pathlib import Path

import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
TRIALS = 7


def prefix_average1(a):
    avg = []

    for j in range(len(a)):
        total = 0

        for i in range(j + 1):
            total += a[i]

        avg.append(total / (j + 1))

    return avg


def prefix_average2(a):
    avg = []
    total = 0

    for i in range(len(a)):
        total += a[i]
        avg.append(total / (i + 1))

    return avg


def same_output(a, b):
    if len(a) != len(b):
        return False

    return all(
        math.isclose(x, y, rel_tol=1e-9, abs_tol=1e-9)
        for x, y in zip(a, b)
    )


def measure(fn, number):
    times = timeit.repeat(fn, repeat=TRIALS, number=number)
    return statistics.median(times) / number


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    tests = [
        ("Empty", []),
        ("Singleton", [8]),
        ("Positive", [2, 4, 6, 8]),
        ("Negative", [-2, -4, -6, -8]),
        ("Mixed", [5, -3, 7, -2, 4])
    ]

    print("LAB WORK 2: PREFIX AVERAGES")
    print("Python version:", sys.version.split()[0])
    print("Platform:", platform.platform())
    print("Checking that both methods return equivalent results:\n")

    for name, a in tests:
        x = prefix_average1(a)
        y = prefix_average2(a)
        assert same_output(x, y), f"Output mismatch for {name} input"
        print(f"{name:<12} Input: {a}  Prefix averages: {y}")

    sizes = [100, 250, 500, 1000, 2000, 3000, 4000]
    rows = []

    for n in sizes:
        a = [((i * 17) % 101) - 50 for i in range(n)]

        t1 = measure(lambda a=a: prefix_average1(a), 1)
        t2 = measure(lambda a=a: prefix_average2(a), 100)

        rows.append({
            "n": n,
            "prefix_average1_seconds": t1,
            "prefix_average2_seconds": t2,
            "prefix_average1_normalized_us": (t1 / (n ** 2)) * 1_000_000,
            "prefix_average2_normalized_us": (t2 / n) * 1_000_000,
            "speedup": t1 / t2
        })

    csv_path = RESULTS_DIR / "lab2_timing.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("\nBenchmark results")
    print("Input generation is outside the timed region.")
    print(f"Each measurement uses the median of {TRIALS} trials.\n")
    print(
        f"{'n':>7} {'Method 1 (ms)':>18} {'Method 2 (ms)':>18} "
        f"{'T1/n^2 (us)':>16} {'T2/n (us)':>14} {'Speedup':>11}"
    )
    print("-" * 91)

    for row in rows:
        print(
            f"{row['n']:>7} "
            f"{row['prefix_average1_seconds'] * 1000:>18.6f} "
            f"{row['prefix_average2_seconds'] * 1000:>18.6f} "
            f"{row['prefix_average1_normalized_us']:>16.6f} "
            f"{row['prefix_average2_normalized_us']:>14.6f} "
            f"{row['speedup']:>10.2f}x"
        )

    plt.figure(figsize=(9, 6))
    plt.plot(
        sizes,
        [row["prefix_average1_seconds"] for row in rows],
        marker="o",
        label="Prefix Average 1 - O(n^2)"
    )
    plt.plot(
        sizes,
        [row["prefix_average2_seconds"] for row in rows],
        marker="o",
        label="Prefix Average 2 - O(n)"
    )
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Sequence length (n)")
    plt.ylabel("Execution time (seconds)")
    plt.title("Prefix Average: Quadratic vs Linear Time")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "lab2_prefix_averages.png", dpi=300)
    plt.show()

    print(f"\nTiming data saved to: {csv_path}")
    print(f"Plot saved in: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
