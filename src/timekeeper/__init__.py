"""timekeeper: measure elapsed time through three surfaces.

- `timed`   -- decorator, times every call to a function
- `timer`   -- context manager, times an arbitrary block
- `lap`     -- generator, times each item as you iterate

All three read time through a `Clock` (default: `perf_counter`) and
produce `Timing` records; `lap` aggregates them into a `LapReport`.
"""

from ._clock import DEFAULT_CLOCK, Clock
from ._lap import LapTimer, lap
from ._models import LapReport, Timing
from ._timed import clear_timings, timed, timings
from ._timer import Stopwatch, timer

__all__ = [
    # surfaces
    "timed",
    "timer",
    "lap",

    # data model
    "Timing",
    "LapReport",

    # clock seam
    "Clock",
    "DEFAULT_CLOCK",

    # handles (for type annotations / advanced use)
    "Stopwatch",
    "LapTimer",

    # default-sink registry helpers
    "timings",
    "clear_timings",
]