import random
import time as _time
from collections import defaultdict

from ..base import ChatboxPlugin

_RESPONSES = [
    "It is certain", "It is decidedly so", "Without a doubt",
    "Yes definitely", "You may rely on it", "As I see it, yes",
    "Most likely", "Outlook good", "Yes", "Signs point to yes",
    "Reply hazy, try again", "Ask again later",
    "Better not tell you now", "Cannot predict now",
    "Concentrate and ask again", "Don't count on it",
    "My reply is no", "My sources say no",
    "Outlook not so good", "Very doubtful",
]

_last_change = 0.0
_current_response = ""


def render_eightball(context, _text, data=0):
    global _last_change, _current_response
    display = context.get("eightball_display", "🎱 {response}")
    interval = context.get("eightball_interval", 30)

    now = _time.time()
    if now - _last_change >= interval or not _current_response:
        _current_response = random.choice(_RESPONSES)
        _last_change = now

    rendered = display.format_map(defaultdict(str, response=_current_response))
    return context["check_data"](rendered, data)


plugin = ChatboxPlugin(name="8ball", render=render_eightball)
