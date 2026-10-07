"""Decorator surface: time every call to a function."""

from __future__ import annotations

from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from ._clock import DEFAULT_CLOCK, Clock
from ._models import Timing

__all__ = ["timed", "timings", "clear_timings"]

P = ParamSpec("P")
R = TypeVar("R")

Sink = Callable[[Timing], None]

_registry: list[Timing] = []

def timings() -> tuple[Timing, ...]:
    """Every Timing recorded via the default sink, oldest first."""
    return tuple(_registry)

def clear_timings() -> None:
    """Empty the default registry."""
    _registry.clear()

def timed(
    label: str | None = None,
    *,
    sink: Sink | None = None,
    clock: Clock = DEFAULT_CLOCK,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorate a function so each call records a `Timing`.

    With no `sink`, timings collect in the registry (read via `timings()`).
    `label` defaults to the function's qualified name.
    """
    record: Sink = sink if sink is not None else _registry.append

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        name = label if label is not None else func.__qualname__

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = clock()
            ok = True
            try:
                return func(*args, **kwargs)
            except BaseException:
                ok = False
                raise
            finally:
                end = clock()
                record(Timing(label=name, start=start, end=end, ok=ok))

        return wrapper

    return decorator