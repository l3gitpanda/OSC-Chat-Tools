from __future__ import annotations

import time
from typing import Any, Callable, Iterable


def processMessage(ctx: Any, a: str) -> Iterable[str]:
    """Message processing shim; uses legacy processor when available."""

    if hasattr(ctx, "legacy_processMessage") and callable(ctx.legacy_processMessage):
        return ctx.legacy_processMessage(a)
    return [a]


def sendMsg(ctx: Any, a: str, sender: Callable[[str], None]) -> None:
    sender(a)
    ctx.lastSent = a
    ctx.sentTime = time.time()


def runmsg(ctx: Any, sender: Callable[[str], None]) -> None:
    ctx.textParseIterator = getattr(ctx, "textParseIterator", 0)
    while ctx.playMsg:
        text_storage = ctx.messageString
        if not ctx.afk and not ctx.scrollText:
            for x in processMessage(ctx, ctx.messageString):
                if ctx.afk or ctx.scrollText or (not ctx.playMsg) or (not ctx.run) or (ctx.messageString != text_storage):
                    break
                if x == "*":
                    sendMsg(ctx, " ㅤ", sender)
                else:
                    sendMsg(ctx, " " + x, sender)
        elif ctx.afk:
            sendMsg(ctx, "\vAFK\v", sender)
            sendMsg(ctx, "\vㅤ\v", sender)
        else:
            sendMsg(ctx, "", sender)

    if getattr(ctx, "sendBlank", False):
        sender("")
