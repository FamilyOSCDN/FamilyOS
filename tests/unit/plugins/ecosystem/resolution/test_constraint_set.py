"""Tests for constraint sets."""

import pytest

from familyos_cli.plugins.ecosystem.resolution.constraint_set import (
    ConstraintSet,
)
from familyos_cli.plugins.ecosystem.resolution.plugin_version import (
    PluginVersion,
)


def test_constraint_set_parse() -> None:
    """Constraint sets should be parsed."""

    constraint_set = ConstraintSet.parse(
        ">=1.2.0,<2.0.0",
    )

    assert len(
        constraint_set.constraints,
    ) == 2

    assert (
        str(constraint_set)
        == ">=1.2.0,<2.0.0"
    )


@pytest.mark.parametrize(
    (
        "version",
        "expected",
    ),
    [
        (
            "1.2.0",
            True,
        ),
        (
            "1.8.4",
            True,
        ),
        (
            "2.0.0",
            False,
        ),
        (
            "1.1.9",
            False,
        ),
    ],
)
def test_constraint_set_evaluation(
    version: str,
    expected: bool,
) -> None:
    """All constraints must be satisfied."""

    constraint_set = ConstraintSet.parse(
        ">=1.2.0,<2.0.0",
    )

    assert (
        constraint_set.is_satisfied_by(
            PluginVersion.parse(
                version,
            ),
        )
        is expected
    )


def test_empty_constraint_set_is_rejected() -> None:
    """Empty constraint sets are invalid."""

    with pytest.raises(
        ValueError,
    ):
        ConstraintSet.parse("")
