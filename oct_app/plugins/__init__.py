from .registry import PluginRegistry
from .builtin.cpu import plugin as cpu_plugin
from .builtin.divider import plugin as divider_plugin
from .builtin.gpu import plugin as gpu_plugin
from .builtin.hr import plugin as hr_plugin
from .builtin.mute import plugin as mute_plugin
from .builtin.playtime import plugin as playtime_plugin
from .builtin.ram import plugin as ram_plugin
from .builtin.song import plugin as song_plugin
from .builtin.stt import plugin as stt_plugin
from .builtin.text import plugin as text_plugin
from .builtin.time import plugin as time_plugin
from .builtin.timer import plugin as timer_plugin


def create_default_registry() -> PluginRegistry:
    registry = PluginRegistry()
    for plugin in (
        text_plugin,
        time_plugin,
        timer_plugin,
        song_plugin,
        cpu_plugin,
        ram_plugin,
        gpu_plugin,
        hr_plugin,
        stt_plugin,
        divider_plugin,
        mute_plugin,
        playtime_plugin,
    ):
        registry.register(plugin)
    return registry
