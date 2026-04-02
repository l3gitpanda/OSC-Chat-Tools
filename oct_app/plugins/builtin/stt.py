from ..base import ChatboxPlugin


def render_stt(context, _text, data=0):
    return context["check_data"]("Coming Soon", data)


plugin = ChatboxPlugin(name="stt", render=render_stt)
