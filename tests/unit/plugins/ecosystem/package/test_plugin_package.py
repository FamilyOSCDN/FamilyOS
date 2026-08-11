"""Tests for plugin package model."""

import pytest

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)


def test_plugin_package_creation() -> None:
    """Plugin package should be created with a canonical identifier."""

    package = PluginPackage(
        plugin_id="familyos.calendar",
        version="1.0.0",
        source="official",
    )

    assert package.plugin_id == "familyos.calendar"
    assert package.version == "1.0.0"
    assert package.identifier() == "familyos.calendar@1.0.0"


def test_plugin_package_normalizes_canonical_plugin_id() -> None:
    """Canonical Plugin Identifiers should be validated on construction."""

    package = PluginPackage(
        plugin_id="familyos.calendar",
        version="1.0.0",
        source="official",
    )

    assert package.plugin_id == "familyos.calendar"


def test_plugin_package_rejects_invalid_plugin_id() -> None:
    """Invalid Plugin Identifiers should be rejected."""

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        PluginPackage(
            plugin_id="calendar",
            version="1.0.0",
            source="official",
        )


def test_plugin_package_preserves_optional_metadata() -> None:
    """Optional package metadata should be preserved."""

    package = PluginPackage(
        plugin_id="familyos.calendar",
        version="1.0.0",
        source="official",
        checksum="sha256:test",
        signature="signature",
    )

    assert package.checksum == "sha256:test"
    assert package.signature == "signature"


def test_plugin_package_is_immutable() -> None:
    """Plugin package identity and metadata should be immutable."""

    package = PluginPackage(
        plugin_id="familyos.calendar",
        version="1.0.0",
        source="official",
    )

    with pytest.raises(
        AttributeError,
    ):
        package.plugin_id = "familyos.documents"  # type: ignore[misc]
