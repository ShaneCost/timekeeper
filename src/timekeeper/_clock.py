"""Clock abstraction: the single seam through which the library reads time."""

from time import perf_counter
from typing import Protocol

__all__ = ["Clock", "DEFAULT_CLOCK"]

class Clock(Protocol):
    """Any zero-argument callable returning seconds as a float."""

    def __call__(self) -> float:
        """Return the current time, in seconds."""
        ...

# Default clock: monotonic and high-resolution, ideal for measuring durations.
DEFAULT_CLOCK: Clock = perf_counter