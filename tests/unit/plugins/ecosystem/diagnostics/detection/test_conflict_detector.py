"""Tests for the conflict detector."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.detection import (
    ConflictDetector,
)
from familyos_cli.plugins.ecosystem.diagnostics.ports import (
    ConflictDetectionSource,
)


class FakeConflictDetectionSource:
    """Fake source used by detector tests."""

    def plugins(self) -> tuple[str, ...]:
        return ()

    def candidate_versions(
        self,
        plugin: str,
    ) -> tuple[str, ...]:
        return ()

    def constraints_for(
        self,
        plugin: str,
    ) -> tuple[str, ...]:
        return ()

    def dependents_of(
        self,
        plugin: str,
    ) -> tuple[str, ...]:
        return ()


def test_conflict_detector_creation() -> None:
    """The detector accepts a detection source."""

    source: ConflictDetectionSource = FakeConflictDetectionSource()

    detector = ConflictDetector(source)

    assert detector is not None


def test_conflict_detector_returns_no_conflicts_yet() -> None:
    """The initial detector returns no conflicts."""

    detector = ConflictDetector(
        FakeConflictDetectionSource(),
    )

    assert detector.detect() == ()
