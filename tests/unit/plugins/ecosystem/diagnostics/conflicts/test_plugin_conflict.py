"""Tests for the plugin resolution conflict model."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    ConflictReason,
    PluginConflict,
)


def test_plugin_conflict_creation() -> None:
    """A conflict stores its complete technical context."""

    conflict = PluginConflict(
        plugin="crypto",
        reason=ConflictReason.INCOMPATIBLE_CONSTRAINTS,
        required_by=(
            "security",
            "backup",
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

    assert conflict.plugin == "crypto"
    assert conflict.reason is ConflictReason.INCOMPATIBLE_CONSTRAINTS
    assert conflict.required_by == (
        "security",
        "backup",
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
        plugin="unknown",
        reason=ConflictReason.PACKAGE_NOT_FOUND,
    )

    assert conflict.required_by == ()
    assert conflict.requested_constraints == ()
    assert conflict.available_versions == ()


def test_plugin_conflict_concerns_plugin() -> None:
    """A conflict identifies the plugin it concerns."""

    conflict = PluginConflict(
        plugin="crypto",
        reason=ConflictReason.NO_COMPATIBLE_VERSION,
    )

    assert conflict.concerns("crypto")
    assert not conflict.concerns("backup")


def test_plugin_conflict_identifies_requiring_plugins() -> None:
    """A conflict identifies plugins that introduced requirements."""

    conflict = PluginConflict(
        plugin="crypto",
        reason=ConflictReason.INCOMPATIBLE_CONSTRAINTS,
        required_by=(
            "security",
            "backup",
        ),
    )

    assert conflict.is_required_by("security")
    assert conflict.is_required_by("backup")
    assert not conflict.is_required_by("documents")


def test_plugin_conflict_detects_available_versions() -> None:
    """A conflict reports whether package versions were available."""

    available = PluginConflict(
        plugin="crypto",
        reason=ConflictReason.NO_COMPATIBLE_VERSION,
        available_versions=(
            "1.0.0",
            "2.0.0",
        ),
    )
    unavailable = PluginConflict(
        plugin="unknown",
        reason=ConflictReason.PACKAGE_NOT_FOUND,
    )

    assert available.has_available_versions()
    assert not unavailable.has_available_versions()


def test_plugin_conflict_detects_multiple_constraints() -> None:
    """A conflict reports whether several constraints contributed."""

    multiple = PluginConflict(
        plugin="crypto",
        reason=ConflictReason.INCOMPATIBLE_CONSTRAINTS,
        requested_constraints=(
            ">=3.0",
            "<3.0",
        ),
    )
    single = PluginConflict(
        plugin="crypto",
        reason=ConflictReason.NO_COMPATIBLE_VERSION,
        requested_constraints=(">=4.0",),
    )

    assert multiple.has_multiple_constraints()
    assert not single.has_multiple_constraints()
