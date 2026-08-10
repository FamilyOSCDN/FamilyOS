"""Tests for plugin installer."""

from familyos_cli.plugins.ecosystem.installation import (
    PluginInstaller,
)
from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)


def test_plugin_package_installation() -> None:
    """Installer should create installed plugins."""

    package = PluginPackage(
        plugin_id="familyos.calendar",
        version="1.0.0",
        source="official",
    )

    installer = PluginInstaller()

    installed = installer.install(
        package,
        "/plugins/calendar",
    )

    assert installed.plugin_id == "familyos.calendar"
    assert installed.name == "familyos.calendar"
    assert installed.version == "1.0.0"
    assert installed.location == "/plugins/calendar"
