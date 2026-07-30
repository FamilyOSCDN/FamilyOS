"""Tests for plugin discovery port."""

import pytest

from familyos_cli.application.ports.plugins import (
    PluginDiscoveryPort,
)


def test_plugin_discovery_port_is_abstract() -> None:
    """Discovery port should be abstract."""

    with pytest.raises(TypeError):
        PluginDiscoveryPort()
