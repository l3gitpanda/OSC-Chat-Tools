from ..base import ChatboxPlugin

_scroll_pos = 0


def render_marquee(context, text, data=0):
    global _scroll_pos
    width = context.get("marquee_width", 20)
    speed = context.get("marquee_speed", 1)
    result = text.replace("\\n", " ").replace("\\v", " ")

    if not result or len(result) <= width:
        _scroll_pos = 0
        return context["check_data"](result, data)

    padded = result + "   " + result
    display = padded[_scroll_pos:_scroll_pos + width]
    _scroll_pos = (_scroll_pos + speed) % (len(result) + 3)

    return context["check_data"](display, data)


plugin = ChatboxPlugin(name="marquee", render=render_marquee)
