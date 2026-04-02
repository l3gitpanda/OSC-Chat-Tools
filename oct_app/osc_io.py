"""OSC I/O module wrappers for OCT."""


def runmsg():
    from . import main as legacy_main

    return legacy_main.runmsg()
