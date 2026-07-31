"""Tests for the plugin dependency cycle model."""

import pytest

from familyos_cli.plugins.ecosystem.diagnostics import (
    DependencyCycle,
)


def test_dependency_cycle_creation() -> None:
    """A cycle stores its complete closed path."""

    cycle = DependencyCycle(
        path=(
            "security",
            "crypto",
            "storage",
            "security",
        ),
    )

    assert cycle.path == (
        "security",
        "crypto",
        "storage",
        "security",
    )
    assert cycle.plugin == "security"
    assert cycle.length == 3


def test_dependency_cycle_requires_at_least_two_nodes() -> None:
    """A cycle cannot contain only one path element."""

    with pytest.raises(
        ValueError,
        match=(
            "A dependency cycle must contain at least two nodes."
        ),
    ):
        DependencyCycle(
            path=("security",),
        )


def test_dependency_cycle_requires_closed_path() -> None:
    """A cycle path must end at its starting plugin."""

    with pytest.raises(
        ValueError,
        match=(
            "A dependency cycle path must start and end "
            "with the same plugin."
        ),
    ):
        DependencyCycle(
            path=(
                "security",
                "crypto",
                "storage",
            ),
        )


def test_dependency_cycle_supports_self_cycle() -> None:
    """A plugin may depend directly on itself."""

    cycle = DependencyCycle(
        path=(
            "security",
            "security",
        ),
    )

    assert cycle.plugin == "security"
    assert cycle.length == 1
    assert cycle.contains("security")
    assert cycle.unique_plugins() == ("security",)


def test_dependency_cycle_identifies_contained_plugins() -> None:
    """A cycle reports whether a plugin belongs to its path."""

    cycle = DependencyCycle(
        path=(
            "security",
            "crypto",
            "storage",
            "security",
        ),
    )

    assert cycle.contains("security")
    assert cycle.contains("crypto")
    assert cycle.contains("storage")
    assert not cycle.contains("backup")


def test_dependency_cycle_returns_unique_plugins() -> None:
    """Cycle plugins exclude the repeated closing node."""

    cycle = DependencyCycle(
        path=(
            "security",
            "crypto",
            "storage",
            "security",
        ),
    )

    assert cycle.unique_plugins() == (
        "security",
        "crypto",
        "storage",
    )


def test_dependency_cycle_removes_repeated_internal_plugins() -> None:
    """Unique plugins preserve first appearance order."""

    cycle = DependencyCycle(
        path=(
            "security",
            "crypto",
            "security",
        ),
    )

    assert cycle.unique_plugins() == (
        "security",
        "crypto",
    )


def test_dependency_cycle_normalizes_rotation() -> None:
    """Equivalent cycle rotations receive the same representation."""

    first = DependencyCycle(
        path=(
            "security",
            "crypto",
            "storage",
            "security",
        ),
    )
    second = DependencyCycle(
        path=(
            "storage",
            "security",
            "crypto",
            "storage",
        ),
    )

    assert first.normalized() == second.normalized()
    assert first.normalized().path == (
        "crypto",
        "storage",
        "security",
        "crypto",
    )


def test_dependency_cycle_normalization_preserves_self_cycle() -> None:
    """Normalizing a direct self-cycle preserves its path."""

    cycle = DependencyCycle(
        path=(
            "security",
            "security",
        ),
    )

    assert cycle.normalized() == cycle
