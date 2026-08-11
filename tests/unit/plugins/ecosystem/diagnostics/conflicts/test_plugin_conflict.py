"""Tests for the plugin resolution conflict model."""

import pytest

from familyos_cli.plugins.ecosystem.diagnostics import (
    ConflictReason,
    PluginConflict,
)


def test_plugin_conflict_creation() -> None:
    """A conflict stores its complete technical context."""

    conflict = PluginConflict(
        plugin="familyos.crypto",
        reason=ConflictReason.INCOMPATIBLE_CONSTRAINTS,
        required_by=(
            "familyos.security",
            "familyos.backup",
        ),
        requested_constraints=(
            ">=3.0",
            "<3.0",
        ),
        available_versions=(
            "2.0.0",
            "2.5.0",
            "3.0.0",
        ),
    )

    assert conflict.plugin == "familyos.crypto"
    assert conflict.reason is ConflictReason.INCOMPATIBLE_CONSTRAINTS
    assert conflict.required_by == (
        "familyos.security",
        "familyos.backup",
    )
    assert conflict.requested_constraints == (
        ">=3.0",
        "<3.0",
    )
    assert conflict.available_versions == (
        "2.0.0",
        "2.5.0",
        "3.0.0",
    )


def test_plugin_conflict_defaults() -> None:
    """Optional conflict context defaults to immutable empty tuples."""

    conflict = PluginConflict(
        plugin="familyos.unknown",
        reason=ConflictReason.PACKAGE_NOT_FOUND,
    )

    assert conflict.required_by == ()
    assert conflict.requested_constraints == ()
    assert conflict.available_versions == ()


def test_plugin_conflict_rejects_non_canonical_plugin_id() -> None:
    """A conflict should reject non-canonical plugin identifiers."""

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        PluginConflict(
            plugin="crypto",
            reason=ConflictReason.PACKAGE_NOT_FOUND,
        )


def test_plugin_conflict_rejects_non_canonical_required_by_id() -> None:
    """Required-by relationships should use canonical plugin identifiers."""

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        PluginConflict(
            plugin="familyos.crypto",
            reason=ConflictReason.PACKAGE_NOT_FOUND,
            required_by=("security",),
        )


def test_plugin_conflict_concerns_plugin() -> None:
    """A conflict identifies the plugin it concerns."""

    conflict = PluginConflict(
        plugin="familyos.crypto",
        reason=ConflictReason.NO_COMPATIBLE_VERSION,
    )

    assert conflict.concerns("familyos.crypto")
    assert not conflict.concerns("familyos.backup")


def test_plugin_conflict_identifies_requiring_plugins() -> None:
    """A conflict identifies plugins that introduced requirements."""

    conflict = PluginConflict(
        plugin="familyos.crypto",
        reason=ConflictReason.INCOMPATIBLE_CONSTRAINTS,
        required_by=(
            "familyos.security",
            "familyos.backup",
        ),
    )

    assert conflict.is_required_by("familyos.security")
    assert conflict.is_required_by("familyos.backup")
    assert not conflict.is_required_by("familyos.documents")


def test_plugin_conflict_detects_available_versions() -> None:
    """A conflict reports whether package versions were available."""

    available = PluginConflict(
        plugin="familyos.crypto",
        reason=ConflictReason.NO_COMPATIBLE_VERSION,
        available_versions=(
            "1.0.0",
            "2.0.0",
        ),
    )
    unavailable = PluginConflict(
        plugin="familyos.unknown",
        reason=ConflictReason.PACKAGE_NOT_FOUND,
    )

    assert available.has_available_versions()
    assert not unavailable.has_available_versions()


def test_plugin_conflict_detects_multiple_constraints() -> None:
    """A conflict reports whether several constraints contributed."""

    multiple = PluginConflict(
        plugin="familyos.crypto",
        reason=ConflictReason.INCOMPATIBLE_CONSTRAINTS,
        requested_constraints=(
            ">=3.0",
            "<3.0",
        ),
    )
    single = PluginConflict(
        plugin="familyos.crypto",
        reason=ConflictReason.NO_COMPATIBLE_VERSION,
        requested_constraints=(">=4.0",),
    )

    assert multiple.has_multiple_constraints()
    assert not single.has_multiple_constraints()
