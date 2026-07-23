from __future__ import annotations

import importlib


def test_import_module() -> None:
    """A plugin module should be importable."""

    module = importlib.import_module(
        "familyos_cli.plugins.plugin",
    )

    assert module is not None