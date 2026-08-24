"""Tests for canonical Testing Framework source-state authority."""

from __future__ import annotations

import pytest

from familyos_cli.application.testing.testing_source_state import (
    TestingSourceState as CanonicalTestingSourceState,
)


def test_source_state_preserves_revision_and_dirty_state() -> None:
    state = CanonicalTestingSourceState(
        revision="0123456789abcdef0123456789abcdef01234567",
        dirty=False,
    )

    assert state.revision == "0123456789abcdef0123456789abcdef01234567"
    assert state.dirty is False


def test_source_state_allows_unavailable_repository_state() -> None:
    state = CanonicalTestingSourceState(
        revision=None,
        dirty=None,
    )

    assert state.revision is None
    assert state.dirty is None


def test_source_state_is_immutable() -> None:
    state = CanonicalTestingSourceState(
        revision="0123456789abcdef0123456789abcdef01234567",
        dirty=False,
    )

    with pytest.raises(AttributeError):
        state.revision = "replacement"  # type: ignore[misc]
