"""Tests for plugin conflict reasons."""

from familyos_cli.plugins.ecosystem.diagnostics import ConflictReason


def test_conflict_reason_values() -> None:
    """Conflict reasons expose stable serialized values."""

    assert (
        ConflictReason.INCOMPATIBLE_CONSTRAINTS
        == "incompatible_constraints"
    )
    assert ConflictReason.NO_COMPATIBLE_VERSION == "no_compatible_version"
    assert ConflictReason.PACKAGE_NOT_FOUND == "package_not_found"
    assert ConflictReason.INVALID_VERSION == "invalid_version"
