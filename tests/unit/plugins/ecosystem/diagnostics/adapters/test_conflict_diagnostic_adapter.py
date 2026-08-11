"""Tests for the conflict diagnostic adapter."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    ConflictDiagnosticAdapter,
    ConflictReason,
    DiagnosticKind,
    DiagnosticSeverity,
    PluginConflict,
)


def test_adapter_maps_missing_package_conflict() -> None:
    """A missing package becomes a missing-dependency diagnostic."""

    conflict = PluginConflict(
        plugin="familyos.security",
        reason=ConflictReason.PACKAGE_NOT_FOUND,
        required_by=("familyos.application",),
    )

    diagnostics = ConflictDiagnosticAdapter().adapt(
        (conflict,),
    )

    assert len(diagnostics) == 1

    diagnostic = diagnostics[0]

    assert diagnostic.kind is DiagnosticKind.MISSING_DEPENDENCY
    assert diagnostic.severity is DiagnosticSeverity.ERROR
    assert diagnostic.plugin == "familyos.security"
    assert diagnostic.message == (
        "Plugin 'familyos.security' is required but not available."
    )
    assert diagnostic.details == ("Required by: familyos.application",)
    assert diagnostic.path == (
        "familyos.application",
        "familyos.security",
    )


def test_adapter_maps_invalid_version_conflict() -> None:
    """An invalid version becomes an invalid-package diagnostic."""

    conflict = PluginConflict(
        plugin="familyos.security",
        reason=ConflictReason.INVALID_VERSION,
        available_versions=("latest",),
    )

    diagnostic = ConflictDiagnosticAdapter().adapt(
        (conflict,),
    )[0]

    assert diagnostic.kind is DiagnosticKind.INVALID_PACKAGE
    assert diagnostic.message == (
        "Plugin 'familyos.security' has an invalid package version."
    )
    assert diagnostic.details == ("Available version: latest",)


def test_adapter_maps_incompatible_constraints() -> None:
    """Incompatible constraints become a version-conflict diagnostic."""

    conflict = PluginConflict(
        plugin="familyos.crypto",
        reason=ConflictReason.INCOMPATIBLE_CONSTRAINTS,
        required_by=(
            "familyos.security",
            "familyos.backup",
        ),
        requested_constraints=(
            ">=3.0.0",
            "<3.0.0",
        ),
        available_versions=(
            "2.0.0",
            "3.0.0",
        ),
    )

    diagnostic = ConflictDiagnosticAdapter().adapt(
        (conflict,),
    )[0]

    assert diagnostic.kind is DiagnosticKind.VERSION_CONFLICT
    assert diagnostic.message == (
        "Plugin 'familyos.crypto' has incompatible version constraints."
    )
    assert diagnostic.details == (
        "Required by: familyos.security",
        "Required by: familyos.backup",
        "Requested constraint: >=3.0.0",
        "Requested constraint: <3.0.0",
        "Available version: 2.0.0",
        "Available version: 3.0.0",
    )
    assert diagnostic.path == (
        "familyos.security",
        "familyos.backup",
        "familyos.crypto",
    )


def test_adapter_maps_missing_compatible_version() -> None:
    """An unavailable compatible version becomes a version conflict."""

    conflict = PluginConflict(
        plugin="familyos.crypto",
        reason=ConflictReason.NO_COMPATIBLE_VERSION,
        requested_constraints=(">=4.0.0",),
        available_versions=(
            "2.0.0",
            "3.0.0",
        ),
    )

    diagnostic = ConflictDiagnosticAdapter().adapt(
        (conflict,),
    )[0]

    assert diagnostic.kind is DiagnosticKind.VERSION_CONFLICT
    assert diagnostic.message == (
        "No compatible version is available for plugin 'familyos.crypto'."
    )


def test_adapter_preserves_conflict_order() -> None:
    """Conflicts are adapted in their original order."""

    diagnostics = ConflictDiagnosticAdapter().adapt(
        (
            PluginConflict(
                plugin="familyos.security",
                reason=ConflictReason.PACKAGE_NOT_FOUND,
            ),
            PluginConflict(
                plugin="familyos.backup",
                reason=ConflictReason.PACKAGE_NOT_FOUND,
            ),
        ),
    )

    assert tuple(diagnostic.plugin for diagnostic in diagnostics) == (
        "familyos.security",
        "familyos.backup",
    )
