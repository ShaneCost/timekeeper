"""Data model: immutable records produced by every timing surface."""

from __future__ import annotations

from dataclasses import dataclass, field

__all__ = ["Timing", "LapReport"]

@dataclass(frozen=True, slots=True)
class Timing:
    """A single completed measurement.

    `ok` is False when the timed work raises exception; `elapsed` is still valid.
    """

    label: str
    start: float
    end: float
    ok: bool = True

    @property
    def elapsed(self) -> float:
        """Seconds between start and end."""
        return self.end - self.start

    def __str__(self) -> str:
        """Human-readable one-line summary."""
        status = "" if self.ok else " (failed)"
        return f"{self.label}: {self.elapsed:.6f}s{status}"


@dataclass(frozen=True, slots=True)
class LapReport:
    """Aggregate of the per-item timings collected while iterating."""

    timings: tuple[Timing, ...] = field(default_factory=tuple)

    @property
    def total(self) -> float:
        """Sum of every item's elapsed time."""
        return sum(t.elapsed for t in self.timings)

    @property
    def mean(self) -> float:
        """Average elapsed time per item, or 0.0 when empty."""
        return self.total / len(self.timings) if self.timings else 0.0

    @property
    def slowest(self) -> Timing | None:
        """The single longest-running item, or None when empty."""
        return max(self.timings, key=lambda t: t.elapsed, default=None)

    def __str__(self) -> str:
        """Human-readable multi-line summary of the whole report."""
        if not self.timings:
            return "LapReport: no items timed"

        lines = [f"LapReport: {len(self.timings)} items"]
        for t in self.timings:
            lines.append(f"  {t.label}: {t.elapsed:.6f}s")
        lines.append(f"  total:   {self.total:.6f}s")
        lines.append(f"  mean:    {self.mean:.6f}s")
        slowest = self.slowest
        if slowest is not None:
            lines.append(f"  slowest: {slowest.label} ({slowest.elapsed:.6f}s)")
        return "\n".join(lines)