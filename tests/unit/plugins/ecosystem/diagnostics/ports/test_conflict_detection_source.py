"""Tests for the conflict detection source protocol."""

from __future__ import annotations

from familyos_cli.plugins.ecosystem.diagnostics.ports import (
    ConflictDetectionSource,
)


class FakeConflictDetectionSource:
    """Simple implementation of the protocol."""

    def plugins(self) -> tuple[str, ...]:
        return (
            "familyos.security",
            "familyos.backup",
        )

    def candidate_versions(
        self,
        plugin: str,
    ) -> tuple[str, ...]:
        return ("1.0.0",)

    def constraints_for(
        self,
        plugin: str,
    ) -> tuple[str, ...]:
        return (">=1.0.0",)

    def dependents_of(
        self,
        plugin: str,
    ) -> tuple[str, ...]:
        return ("familyos.application",)


def test_conflict_detection_source_protocol() -> None:
    """A concrete implementation satisfies the protocol."""

    source: ConflictDetectionSource = FakeConflictDetectionSource()

    assert source.plugins() == (
        "familyos.security",
        "familyos.backup",
    )
    assert source.candidate_versions(
        "familyos.security",
    ) == ("1.0.0",)
    assert source.constraints_for(
        "familyos.security",
    ) == (">=1.0.0",)
    assert source.dependents_of(
        "familyos.security",
    ) == ("familyos.application",)
