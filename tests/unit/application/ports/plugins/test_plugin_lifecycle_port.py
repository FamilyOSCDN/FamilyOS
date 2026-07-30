"""Tests for plugin lifecycle port."""

import pytest

from familyos_cli.application.ports.plugins import (
    PluginLifecyclePort,
)


def test_plugin_lifecycle_port_is_abstract() -> None:
    """Lifecycle port should be abstract."""

    with pytest.raises(TypeError):
        PluginLifecyclePort()
