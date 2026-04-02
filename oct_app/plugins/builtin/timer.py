from collections import defaultdict
from datetime import datetime

from ..base import ChatboxPlugin


def render_timer(context, _text, data=0):
    current_time = int(datetime.now().timestamp() * 1000)
    timer_var = context["timer_end_stamp"] - current_time
    if timer_var < 0:
        timer_var = 0
        context["timer_end_stamp"] = int(datetime.now().timestamp() * 1000)
    hours, remainder = divmod(timer_var // 1000, 3600)
    minutes, seconds = divmod(remainder, 60)
    context["timer_var"] = timer_var
    formatted = context["timer_display"].format_map(
        defaultdict(str, hours=f"{hours:02}", minutes=f"{minutes:02}", seconds=f"{seconds:02}")
    )
    return context["check_data"](formatted, data)


plugin = ChatboxPlugin(name="timer", render=render_timer)
