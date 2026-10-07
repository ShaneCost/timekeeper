"""Generator surface: time each item as you iterate."""

from __future__ import annotations

from typing import Generic, Iterable, Iterator, TypeVar

from ._clock import DEFAULT_CLOCK, Clock
from ._models import LapReport, Timing

__all__ = ["LapTimer", "lap"]

T = TypeVar("T")

class LapTimer(Generic[T]):
    """Iterable handle: yields items unchanged, records a Timing per item.

    Read `report` after iterating for the aggregated per-item timings.
    """

    def __init__(
        self,
        iterable: Iterable[T],
        label: str = "lap",
        *,
        clock: Clock = DEFAULT_CLOCK,
    ) -> None:
        self._iterable = iterable
        self._label = label
        self._clock = clock
        self._timings: list[Timing] = []

    def __iter__(self) -> Iterator[T]:
        self._timings = []
        clock = self._clock
        for index, item in enumerate(self._iterable):
            start = clock()
            yield item
            end = clock()
            self._timings.append(
                Timing(label=f"{self._label}[{index}]", start=start, end=end)
            )

    @property
    def report(self) -> LapReport:
        """Aggregate of the timings from the most recent iteration."""
        return LapReport(tuple(self._timings))

def lap(
    iterable: Iterable[T],
    label: str = "lap",
    *,
    clock: Clock = DEFAULT_CLOCK,
) -> LapTimer[T]:
    """Wrap an iterable to time each item: iterate, then read `.report`."""
    return LapTimer(iterable, label, clock=clock)