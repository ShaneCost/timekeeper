# timekeeper

Measure elapsed time three ways — a **decorator**, a **context manager**, and a
**generator**. Fully type-annotated, no runtime dependencies, Python 3.10+.

All three read time through a pluggable `Clock` (default `time.perf_counter`)
and produce immutable `Timing` records; `lap` aggregates them into a `LapReport`.

## Setup

From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .          # add ".[dev]" for mypy + ruff
```

## Demo

```bash
python demo.py
```

Runs all three surfaces, including the failure cases and the empty-iterable case.

## Usage

```python
from timekeeper import timed, timer, lap, timings, clear_timings
```

### `@timed` — decorator

Times every function call. With no `sink`, timings collect in a registry you read with
`timings()`; pass a `sink` to route them elsewhere. Signature-preserving, and a
call that raises an exception is still recorded (`ok=False`).

```python
@timed() # label defaults to the function name
def load(path: str) -> bytes: ...

@timed(label="fetch", sink=lambda t: print(f"{t.label}: {t.elapsed:.3f}s"))
def fetch(url: str) -> bytes: ...

load("data.bin")
for t in timings():
    print(t)
clear_timings()
```

### `timer` — context manager

Times a block of code. The handle reads *live* while the block runs and *final* after.
A block that raises an exception still records (`ok=False`), then re-raises.

```python
with timer(label="db-load") as t:
    rows = load()
    print(t.elapsed)        # live
print(t.elapsed)            # final
print(t.timing)             # completed Timing record
```

### `lap` — generator

Wraps an iterable, yielding items unchanged while timing each iteration. Read `.report`
after iterating; an empty iterable is handled gracefully.

```python
laps = lap(dataset, label="process")
for item in laps:
    process(item)
print(laps.report)          # per-item, total, mean, slowest
```

## Public API

| Name | Purpose |
| --- | --- |
| `timed`, `timer`, `lap` | the three timing surfaces |
| `Timing`, `LapReport` | immutable result records |
| `Clock`, `DEFAULT_CLOCK` | the clock protocol and its default |
| `Stopwatch`, `LapTimer` | handles returned by `timer` / `lap` |
| `timings`, `clear_timings` | read / reset the default-sink registry |
