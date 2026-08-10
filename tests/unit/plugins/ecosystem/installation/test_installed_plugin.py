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


def test_installed_plugin_accepts_canonical_plugin_id() -> None:
    """Installed plugin should accept a canonical Plugin Identifier."""

    plugin = InstalledPlugin(
        plugin_id="familyos.calendar",
        version="1.0.0",
        location="/plugins/calendar",
    )

    assert plugin.plugin_id == "familyos.calendar"
    assert plugin.name == "familyos.calendar"
    assert plugin.identifier() == "familyos.calendar@1.0.0"


def test_installed_plugin_rejects_invalid_explicit_plugin_id() -> None:
    """Explicit Plugin Identifiers should satisfy the canonical contract."""

    import pytest

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        InstalledPlugin(
            plugin_id="calendar",
            version="1.0.0",
            location="/plugins/calendar",
        )


def test_installed_plugin_preserves_legacy_name_identity() -> None:
    """Legacy name construction should remain compatible."""

    plugin = InstalledPlugin(
        name="calendar",
        version="1.0.0",
        location="/plugins/calendar",
    )

    assert plugin.plugin_id == "calendar"
    assert plugin.name == "calendar"
    assert plugin.identifier() == "calendar@1.0.0"


def test_installed_plugin_rejects_conflicting_identity_arguments() -> None:
    """Canonical and legacy identity inputs must not disagree."""

    import pytest

    with pytest.raises(
        ValueError,
        match="same Plugin Identifier",
    ):
        InstalledPlugin(
            name="calendar",
            plugin_id="familyos.calendar",
            version="1.0.0",
            location="/plugins/calendar",
        )
