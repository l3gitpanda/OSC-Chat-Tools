from .registry import PluginRegistry


def create_default_registry() -> PluginRegistry:
    # Import plugins lazily so module import doesn't load all plugin deps
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
    from .builtin.textstyle import plugin as textstyle_plugin
    from .builtin.fliptext import plugin as fliptext_plugin
    from .builtin.zalgo import plugin as zalgo_plugin
    from .builtin.kaomoji import plugin as kaomoji_plugin
    from .builtin.sparkle import plugin as sparkle_plugin
    from .builtin.eightball import plugin as eightball_plugin
    from .builtin.dice import plugin as dice_plugin
    from .builtin.fortune import plugin as fortune_plugin
    from .builtin.typewriter import plugin as typewriter_plugin
    from .builtin.cycler import plugin as cycler_plugin
    from .builtin.reaction import plugin as reaction_plugin
    from .builtin.marquee import plugin as marquee_plugin
    from .builtin.textalign import plugin as textalign_plugin
    from .builtin.smarttruncate import plugin as smarttruncate_plugin
    from .builtin.animate import plugin as animate_plugin

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
        textstyle_plugin,
        fliptext_plugin,
        zalgo_plugin,
        kaomoji_plugin,
        sparkle_plugin,
        eightball_plugin,
        dice_plugin,
        fortune_plugin,
        typewriter_plugin,
        cycler_plugin,
        reaction_plugin,
        marquee_plugin,
        textalign_plugin,
        smarttruncate_plugin,
        animate_plugin,
    ):
        registry.register(plugin)
    return registry
