from __future__ import annotations

from typing import Callable


def uiThread(builder: Callable[[], None]) -> None:
    """FreeSimpleGUI construction + event loop callback entrypoint."""

    builder()
