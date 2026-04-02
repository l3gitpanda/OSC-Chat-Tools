from ..base import ChatboxPlugin


def render_text(context, text, data=0):
    return context["check_data"](text.replace("\\n", "\v").replace("\\v", "\v"), data)


plugin = ChatboxPlugin(name="text", render=render_text)
