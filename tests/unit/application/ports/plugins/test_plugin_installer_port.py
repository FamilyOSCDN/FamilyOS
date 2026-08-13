"""Tests for plugin installer port."""

import inspect

from familyos_cli.application.ports.plugins import (
    PluginInstallerPort,
)


def test_plugin_installer_port_is_abstract() -> None:
    """Installer port should be abstract."""

    assert inspect.isabstract(PluginInstallerPort)
