from collections import defaultdict

from ..base import ChatboxPlugin


def render_ram(context, _text, data=0):
    import psutil
    vm = psutil.virtual_memory()
    ram_percent = str(int(vm[2]))
    ram_used = str(round(int(vm[0]) / 1073741824 - int(vm[1]) / 1073741824, 1))
    ram_available = str(round(int(vm[1]) / 1073741824, 1))
    ram_total = str(round(int(vm[0]) / 1073741824, 1))
    ram_data = context["ram_display"].format_map(
        defaultdict(
            str,
            ram_percent=ram_percent,
            ram_available=ram_available,
            ram_total=ram_total,
            ram_used=ram_used,
        )
    )
    return context["check_data"](ram_data, data)


plugin = ChatboxPlugin(name="ram", render=render_ram)
