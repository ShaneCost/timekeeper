"""Context manager surface: time an arbitrary block of code."""

from __future__ import annotations

from types import TracebackType

from ._clock import DEFAULT_CLOCK, Clock
from ._models import Timing

__all__ = ["Stopwatch", "timer"]

class Stopwatch:
    """Handle bound by `timer`: live reading during the block, final after."""

    def __init__(self, label: str, clock: Clock = DEFAULT_CLOCK) -> None:
        self._label = label
        self._clock = clock
        self._start: float = 0.0
        self._timing: Timing | None = None

    def __enter__(self) -> Stopwatch:
        self._start = self._clock()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        end = self._clock()
        self._timing = Timing(
            label=self._label,
            start=self._start,
            end=end,
            ok=exc_type is None,
        )

    @property
    def elapsed(self) -> float:
        """Seconds so far (while running) or the final duration (after exit)."""
        if self._timing is not None:
            return self._timing.elapsed
        return self._clock() - self._start

    @property
    def timing(self) -> Timing | None:
        """The completed `Timing`, or None until the block exits."""
        return self._timing

def timer(label: str, *, clock: Clock = DEFAULT_CLOCK) -> Stopwatch:
    """Time a block: `with timer("label") as t: ...` then read `t.elapsed`."""
    return Stopwatch(label, clock)