from collections import defaultdict

from ..base import ChatboxPlugin


def render_playtime(context, _text, data=0):
    try:
        minutes = int((context["time_var"] - context["play_time_dat"]) / 60)
        hours, remainder_minutes = divmod(minutes, 60)
        if context["vrc_pid"] is None:
            minutes = 0
            hours = 0
            remainder_minutes = 0
    except Exception:
        minutes = 0
        hours = 0
        remainder_minutes = 0

    play_data = context["play_time_display"].format_map(
        defaultdict(
            str,
            hours="{:02d}".format(hours),
            remainder_minutes="{:02d}".format(remainder_minutes),
            minutes="{:02d}".format(minutes),
        )
    )
    return context["check_data"](play_data, data)


plugin = ChatboxPlugin(name="playtime", render=render_playtime)
