from __future__ import annotations

from typing import Callable


def oscListenServerManager(manager: Callable[[], None]) -> None:
    manager()


def oscForwardingManager(manager: Callable[[], None]) -> None:
    manager()
