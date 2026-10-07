"""Runnable demo of timekeeper's three surfaces.

Run from the repo root (with the package installed) via:  python demo.py
"""
import time
from timekeeper import (
    timed,
    timer,
    lap,
    timings,
    clear_timings,
)

# --------------------------------------------------------------------------
# Surface 1: the decorator  (@timed)
# --------------------------------------------------------------------------
def demo_decorator() -> None:
    # --- default sink: timings collect in the registry ---
    @timed(label="slow_add")
    def slow_add(a: int, b: int, sleep_time: float = 0.1) -> int:
        time.sleep(sleep_time)
        return a + b

    @timed(label="slow_div")
    def slow_div(a: int, b: int) -> float:
        time.sleep(0.05)
        return a / b

    # --- custom sink: route the timing to a print function ---
    @timed(label="greet", sink=lambda t: print(f"{t.label} ran in {t.elapsed:.3f}s"))
    def greet(name: str) -> str:
        time.sleep(0.05)
        return f"hello, {name}"

    # --- default sink: call functions, then read back the registry ---
    clear_timings()
    slow_add(a=1, b=2) # default sleep_time
    slow_add(a=3, b=4, sleep_time=1.0) # longer sleep_time -> larger elapsed

    try:
        slow_div(a=50, b=0) # fails mid-call; still recorded, ok=False
    except ZeroDivisionError:
        pass # swallow it here; the timing survived

    for t in timings(): # iterate the default sink registry
        print(t) # uses Timing.__str__

    print("-" * 40)

    # --- custom sink: timing is routed to the lambda, not the registry ---
    greet(name="Shane")

    clear_timings() # reset the shared registry

# --------------------------------------------------------------------------
# Surface 2: the context manager  (timer)
# --------------------------------------------------------------------------
def demo_context_manager() -> None:
    # --- live vs. final: read elapsed repeatedly to show it growing, then frozen ---
    with timer(label="context_manager") as t:
        time.sleep(0.15)
        print(f"live elapsed (midway):  {t.elapsed:.3f}s")
        time.sleep(0.15)
        print(f"live elapsed (later):   {t.elapsed:.3f}s")
        time.sleep(0.15)
    print(f"final elapsed (after):  {t.elapsed:.3f}s")
    print(f"final elapsed (again):  {t.elapsed:.3f}s")   # unchanged on re-read

    # --- the completed Timing handle, with it's ok flag ---
    print("-" * 40)
    print(t.timing) # uses Timing.__str__
    print(f"ok={t.timing.ok}")

    print("-" * 40)

    # --- failure case: a block that raises still records, with ok=False ---
    try:
        with timer(label="will_fail") as t_fail:
            time.sleep(0.1)
            raise ValueError("boom") # something goes wrong mid-block
    except ValueError:
        pass # swallow it here; the timing survived

    print(t_fail.timing) # recorded despite the exception
    print(f"ok={t_fail.timing.ok}") # -> False

# --------------------------------------------------------------------------
# Surface 3: the generator  (lap)
# --------------------------------------------------------------------------
def demo_generator() -> None:
    # --- wrap an iterable: each item is timed as the loop body processes it ---
    dataset = [1, 2, 3, 4, 5]
    laps = lap(iterable=dataset, label="process")

    for n in laps: # iterate as normal; timing is automatic
        time.sleep(0.02 * n) # work that grows per item -> varied timings
        print(f"processed {n}")

    print("-" * 40)

    # --- read the aggregate after iterating ---
    print(laps.report) # uses LapReport.__str__
    print("-" * 40)

    # --- the report's accessors are also available individually ---
    report = laps.report
    print(f"items:   {len(report.timings)}")
    print(f"total:   {report.total:.3f}s")
    print(f"mean:    {report.mean:.3f}s")
    if report.slowest is not None:
        print(f"slowest: {report.slowest.label} ({report.slowest.elapsed:.3f}s)")

    print("-" * 40)

    # --- empty iterable: the report handles it without blowing up ---
    empty = lap([], label="nothing")
    for _ in empty: # loop body never runs
        pass
    print(empty.report) # -> "LapReport: no items timed"

def main() -> None:

    def header(title: str) -> None:
        print("\n" + "=" * 50)
        print(f"  {title}")
        print("=" * 50)

    header("Surface 1: the decorator  (@timed)")
    demo_decorator()

    header("Surface 2: the context manager  (timer)")
    demo_context_manager()

    header("Surface 3: the generator  (lap)")
    demo_generator()

if __name__ == "__main__":
    main()