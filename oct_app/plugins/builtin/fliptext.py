from ..base import ChatboxPlugin

_FLIP_MAP = dict(zip(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?'\"()[]{}<>_",
    "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz∀ꓭƆᗡƎℲ⅁HIſꓘ⅂WNOԁQꓤSꓕ∩ΛMX⅄Z0ƖᄅƐㄣϛ9ㄥ86˙'¡¿,„)(][}{><‾"
))

_MIRROR_MAP = dict(zip(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()[]{}<>",
    "ɒdɔbɘꟻǫʜiꞁʞlmnoqpɿꙅƚυvwxʏzAdƆbƎꟻGHIJꓘ⅃MͶOꟼpɈꙄTUVWXYZ)(][}{><"
))


def render_fliptext(context, text, data=0):
    flip = context.get("flip_text", False)
    mirror = context.get("mirror_text", False)
    result = text.replace("\\n", "\v").replace("\\v", "\v")

    if flip:
        result = "".join(_FLIP_MAP.get(c, c) for c in result)[::-1]
    if mirror:
        result = "".join(_MIRROR_MAP.get(c, c) for c in result)[::-1]

    return context["check_data"](result, data)


plugin = ChatboxPlugin(name="fliptext", render=render_fliptext)
