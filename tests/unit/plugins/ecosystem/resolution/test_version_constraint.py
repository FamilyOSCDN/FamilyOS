"""Tests for plugin version constraints."""

import pytest

from familyos_cli.plugins.ecosystem.resolution.plugin_version import (
    PluginVersion,
)
from familyos_cli.plugins.ecosystem.resolution.version_constraint import (
    VersionConstraint,
)
from familyos_cli.plugins.ecosystem.resolution.version_operator import (
    VersionOperator,
)


@pytest.mark.parametrize(
    (
        "value",
        "expected_operator",
        "expected_version",
    ),
    [
        (
            "==1.2.3",
            VersionOperator.EQUAL,
            "1.2.3",
        ),
        (
            ">1.2.3",
            VersionOperator.GREATER,
            "1.2.3",
        ),
        (
            ">=1.2.3",
            VersionOperator.GREATER_OR_EQUAL,
            "1.2.3",
        ),
        (
            "<1.2.3",
            VersionOperator.LOWER,
            "1.2.3",
        ),
        (
            "<=1.2.3",
            VersionOperator.LOWER_OR_EQUAL,
            "1.2.3",
        ),
        (
            "^1.2.3",
            VersionOperator.COMPATIBLE,
            "1.2.3",
        ),
        (
            "~1.2.3",
            VersionOperator.APPROXIMATE,
            "1.2.3",
        ),
    ],
)
def test_version_constraint_parse(
    value: str,
    expected_operator: VersionOperator,
    expected_version: str,
) -> None:
    """Supported constraints should be parsed."""

    constraint = VersionConstraint.parse(value)

    assert constraint.operator is expected_operator
    assert str(constraint.version) == expected_version
    assert str(constraint) == value


@pytest.mark.parametrize(
    (
        "constraint_value",
        "version_value",
        "expected",
    ),
    [
        (
            "==1.2.3",
            "1.2.3",
            True,
        ),
        (
            "==1.2.3",
            "1.2.4",
            False,
        ),
        (
            ">1.2.3",
            "1.2.4",
            True,
        ),
        (
            ">1.2.3",
            "1.2.3",
            False,
        ),
        (
            ">=1.2.3",
            "1.2.3",
            True,
        ),
        (
            ">=1.2.3",
            "2.0.0",
            True,
        ),
        (
            "<1.2.3",
            "1.2.2",
            True,
        ),
        (
            "<1.2.3",
            "1.2.3",
            False,
        ),
        (
            "<=1.2.3",
            "1.2.3",
            True,
        ),
        (
            "<=1.2.3",
            "2.0.0",
            False,
        ),
    ],
)
def test_version_constraint_evaluation(
    constraint_value: str,
    version_value: str,
    expected: bool,
) -> None:
    """Constraints should evaluate comparable plugin versions."""

    constraint = VersionConstraint.parse(
        constraint_value,
    )

    version = PluginVersion.parse(
        version_value,
    )

    assert constraint.is_satisfied_by(version) is expected


@pytest.mark.parametrize(
    (
        "constraint_value",
        "version_value",
        "expected",
    ),
    [
        (
            "^1.2.3",
            "1.2.3",
            True,
        ),
        (
            "^1.2.3",
            "1.9.9",
            True,
        ),
        (
            "^1.2.3",
            "2.0.0",
            False,
        ),
        (
            "^0.2.3",
            "0.2.9",
            True,
        ),
        (
            "^0.2.3",
            "0.3.0",
            False,
        ),
        (
            "^0.0.3",
            "0.0.3",
            True,
        ),
        (
            "^0.0.3",
            "0.0.4",
            False,
        ),
        (
            "^1.2.3",
            "1.2.3-alpha",
            False,
        ),
    ],
)
def test_compatible_constraint_evaluation(
    constraint_value: str,
    version_value: str,
    expected: bool,
) -> None:
    """Caret constraints should use the first non-zero component."""

    constraint = VersionConstraint.parse(
        constraint_value,
    )

    version = PluginVersion.parse(
        version_value,
    )

    assert constraint.is_satisfied_by(version) is expected


@pytest.mark.parametrize(
    (
        "constraint_value",
        "version_value",
        "expected",
    ),
    [
        (
            "~1.2.3",
            "1.2.3",
            True,
        ),
        (
            "~1.2.3",
            "1.2.9",
            True,
        ),
        (
            "~1.2.3",
            "1.3.0",
            False,
        ),
        (
            "~0.2.3",
            "0.2.9",
            True,
        ),
        (
            "~0.2.3",
            "0.3.0",
            False,
        ),
        (
            "~1.2.3",
            "2.0.0",
            False,
        ),
    ],
)
def test_approximate_constraint_evaluation(
    constraint_value: str,
    version_value: str,
    expected: bool,
) -> None:
    """Tilde constraints should allow patch-level evolution."""

    constraint = VersionConstraint.parse(
        constraint_value,
    )

    version = PluginVersion.parse(
        version_value,
    )

    assert constraint.is_satisfied_by(version) is expected


def test_semantic_constraint_preserves_build_metadata_rules() -> None:
    """Build metadata should not affect constraint evaluation."""

    constraint = VersionConstraint.parse(
        "==1.2.3+build.1",
    )

    assert constraint.is_satisfied_by(
        PluginVersion.parse(
            "1.2.3+build.2",
        ),
    )


@pytest.mark.parametrize(
    "value",
    [
        "",
        "1.2.3",
        "=>1.2.3",
        ">=",
        "==",
        "^",
        "~",
        ">=1.2",
        "unsupported1.2.3",
    ],
)
def test_invalid_version_constraints_are_rejected(
    value: str,
) -> None:
    """Invalid constraints should raise explicit errors."""

    with pytest.raises(ValueError):
        VersionConstraint.parse(value)
