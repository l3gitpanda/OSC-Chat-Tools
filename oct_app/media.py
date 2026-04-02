from __future__ import annotations

from threading import Thread
from typing import Any, Callable

import requests


def refreshAccessToken(ctx: Any, oldRefreshToken: str) -> None:
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": oldRefreshToken,
        "client_id": ctx.spotify_client_id,
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        raise Exception(f"AccessToken refresh error... {response.json()}")

    ctx.spotifyRefreshToken = response.json().get("refresh_token")
    ctx.spotifyAccessToken = response.json().get("access_token")


def getSpotifyPlaystate(ctx: Any) -> dict | str:
    def get_playstate(accessToken: str) -> dict | str:
        headers = {"Authorization": "Bearer " + accessToken}
        response = requests.get("https://api.spotify.com/v1/me/player", headers=headers)
        if response.status_code == 204:
            return ""
        return response.json()

    try:
        playState = get_playstate(ctx.spotifyAccessToken)
        if playState not in ("", None) and "error" in str(playState):
            raise Exception(str(playState))
    except Exception as e:
        if "expired" in str(e):
            ctx.outputLog(f"Attempting to regenerate outdated access token...\\nReason: {e}")
            refreshAccessToken(ctx, ctx.spotifyRefreshToken)

            def waitThread() -> None:
                while ctx.windowAccess is None:
                    pass
                ctx.windowAccess.write_event_value("Apply", "")

            Thread(target=waitThread).start()
            playState = get_playstate(ctx.spotifyAccessToken)
        else:
            ctx.outputLog(f"Spotify connection error... retrying\\nFull Error: {e}")
            playState = get_playstate(ctx.spotifyAccessToken)

    if playState is None:
        return ""
    return playState


def linkSpotify(ctx: Any, linker: Callable[[], str]) -> str:
    """Wrapper for Spotify linking flow to keep API wiring in one module."""

    linked_user = linker()
    ctx.spotifyLinkStatus = f"Linked to {linked_user}" if linked_user else "Unlinked"
    return linked_user
