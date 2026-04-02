from collections import defaultdict
from datetime import datetime

from ..base import ChatboxPlugin


def render_time(context, _text, data=0):
    now = datetime.now()
    hour24 = now.strftime("%H")
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    time_zone = datetime.now().astimezone().tzname()
    if time_zone == 'Central Daylight Time':
        time_zone = 'CDT'

    if int(hour) >= 12:
        hour = int(hour) - 12
        if int(hour) == 0:
            hour = 12
        rendered = context["time_display_pm"].format_map(
            defaultdict(str, hour=hour, minute=minute, time_zone=time_zone, hour24=hour24)
        )
    else:
        if int(hour) == 0:
            hour = 12
        rendered = context["time_display_am"].format_map(
            defaultdict(str, hour=hour, minute=minute, time_zone=time_zone, hour24=hour24)
        )
    return context["check_data"](rendered, data)


plugin = ChatboxPlugin(name="time", render=render_time)
