"""Tests for installed plugin model."""

from familyos_cli.plugins.ecosystem.installation import (
    InstalledPlugin,
)


def test_installed_plugin_identifier() -> None:
    """Installed plugin identifier should be generated."""

    plugin = InstalledPlugin(
        name="calendar",
        version="1.0.0",
        location="/plugins/calendar",
    )

    assert plugin.identifier() == "calendar@1.0.0"
