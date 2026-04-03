from ..base import ChatboxPlugin

_char_index = 0


def render_typewriter(context, text, data=0):
    global _char_index
    speed = context.get("typewriter_speed", 2)
    result = text.replace("\\n", "\v").replace("\\v", "\v")

    if not result:
        _char_index = 0
        return context["check_data"]("", data)

    _char_index = min(_char_index + speed, len(result))
    displayed = result[:_char_index]

    if _char_index >= len(result):
        _char_index = 0

    return context["check_data"](displayed, data)


plugin = ChatboxPlugin(name="typewriter", render=render_typewriter)
