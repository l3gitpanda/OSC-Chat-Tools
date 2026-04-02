"""Logging utility wrappers for OCT."""


def outputLog(*args, **kwargs):
    from . import main as legacy_main

    return legacy_main.outputLog(*args, **kwargs)
