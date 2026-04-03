import random

from ..base import ChatboxPlugin

_ZALGO_UP = [
    '\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0305', '\u0306',
    '\u0307', '\u0308', '\u0309', '\u030a', '\u030b', '\u030c', '\u030d',
    '\u030e', '\u030f', '\u0310', '\u0311', '\u0312', '\u0313', '\u0314',
    '\u0315', '\u031a', '\u031b',
]

_ZALGO_MID = [
    '\u0334', '\u0335', '\u0336', '\u0337', '\u0338',
]

_ZALGO_DOWN = [
    '\u0316', '\u0317', '\u0318', '\u0319', '\u031c', '\u031d', '\u031e',
    '\u031f', '\u0320', '\u0321', '\u0322', '\u0323', '\u0324', '\u0325',
    '\u0326', '\u0327', '\u0328', '\u0329', '\u032a', '\u032b', '\u032c',
    '\u032d', '\u032e', '\u032f', '\u0330', '\u0331', '\u0332', '\u0333',
]

_INTENSITY_RANGES = {
    1: (0, 2),   # light
    2: (1, 4),   # medium
    3: (3, 7),   # heavy
}


def _zalgoify(text, intensity):
    lo, hi = _INTENSITY_RANGES.get(intensity, (1, 4))
    out = []
    for c in text:
        if c in (' ', '\v', '\n'):
            out.append(c)
            continue
        out.append(c)
        for pool in (_ZALGO_UP, _ZALGO_MID, _ZALGO_DOWN):
            for _ in range(random.randint(lo, hi)):
                out.append(random.choice(pool))
    return "".join(out)


def render_zalgo(context, text, data=0):
    enabled = context.get("zalgo_enabled", False)
    if not enabled:
        return context["check_data"](text.replace("\\n", "\v").replace("\\v", "\v"), data)
    intensity = context.get("zalgo_intensity", 2)
    result = _zalgoify(text.replace("\\n", "\v").replace("\\v", "\v"), intensity)
    return context["check_data"](result, data)


plugin = ChatboxPlugin(name="zalgo", render=render_zalgo)
