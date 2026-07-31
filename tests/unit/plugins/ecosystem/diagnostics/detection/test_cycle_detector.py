"""Tests for the dependency cycle detector."""

from familyos_cli.plugins.ecosystem.diagnostics import (
    CycleDetector,
    DependencyCycle,
)


class FakeCycleDetectionSource:
    """Fake dependency graph source."""

    def __init__(
        self,
        graph: dict[str, tuple[str, ...]],
    ) -> None:
        self._graph = graph

    def plugins(self) -> tuple[str, ...]:
        return tuple(
            self._graph,
        )

    def dependencies_of(
        self,
        plugin: str,
    ) -> tuple[str, ...]:
        return self._graph.get(
            plugin,
            (),
        )


def test_cycle_detector_finds_simple_cycle() -> None:
    """The detector finds a direct dependency cycle."""

    detector = CycleDetector(
        FakeCycleDetectionSource(
            {
                "security": ("crypto",),
                "crypto": ("security",),
            },
        ),
    )

    cycles = detector.detect()

    assert cycles == (
        DependencyCycle(
            path=(
                "crypto",
                "security",
                "crypto",
            ),
        ),
    )


def test_cycle_detector_finds_long_cycle() -> None:
    """The detector finds a multi-node cycle."""

    detector = CycleDetector(
        FakeCycleDetectionSource(
            {
                "a": ("b",),
                "b": ("c",),
                "c": ("a",),
            },
        ),
    )

    cycles = detector.detect()

    assert cycles == (
        DependencyCycle(
            path=(
                "a",
                "b",
                "c",
                "a",
            ),
        ),
    )


def test_cycle_detector_ignores_acyclic_graph() -> None:
    """The detector returns no cycles for a valid graph."""

    detector = CycleDetector(
        FakeCycleDetectionSource(
            {
                "security": ("crypto",),
                "crypto": (),
            },
        ),
    )

    assert detector.detect() == ()


def test_cycle_detector_detects_self_cycle() -> None:
    """The detector detects direct self dependencies."""

    detector = CycleDetector(
        FakeCycleDetectionSource(
            {
                "security": ("security",),
            },
        ),
    )

    assert detector.detect() == (
        DependencyCycle(
            path=(
                "security",
                "security",
            ),
        ),
    )


def test_cycle_detector_does_not_duplicate_cycles() -> None:
    """The detector does not return duplicate cycle paths."""

    detector = CycleDetector(
        FakeCycleDetectionSource(
            {
                "a": ("b",),
                "b": ("a",),
                "c": ("b",),
            },
        ),
    )

    cycles = detector.detect()

    assert len(cycles) == 1
