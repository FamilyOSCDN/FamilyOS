"""Tests for plugin discovery port."""

import inspect

from familyos_cli.application.ports.plugins import (
    PluginDiscoveryPort,
)


def test_plugin_discovery_port_is_abstract() -> None:
    """Discovery port should be abstract."""

    assert inspect.isabstract(PluginDiscoveryPort)
