import random

from ..base import ChatboxPlugin

_KAOMOJI = {
    "happy": ["(◕‿◕)", "(｡◕‿◕｡)", "(◠‿◠)", "(✿◠‿◠)", "(◕ᴗ◕✿)", "(*≧ω≦)", "(≧◡≦)", "(◠ᴗ◠)", "☆*:.｡.o(≧▽≦)o.｡.:*☆"],
    "sad": ["(╥﹏╥)", "(っ˘̩╭╮˘̩)っ", "(T_T)", "(;_;)", "(ノ_<。)", "( ´_ゝ`)", "(´;ω;`)", "(._.)", "(μ_μ)"],
    "shrug": ["¯\\_(ツ)_/¯", "┐(´ー｀)┌", "╮(╯_╰)╭", "¯\\_(⊙_ʖ⊙)_/¯", "ᕕ( ᐛ )ᕗ"],
    "dance": ["♪┌|∵|┘♪", "└|∵|┐♪", "♪(┌・。・)┌", "ヽ(⌐■_■)ノ♪♬", "(ノ˘ ³˘)ノ°˖✧", "~(˘▾˘~)", "(~˘▾˘)~"],
    "love": ["(♡˙︶˙♡)", "(◍•ᴗ•◍)❤", "(´∀`)♡", "(◕‿◕)♡", "♡(ŐωŐ人)", "(ɔˆ ³(ˆ⌣ˆc)", "(*♡∀♡)"],
    "angry": ["(╯°□°)╯︵ ┻━┻", "(ノಠ益ಠ)ノ彡┻━┻", "ヽ(`Д´)ノ", "(ง'̀-'́)ง", "(¬_¬)", "( •̀ω•́ )σ", "(ᗒᗣᗕ)՞"],
}


def render_kaomoji(context, _text, data=0):
    category = context.get("kaomoji_category", "random")
    if category == "random":
        all_kaomoji = [k for group in _KAOMOJI.values() for k in group]
        result = random.choice(all_kaomoji)
    else:
        pool = _KAOMOJI.get(category, _KAOMOJI["happy"])
        result = random.choice(pool)
    return context["check_data"](result, data)


plugin = ChatboxPlugin(name="kaomoji", render=render_kaomoji)
