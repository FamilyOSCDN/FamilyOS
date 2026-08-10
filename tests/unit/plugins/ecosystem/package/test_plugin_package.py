"""Tests for plugin package model."""

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)


def test_plugin_package_creation() -> None:
    """Plugin package should be created."""

    package = PluginPackage(
        name="calendar",
        version="1.0.0",
        source="official",
    )

    assert package.name == "calendar"
    assert package.version == "1.0.0"
    assert package.identifier() == "calendar@1.0.0"


def test_plugin_package_exposes_canonical_plugin_id() -> None:
    """Package should expose an explicit canonical Plugin Identifier."""

    package = PluginPackage(
        plugin_id="familyos.calendar",
        version="1.0.0",
        source="official",
    )

    assert package.plugin_id == "familyos.calendar"
    assert package.name == "familyos.calendar"
    assert package.identifier() == "familyos.calendar@1.0.0"


def test_plugin_package_accepts_legacy_name_argument() -> None:
    """Legacy name argument should remain compatible."""

    package = PluginPackage(
        name="familyos.calendar",
        version="1.0.0",
        source="official",
    )

    assert package.plugin_id == "familyos.calendar"
    assert package.name == "familyos.calendar"


def test_plugin_package_rejects_conflicting_identity_arguments() -> None:
    """Canonical and legacy identity inputs must not disagree."""

    import pytest

    with pytest.raises(
        ValueError,
        match="same Plugin Identifier",
    ):
        PluginPackage(
            name="calendar",
            plugin_id="familyos.calendar",
            version="1.0.0",
            source="official",
        )


def test_plugin_package_rejects_invalid_explicit_plugin_id() -> None:
    """Explicit Plugin Identifiers should satisfy the canonical contract."""

    import pytest

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        PluginPackage(
            plugin_id="calendar",
            version="1.0.0",
            source="official",
        )


def test_plugin_package_preserves_legacy_name_identity() -> None:
    """Legacy name construction should remain compatible."""

    package = PluginPackage(
        name="calendar",
        version="1.0.0",
        source="official",
    )

    assert package.plugin_id == "calendar"
    assert package.name == "calendar"
