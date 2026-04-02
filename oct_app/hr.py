from __future__ import annotations

from typing import Any, Callable


def hrConnectionThread(ctx: Any, worker: Callable[[], None]) -> None:
    """Delegates to provider-specific HR socket worker and keeps state in context."""

    ctx.hrConnected = False
    worker()
