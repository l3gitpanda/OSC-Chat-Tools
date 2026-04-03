from collections import defaultdict

from ..base import ChatboxPlugin

_reaction_count = 0


def get_count():
    return _reaction_count


def increment():
    global _reaction_count
    _reaction_count += 1
    return _reaction_count


def reset():
    global _reaction_count
    _reaction_count = 0


def render_reaction(context, _text, data=0):
    global _reaction_count
    display = context.get("reaction_display", "💜 {label}: {count}")
    label = context.get("reaction_label", "Headpats")
    rendered = display.format_map(defaultdict(str, count=str(_reaction_count), label=label))
    return context["check_data"](rendered, data)


plugin = ChatboxPlugin(name="reaction", render=render_reaction)
