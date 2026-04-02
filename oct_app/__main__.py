from __future__ import annotations

"""Thin startup entry for modular OCT package."""

import importlib.util
from pathlib import Path
from threading import Thread

from . import hr, media, message_engine, osc_io, ui


def _load_legacy_module():
    root = Path(__file__).resolve().parents[1]
    legacy_path = root / "osc-chat-tools.py"
    spec = importlib.util.spec_from_file_location("osc_chat_tools_legacy", legacy_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> None:
    legacy = _load_legacy_module()

    # Wire moved function groups while keeping legacy behavior.
    Thread(target=ui.uiThread, args=(legacy.uiThread,), daemon=True).start()
    Thread(target=message_engine.runmsg, args=(legacy, lambda m: legacy.client.send_message('/chatbox/input', [m, True, False])), daemon=True).start()
    Thread(target=hr.hrConnectionThread, args=(legacy, legacy.hrConnectionThread), daemon=True).start()
    Thread(target=osc_io.oscListenServerManager, args=(lambda: None,), daemon=True).start()
    Thread(target=osc_io.oscForwardingManager, args=(lambda: None,), daemon=True).start()

    # Keep Spotify helpers importable from the new module boundary.
    legacy.refreshAccessToken = lambda token: media.refreshAccessToken(legacy, token)
    legacy.getSpotifyPlaystate = lambda: media.getSpotifyPlaystate(legacy)

    legacy.mainUI.join()


if __name__ == "__main__":
    main()
