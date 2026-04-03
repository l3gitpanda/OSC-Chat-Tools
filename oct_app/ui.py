"""UI module wrappers for OCT - now delegates to web UI."""


def layoutPreviewBuilder(layout, window=None):
    """Legacy stub - layout preview is now handled in the web UI JavaScript."""
    pass


def uiThread():
    from . import main as legacy_main

    return legacy_main.uiThread()
