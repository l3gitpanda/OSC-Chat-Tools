"""Spotify integration wrappers for OCT."""


def spotifyConnectionManager():
    from . import main as legacy_main

    return legacy_main.spotifyConnectionManager()
