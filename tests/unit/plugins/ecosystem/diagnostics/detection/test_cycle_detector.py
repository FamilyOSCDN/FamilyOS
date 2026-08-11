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
                "familyos.security": ("familyos.crypto",),
                "familyos.crypto": ("familyos.security",),
            },
        ),
    )

    cycles = detector.detect()

    assert cycles == (
        DependencyCycle(
            path=(
                "familyos.crypto",
                "familyos.security",
                "familyos.crypto",
            ),
        ),
    )


def test_cycle_detector_finds_long_cycle() -> None:
    """The detector finds a multi-node cycle."""

    detector = CycleDetector(
        FakeCycleDetectionSource(
            {
                "familyos.plugin_a": ("familyos.plugin_b",),
                "familyos.plugin_b": ("familyos.plugin_c",),
                "familyos.plugin_c": ("familyos.plugin_a",),
            },
        ),
    )

    cycles = detector.detect()

    assert cycles == (
        DependencyCycle(
            path=(
                "familyos.plugin_a",
                "familyos.plugin_b",
                "familyos.plugin_c",
                "familyos.plugin_a",
            ),
        ),
    )


def test_cycle_detector_ignores_acyclic_graph() -> None:
    """The detector returns no cycles for a valid graph."""

    detector = CycleDetector(
        FakeCycleDetectionSource(
            {
                "familyos.security": ("familyos.crypto",),
                "familyos.crypto": (),
            },
        ),
    )

    assert detector.detect() == ()


def test_cycle_detector_detects_self_cycle() -> None:
    """The detector detects direct self dependencies."""

    detector = CycleDetector(
        FakeCycleDetectionSource(
            {
                "familyos.security": ("familyos.security",),
            },
        ),
    )

    assert detector.detect() == (
        DependencyCycle(
            path=(
                "familyos.security",
                "familyos.security",
            ),
        ),
    )


def test_cycle_detector_does_not_duplicate_cycles() -> None:
    """The detector does not return duplicate cycle paths."""

    detector = CycleDetector(
        FakeCycleDetectionSource(
            {
                "familyos.plugin_a": ("familyos.plugin_b",),
                "familyos.plugin_b": ("familyos.plugin_a",),
                "familyos.plugin_c": ("familyos.plugin_b",),
            },
        ),
    )

    cycles = detector.detect()

    assert len(cycles) == 1
