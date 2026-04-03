from ..base import ChatboxPlugin

_ABBREVIATIONS = {
    " and ": " & ",
    " with ": " w/ ",
    " without ": " w/o ",
    " because ": " bc ",
    " before ": " b4 ",
    " please ": " pls ",
    " people ": " ppl ",
    " something ": " sth ",
    " someone ": " sb ",
    " about ": " abt ",
    " between ": " btwn ",
    " through ": " thru ",
    " though ": " tho ",
    " really ": " rly ",
    " probably ": " prob ",
    " tonight ": " 2nite ",
    " tomorrow ": " tmrw ",
    " together ": " tgth ",
}


def render_smarttruncate(context, text, data=0):
    max_len = context.get("smart_truncate_max", 144)
    result = text.replace("\\n", "\v").replace("\\v", "\v")

    if len(result) <= max_len:
        return context["check_data"](result, data)

    # Try abbreviations first
    for full, short in _ABBREVIATIONS.items():
        if len(result) <= max_len:
            break
        result = result.replace(full, short)

    # If still too long, truncate with ellipsis
    if len(result) > max_len:
        result = result[:max_len - 3] + "..."

    return context["check_data"](result, data)


plugin = ChatboxPlugin(name="smarttruncate", render=render_smarttruncate)
