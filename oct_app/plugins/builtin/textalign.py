from ..base import ChatboxPlugin


def render_textalign(context, text, data=0):
    alignment = context.get("text_alignment", "left")
    width = context.get("text_align_width", 30)
    result = text.replace("\\n", "\v").replace("\\v", "\v")

    if alignment == "center":
        result = result.center(width)
    elif alignment == "right":
        result = result.rjust(width)

    return context["check_data"](result, data)


plugin = ChatboxPlugin(name="textalign", render=render_textalign)
