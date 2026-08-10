"""Tests for plugin verifier."""

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.verification import (
    PluginVerifier,
)


def test_plugin_package_is_verified() -> None:
    """Valid packages should pass verification."""

    package = PluginPackage(
        name="calendar",
        version="1.0.0",
        source="official",
    )

    verifier = PluginVerifier()

    result = verifier.verify(package)

    assert result.is_valid() is True
    assert result.reason == "Package verified."


def test_missing_plugin_id_fails_verification() -> None:
    """Packages without Plugin Identifiers should fail verification."""

    package = PluginPackage(
        name="",
        version="1.0.0",
        source="official",
    )

    verifier = PluginVerifier()

    result = verifier.verify(package)

    assert result.is_valid() is False
    assert result.reason == "Plugin identifier is missing."


def test_missing_version_fails_verification() -> None:
    """Packages without versions should fail verification."""

    package = PluginPackage(
        name="calendar",
        version="",
        source="official",
    )

    verifier = PluginVerifier()

    result = verifier.verify(package)

    assert result.is_valid() is False
    assert result.reason == "Plugin version is missing."
