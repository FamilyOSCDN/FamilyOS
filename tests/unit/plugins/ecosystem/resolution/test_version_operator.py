"""Tests for version operators."""

from familyos_cli.plugins.ecosystem.resolution.version_operator import (
    VersionOperator,
)


def test_version_operator_values() -> None:
    """Supported operators should expose their symbols."""

    assert VersionOperator.EQUAL.value == "=="

    assert VersionOperator.GREATER.value == ">"

    assert VersionOperator.GREATER_OR_EQUAL.value == ">="

    assert VersionOperator.LOWER.value == "<"

    assert VersionOperator.LOWER_OR_EQUAL.value == "<="

    assert VersionOperator.COMPATIBLE.value == "^"

    assert VersionOperator.APPROXIMATE.value == "~"
