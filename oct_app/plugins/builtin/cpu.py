from collections import defaultdict

import psutil

from ..base import ChatboxPlugin


def render_cpu(context, _text, data=0):
    cpu_percent = str(psutil.cpu_percent())
    cpu_data = context["cpu_display"].format_map(defaultdict(str, cpu_percent=cpu_percent))
    return context["check_data"](cpu_data, data)


plugin = ChatboxPlugin(name="cpu", render=render_cpu)
