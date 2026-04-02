from collections import defaultdict

from ..base import ChatboxPlugin


def render_hr(context, _text, data=0):
    hr = str(context["heart_rate"])
    if hr in {"0", "1"}:
        hr = "-"
    hr_info = context["hr_display"].format_map(defaultdict(str, hr=hr))
    return context["check_data"](hr_info, data)


plugin = ChatboxPlugin(name="hr", render=render_hr)
