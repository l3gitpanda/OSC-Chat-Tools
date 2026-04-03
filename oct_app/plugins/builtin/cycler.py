from ..base import ChatboxPlugin

_tick_counter = 0
_message_index = 0


def render_cycler(context, _text, data=0):
    global _tick_counter, _message_index
    messages_str = context.get("cycler_messages", "")
    interval = context.get("cycler_interval", 5)

    if not messages_str:
        return ""

    messages = [m.strip() for m in messages_str.split("|") if m.strip()]
    if not messages:
        return ""

    _tick_counter += 1
    if _tick_counter >= interval:
        _tick_counter = 0
        _message_index = (_message_index + 1) % len(messages)

    current = messages[_message_index % len(messages)]
    return context["check_data"](current, data)


plugin = ChatboxPlugin(name="cycler", render=render_cycler)
