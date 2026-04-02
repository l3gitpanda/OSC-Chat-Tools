from __future__ import annotations

from typing import Dict

from .base import ChatboxPlugin, PluginContext


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: Dict[str, ChatboxPlugin] = {}

    def register(self, plugin: ChatboxPlugin) -> None:
        self._plugins[plugin.name] = plugin

    def render(self, name: str, context: PluginContext, text: str, data: int = 0) -> str:
        plugin = self._plugins.get(name)
        if plugin is None:
            raise KeyError(f"Unknown plugin '{name}'")
        return plugin.render(context, text, data)

    def has(self, name: str) -> bool:
        return name in self._plugins
