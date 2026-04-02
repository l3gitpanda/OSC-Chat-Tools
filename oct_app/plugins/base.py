from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, MutableMapping


PluginContext = MutableMapping[str, object]
PluginRenderer = Callable[[PluginContext, str, int], str]


@dataclass(frozen=True)
class ChatboxPlugin:
    """Single layout token plugin."""

    name: str
    render: PluginRenderer
