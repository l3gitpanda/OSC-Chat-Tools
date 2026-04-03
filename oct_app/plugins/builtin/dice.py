import random
import time as _time
from collections import defaultdict

from ..base import ChatboxPlugin

_last_roll_time = 0.0
_current_result = ""


def render_dice(context, _text, data=0):
    global _last_roll_time, _current_result
    display = context.get("dice_display", "🎲 {result}")
    sides = context.get("dice_sides", 6)
    count = context.get("dice_count", 1)
    interval = context.get("dice_interval", 30)

    now = _time.time()
    if now - _last_roll_time >= interval or not _current_result:
        rolls = [random.randint(1, sides) for _ in range(count)]
        total = sum(rolls)
        if count == 1:
            result_str = str(total)
        else:
            result_str = "+".join(str(r) for r in rolls) + f"={total}"
        _current_result = result_str
        _last_roll_time = now

    rendered = display.format_map(defaultdict(str, result=_current_result))
    return context["check_data"](rendered, data)


plugin = ChatboxPlugin(name="dice", render=render_dice)
