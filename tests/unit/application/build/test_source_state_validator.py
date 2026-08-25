"""Tests for strict Release Candidate source-state validation."""

from __future__ import annotations

from familyos_cli.application.build.source_state import SourceState


def test_identified_clean_source_state_is_valid() -> None:
    from familyos_cli.application.build.source_state_validator import (
        SourceStateValidator,
    )

    result = SourceStateValidator().validate(
        SourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=False,
        )
    )

    assert result.revision_identified
    assert result.working_tree_clean
    assert result.revision_diagnostic is None
    assert result.working_tree_diagnostic is None
    assert result.successful


def test_missing_source_revision_is_invalid() -> None:
    from familyos_cli.application.build.source_state_validator import (
        SourceStateValidator,
    )

    result = SourceStateValidator().validate(
        SourceState(
            revision=None,
            dirty=False,
        )
    )

    assert not result.revision_identified
    assert result.working_tree_clean
    assert result.revision_diagnostic == (
        "source revision is unavailable"
    )
    assert result.working_tree_diagnostic is None
    assert not result.successful


def test_empty_source_revision_is_invalid() -> None:
    from familyos_cli.application.build.source_state_validator import (
        SourceStateValidator,
    )

    result = SourceStateValidator().validate(
        SourceState(
            revision="",
            dirty=False,
        )
    )

    assert not result.revision_identified
    assert result.revision_diagnostic == (
        "source revision is unavailable"
    )
    assert not result.successful


def test_dirty_source_working_tree_is_invalid() -> None:
    from familyos_cli.application.build.source_state_validator import (
        SourceStateValidator,
    )

    result = SourceStateValidator().validate(
        SourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=True,
        )
    )

    assert result.revision_identified
    assert not result.working_tree_clean
    assert result.revision_diagnostic is None
    assert result.working_tree_diagnostic == (
        "source working tree is dirty"
    )
    assert not result.successful


def test_unknown_source_working_tree_state_is_invalid() -> None:
    from familyos_cli.application.build.source_state_validator import (
        SourceStateValidator,
    )

    result = SourceStateValidator().validate(
        SourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=None,
        )
    )

    assert result.revision_identified
    assert not result.working_tree_clean
    assert result.working_tree_diagnostic == (
        "source working tree state is unavailable"
    )
    assert not result.successful
