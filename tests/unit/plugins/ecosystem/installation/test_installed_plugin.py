"""Tests for installed plugin model."""

import pytest

from familyos_cli.plugins.ecosystem.installation import (
    InstalledPlugin,
)


def test_installed_plugin_identifier() -> None:
    """Installed plugin identifier should use canonical identity."""

    plugin = InstalledPlugin(
        name="documentation",
        version="1.0.0",
        location="/plugins/documentation",
    )

    assert plugin.plugin_id == "familyos.documentation"
    assert plugin.name == "familyos.documentation"
    assert plugin.identifier() == "familyos.documentation@1.0.0"


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

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        InstalledPlugin(
            plugin_id="invalid",
            version="1.0.0",
            location="/plugins/invalid",
        )


def test_installed_plugin_normalizes_legacy_name_identity() -> None:
    """Legacy name construction should normalize to canonical identity."""

    plugin = InstalledPlugin(
        name="documentation",
        version="1.0.0",
        location="/plugins/documentation",
    )

    assert plugin.plugin_id == "familyos.documentation"
    assert plugin.name == "familyos.documentation"
    assert plugin.identifier() == "familyos.documentation@1.0.0"


def test_installed_plugin_rejects_conflicting_identity_arguments() -> None:
    """Canonical and legacy identity inputs must not disagree."""

    with pytest.raises(
        ValueError,
        match="same Plugin Identifier",
    ):
        InstalledPlugin(
            name="documentation",
            plugin_id="familyos.documents",
            version="1.0.0",
            location="/plugins/documentation",
        )


def test_installed_plugin_rejects_unknown_legacy_name_identity() -> None:
    """Unknown legacy names must still satisfy the canonical contract."""

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        InstalledPlugin(
            name="invalid",
            version="1.0.0",
            location="/plugins/invalid",
        )
