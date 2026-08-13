"""Tests for plugin conflict reasons."""

from familyos_cli.plugins.ecosystem.diagnostics import ConflictReason


def test_conflict_reason_values() -> None:
    """Conflict reasons expose stable serialized values."""

    assert (
        ConflictReason.INCOMPATIBLE_CONSTRAINTS.value
        == "incompatible_constraints"
    )
    assert ConflictReason.NO_COMPATIBLE_VERSION.value == "no_compatible_version"
    assert ConflictReason.PACKAGE_NOT_FOUND.value == "package_not_found"
    assert ConflictReason.INVALID_VERSION.value == "invalid_version"
