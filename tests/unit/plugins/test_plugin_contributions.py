"""Tests for the Plugin contribution API."""

from familyos_cli.plugins.plugin import Plugin


def test_plugin_exposes_no_contributions_by_default() -> None:
    """Base plugin should expose an empty contribution collection."""

    plugin = Plugin()

    assert plugin.contributions() == ()
