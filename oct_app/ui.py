"""UI module wrappers for OCT."""


def layoutPreviewBuilder(layout, window):
    from . import main as legacy_main

    return legacy_main.layoutPreviewBuilder(layout, window)


def uiThread():
    from . import main as legacy_main

    return legacy_main.uiThread()
