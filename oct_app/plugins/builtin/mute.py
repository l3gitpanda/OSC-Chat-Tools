from ..base import ChatboxPlugin


def render_mute(context, _text, data=0):
    output = context["muted_display"] if context["is_muted"] else context["unmuted_display"]
    return context["check_data"](output, data)


plugin = ChatboxPlugin(name="mute", render=render_mute)
