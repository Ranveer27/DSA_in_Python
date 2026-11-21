  # Algorithm Analysis Labs

This repository contains Python implementations and empirical benchmarks for two laboratory exercises:

1. Benchmarking constant, logarithmic, linear, n-log-n, quadratic and exponential algorithms.
2. Comparing quadratic and linear-time prefix-average algorithms.

## Requirements

- Python 3.8 or newer
- `matplotlib`
- Standard Python libraries (`csv`, `math`, `random`, `statistics`, `timeit`, and `pathlib`)

The Python version and operating system used for your final report should be recorded from the machine on which you run the experiments.

## Setup in Visual Studio Code

Open this repository folder in VS Code. Open **Terminal > New Terminal** and create a virtual environment.

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Ubuntu / Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

In VS Code, select the interpreter inside `.venv` using **Python: Select Interpreter** from the Command Palette.

## Run the experiments

Run each program from the repository root:

```bash
python lab_work_1.py
python lab_work_2.py
```

On systems where the Python 3 command is `python3`, use `python3` instead.

Each program prints timing results and saves CSV data and plots in the `results/` directory. Run the programs on the computer used for your report because execution times depend on the processor, operating system, Python build and background activity.

## Experimental method

- Each timing is the median of seven trials.
- Input data is generated before the timed function is called.
- The list-indexing and binary-search operations are repeated within each trial to make their short execution times easier to measure.
- Linear search uses a target that is not present, so it scans the complete list.
- Binary search uses sorted input and an absent target above the largest value.
- Merge sort receives deterministic shuffled input generated with seed 42.
- Pair counting uses two nested loops.
- Subset enumeration is limited to `n <= 20` to keep the experiment manageable.
- Prefix-average benchmarks use deterministic input sequences. The two methods are checked on empty, singleton, positive, negative and mixed-value inputs before timing.

## Expected theoretical complexity

| Algorithm | Expected time complexity |
|---|---|
| List indexing | O(1) |
| Binary search | O(log n) |
| Linear search | O(n) |
| Merge sort | O(n log n) |
| Pair counter | O(n^2) |
| Subset enumeration | O(2^n) |
| Prefix average 1 | O(n^2) |
| Prefix average 2 | O(n) |

## Prefix-average operation counts

For an input of length `n`, the nested-loop implementation performs

`1 + 2 + ... + n = n(n + 1) / 2`

additions to compute the prefix sums. Its time complexity is therefore O(n^2).

The running-sum implementation performs one running-sum addition for each element, or `n` additions, so its time complexity is O(n). Both implementations also calculate `n` averages and append `n` results.

## Notes for the report

Record the Python version and platform printed by your own run. Use the generated CSV files and plots as the experimental results. Timing measurements are affected by interpreter overhead, processor state, background processes, memory allocation and input size. Normalized timing values help inspect the expected growth pattern, but they are not expected to be perfectly constant.


## Interpreting the results

The list-indexing measurements should remain approximately constant as `n` grows. Binary search should increase slowly, while linear search should increase in proportion to the input length. Merge sort is expected to follow an `n log n` trend. The pair counter should rise quadratically, and subset enumeration should rise very quickly as `n` increases.

The normalized values divide each measured time by its corresponding theoretical growth function: `1`, `log2(n)`, `n`, `n log2(n)`, `n^2` or `2^n`. A roughly stable normalized value is consistent with the expected growth class, but measurements will not be perfectly constant. Fixed costs, lower-order terms, Python interpreter overhead, memory allocation, processor scheduling and cache effects all influence the results.

For the prefix-average comparison, the first method repeats the addition of earlier elements for every prefix. The second method keeps the previous running sum and adds only the next value. Both produce the same mathematical averages, although floating-point arithmetic can introduce tiny representation differences; the validation therefore uses a tolerance rather than exact equality. The speedup column reports the measured ratio of the first method's time to the second method's time. The point at which the faster method becomes measurably faster depends on the machine and Python environment, so use your own timing output rather than assuming a fixed threshold.
