import random
import time as _time
from collections import defaultdict

from ..base import ChatboxPlugin

_DEFAULT_FORTUNES = [
    "A beautiful, smart, and loving person will be coming into your life.",
    "A dubious friend may be an enemy in camouflage.",
    "A faithful friend is a strong defense.",
    "A fresh start will put you on your way.",
    "A golden egg of opportunity falls into your lap this month.",
    "A good time to finish up old tasks.",
    "A lifetime of happiness lies ahead of you.",
    "A smile is your passport into the hearts of others.",
    "Adventure can be real happiness.",
    "All your hard work will soon pay off.",
    "Be on the alert to recognize your prime at whatever time of your life it may occur.",
    "Enjoy the good luck a companion brings you.",
    "Good news will come to you by mail.",
    "The greatest risk is not taking one.",
    "Your ability to juggle many tasks will take you far.",
]

_last_change = 0.0
_current_fortune = ""
_file_lines = None


def render_fortune(context, _text, data=0):
    global _last_change, _current_fortune, _file_lines
    display = context.get("fortune_display", "🥠 {fortune}")
    interval = context.get("fortune_interval", 60)
    fortune_file = context.get("fortune_file", "")

    now = _time.time()
    if now - _last_change >= interval or not _current_fortune:
        if fortune_file:
            if _file_lines is None:
                try:
                    with open(fortune_file, "r", encoding="utf-8") as f:
                        _file_lines = [line.strip() for line in f if line.strip()]
                except Exception:
                    _file_lines = _DEFAULT_FORTUNES
            pool = _file_lines if _file_lines else _DEFAULT_FORTUNES
        else:
            pool = _DEFAULT_FORTUNES
        _current_fortune = random.choice(pool)
        _last_change = now

    rendered = display.format_map(defaultdict(str, fortune=_current_fortune))
    return context["check_data"](rendered, data)


plugin = ChatboxPlugin(name="fortune", render=render_fortune)
