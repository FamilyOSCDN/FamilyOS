"""Tests for plugin installer port."""

import pytest

from familyos_cli.application.ports.plugins import (
    PluginInstallerPort,
)


def test_plugin_installer_port_is_abstract() -> None:
    """Installer port should be abstract."""

    with pytest.raises(TypeError):
        PluginInstallerPort()
