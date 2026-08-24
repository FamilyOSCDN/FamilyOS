"""Tests for the Testing Framework source-state provider port."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.ports.testing.testing_source_state_provider import (
    TestingSourceStateProviderPort,
)
from familyos_cli.application.testing.testing_source_state import (
    TestingSourceState as CanonicalTestingSourceState,
)


class _Provider(TestingSourceStateProviderPort):
    def observe(
        self,
        *,
        project_root: Path,
    ) -> CanonicalTestingSourceState:
        return CanonicalTestingSourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=False,
        )


def test_port_exposes_testing_owned_source_state(
    tmp_path: Path,
) -> None:
    result = _Provider().observe(
        project_root=tmp_path,
    )

    assert result.revision == (
        "0123456789abcdef0123456789abcdef01234567"
    )
    assert result.dirty is False
