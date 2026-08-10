"""Tests for the resolution conflict adapter."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    ConflictReason,
    ResolutionConflictAdapter,
)
from familyos_cli.plugins.ecosystem.package import PluginPackage
from familyos_cli.plugins.ecosystem.resolution import (
    ResolutionDiagnostic,
    ResolutionPlan,
)


def test_adapter_returns_no_conflict_for_successful_plan() -> None:
    """A successful resolution plan contains no conflicts."""

    plan = ResolutionPlan(
        ordered_packages=[
            PluginPackage(
                plugin_id="familyos.security",
                version="1.0.0",
                source="official",
            ),
        ],
    )

    conflicts = ResolutionConflictAdapter().adapt(
        plan,
    )

    assert conflicts == ()


def test_adapter_maps_missing_dependency() -> None:
    """An unavailable dependency becomes a package-not-found conflict."""

    plan = ResolutionPlan(
        diagnostics=[
            ResolutionDiagnostic(
                plugin="familyos.security",
                message=("Required plugin dependency is not available."),
            ),
        ],
    )

    conflicts = ResolutionConflictAdapter().adapt(
        plan,
    )

    assert len(conflicts) == 1
    assert conflicts[0].plugin == "familyos.security"
    assert conflicts[0].reason is ConflictReason.PACKAGE_NOT_FOUND
    assert conflicts[0].available_versions == ()


def test_adapter_maps_invalid_package_version() -> None:
    """An invalid package version becomes an invalid-version conflict."""

    invalid_package = PluginPackage(
        plugin_id="familyos.security",
        version="invalid",
        source="official",
    )
    plan = ResolutionPlan(
        skipped_packages=[
            invalid_package,
        ],
        diagnostics=[
            ResolutionDiagnostic(
                plugin="familyos.security",
                message=("Plugin package version 'invalid' is invalid."),
            ),
        ],
    )

    conflicts = ResolutionConflictAdapter().adapt(
        plan,
    )

    assert len(conflicts) == 1
    assert conflicts[0].plugin == "familyos.security"
    assert conflicts[0].reason is ConflictReason.INVALID_VERSION
    assert conflicts[0].available_versions == ("invalid",)


def test_adapter_maps_missing_compatible_version() -> None:
    """An unsatisfied constraint becomes a compatibility conflict."""

    first_package = PluginPackage(
        plugin_id="familyos.crypto",
        version="1.0.0",
        source="official",
    )
    second_package = PluginPackage(
        plugin_id="familyos.crypto",
        version="2.0.0",
        source="official",
    )
    plan = ResolutionPlan(
        skipped_packages=[
            first_package,
            second_package,
        ],
        diagnostics=[
            ResolutionDiagnostic(
                plugin="familyos.crypto",
                message=(
                    "No available plugin version satisfies constraint set '>=3.0.0'."
                ),
            ),
        ],
    )

    conflicts = ResolutionConflictAdapter().adapt(
        plan,
    )

    assert len(conflicts) == 1
    assert conflicts[0].plugin == "familyos.crypto"
    assert conflicts[0].reason is ConflictReason.NO_COMPATIBLE_VERSION
    assert conflicts[0].available_versions == (
        "1.0.0",
        "2.0.0",
    )


def test_adapter_maps_plan_without_valid_semantic_version() -> None:
    """An absence of valid versions becomes a compatibility conflict."""

    plan = ResolutionPlan(
        skipped_packages=[
            PluginPackage(
                plugin_id="familyos.security",
                version="latest",
                source="official",
            ),
        ],
        diagnostics=[
            ResolutionDiagnostic(
                plugin="familyos.security",
                message=("No package with a valid semantic version is available."),
            ),
        ],
    )

    conflicts = ResolutionConflictAdapter().adapt(
        plan,
    )

    assert len(conflicts) == 1
    assert conflicts[0].reason is ConflictReason.NO_COMPATIBLE_VERSION
    assert conflicts[0].available_versions == ("latest",)


def test_adapter_preserves_multiple_known_conflicts() -> None:
    """Known resolver diagnostics are adapted in their original order."""

    plan = ResolutionPlan(
        diagnostics=[
            ResolutionDiagnostic(
                plugin="familyos.security",
                message=("Required plugin dependency is not available."),
            ),
            ResolutionDiagnostic(
                plugin="familyos.backup",
                message=("Required plugin dependency is not available."),
            ),
        ],
    )

    conflicts = ResolutionConflictAdapter().adapt(
        plan,
    )

    assert tuple(conflict.plugin for conflict in conflicts) == (
        "familyos.security",
        "familyos.backup",
    )


def test_adapter_ignores_unknown_resolution_diagnostic() -> None:
    """An unknown resolver message is not incorrectly classified."""

    plan = ResolutionPlan(
        diagnostics=[
            ResolutionDiagnostic(
                plugin="familyos.security",
                message="Unexpected resolver information.",
            ),
        ],
    )

    conflicts = ResolutionConflictAdapter().adapt(
        plan,
    )

    assert conflicts == ()


def test_adapter_removes_duplicate_skipped_versions() -> None:
    """Available conflict versions are unique and preserve order."""

    duplicate = PluginPackage(
        plugin_id="familyos.crypto",
        version="1.0.0",
        source="official",
    )
    plan = ResolutionPlan(
        skipped_packages=[
            duplicate,
            duplicate,
            PluginPackage(
                plugin_id="familyos.crypto",
                version="2.0.0",
                source="community",
            ),
        ],
        diagnostics=[
            ResolutionDiagnostic(
                plugin="familyos.crypto",
                message=(
                    "No available plugin version satisfies constraint set '>=3.0.0'."
                ),
            ),
        ],
    )

    conflicts = ResolutionConflictAdapter().adapt(
        plan,
    )

    assert conflicts[0].available_versions == (
        "1.0.0",
        "2.0.0",
    )


def test_adapter_ignores_skipped_versions_from_other_plugins() -> None:
    """A conflict includes only versions belonging to its plugin."""

    plan = ResolutionPlan(
        skipped_packages=[
            PluginPackage(
                plugin_id="familyos.crypto",
                version="1.0.0",
                source="official",
            ),
            PluginPackage(
                plugin_id="familyos.storage",
                version="4.0.0",
                source="official",
            ),
        ],
        diagnostics=[
            ResolutionDiagnostic(
                plugin="familyos.crypto",
                message=(
                    "No available plugin version satisfies constraint set '>=3.0.0'."
                ),
            ),
        ],
    )

    conflicts = ResolutionConflictAdapter().adapt(
        plan,
    )

    assert conflicts[0].available_versions == ("1.0.0",)


def test_adapter_matches_skipped_versions_by_plugin_id() -> None:
    """Conflict matching should use canonical plugin identity."""

    plan = ResolutionPlan(
        skipped_packages=[
            PluginPackage(
                plugin_id="familyos.crypto",
                version="1.0.0",
                source="official",
            ),
            PluginPackage(
                plugin_id="familyos.storage",
                version="2.0.0",
                source="official",
            ),
        ],
        diagnostics=[
            ResolutionDiagnostic(
                plugin="familyos.crypto",
                message=(
                    "No available plugin version satisfies constraint set '>=3.0.0'."
                ),
            ),
        ],
    )

    conflicts = ResolutionConflictAdapter().adapt(
        plan,
    )

    assert conflicts[0].plugin == "familyos.crypto"
    assert conflicts[0].available_versions == ("1.0.0",)
