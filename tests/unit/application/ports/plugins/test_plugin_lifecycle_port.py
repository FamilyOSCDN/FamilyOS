"""Tests for plugin lifecycle port."""

import inspect

from familyos_cli.application.ports.plugins import (
    PluginLifecyclePort,
)


def test_plugin_lifecycle_port_is_abstract() -> None:
    """Lifecycle port should be abstract."""

    assert inspect.isabstract(PluginLifecyclePort)
