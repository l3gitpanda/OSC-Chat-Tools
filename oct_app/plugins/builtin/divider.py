from ..base import ChatboxPlugin


def render_divider(context, _text, data=0):
    return context["check_data"](context["middle_bar"], data)


plugin = ChatboxPlugin(name="div", render=render_divider)
