"""Heart-rate integration wrappers for OCT."""


def hrConnectionThread():
    from . import main as legacy_main

    return legacy_main.hrConnectionThread()
