from datetime import UTC, datetime
from unittest.mock import Mock
from uuid import UUID

import pytest

from familyos_cli.application.family import (
    EndRelationship,
    RelationshipNotFoundError,
)
from familyos_cli.application.ports.family import RelationshipConflictError
from familyos_cli.domain.family import (
    FamilyId,
    InvalidRelationshipTransitionError,
    Relationship,
    RelationshipType,
)
from familyos_cli.domain.person import PersonId

NOW = datetime(2026, 8, 28, 9, 0, tzinfo=UTC)


def _family_id() -> FamilyId:
    return FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))


def _low() -> PersonId:
    return PersonId(UUID("00000000-0000-4000-8000-000000000001"))


def _high() -> PersonId:
    return PersonId(UUID("ffffffff-ffff-4fff-8fff-ffffffffffff"))


def test_end_normalizes_child_of_and_persists_ended_continuity() -> None:
    repo = Mock()
    established = Relationship.establish(
        _family_id(), _low(), _high(), RelationshipType.PARENT_OF
    )
    repo.get.return_value = established
    result = EndRelationship(repo, clock=lambda: NOW).execute(
        _family_id(), _high(), _low(), RelationshipType.CHILD_OF
    )

    assert result.relationship == established.end()
    assert result.event.source_person_id == _low()
    assert result.event.target_person_id == _high()
    assert result.event.relationship_type is RelationshipType.PARENT_OF
    assert result.event.occurred_at == NOW
    repo.get.assert_called_once_with(
        _family_id(), _low(), _high(), RelationshipType.PARENT_OF
    )
    repo.save.assert_called_once_with(result.relationship, result.event)


def test_end_raises_not_found_for_absence() -> None:
    repo = Mock()
    repo.get.return_value = None
    command = EndRelationship(repo, clock=lambda: NOW)
    with pytest.raises(RelationshipNotFoundError):
        command.execute(
            _family_id(), _low(), _high(), RelationshipType.PARENT_OF
        )
    repo.save.assert_not_called()


def test_end_already_ended_fails_before_clock() -> None:
    repo = Mock()
    repo.get.return_value = Relationship.establish(
        _family_id(), _low(), _high(), RelationshipType.PARENT_OF
    ).end()
    clock = Mock(return_value=NOW)
    command = EndRelationship(repo, clock=clock)

    with pytest.raises(InvalidRelationshipTransitionError):
        command.execute(
            _family_id(), _low(), _high(), RelationshipType.PARENT_OF
        )

    clock.assert_not_called()
    repo.save.assert_not_called()


def test_end_rejects_naive_time_before_save() -> None:
    repo = Mock()
    repo.get.return_value = Relationship.establish(
        _family_id(), _low(), _high(), RelationshipType.PARENT_OF
    )
    command = EndRelationship(
        repo, clock=lambda: datetime(2026, 8, 28, 9, 0)
    )
    with pytest.raises(ValueError, match="timezone-aware"):
        command.execute(
            _family_id(), _low(), _high(), RelationshipType.PARENT_OF
        )
    repo.save.assert_not_called()


def test_end_propagates_persistence_conflict() -> None:
    repo = Mock()
    repo.get.return_value = Relationship.establish(
        _family_id(), _low(), _high(), RelationshipType.PARENT_OF
    )
    repo.save.side_effect = RelationshipConflictError("race")
    command = EndRelationship(repo, clock=lambda: NOW)

    with pytest.raises(RelationshipConflictError, match="race"):
        command.execute(
            _family_id(), _low(), _high(), RelationshipType.PARENT_OF
        )


@pytest.mark.parametrize(
    "relationship_type",
    [RelationshipType.SPOUSE_OF, RelationshipType.SIBLING_OF],
)
def test_end_normalizes_reversed_symmetric(
    relationship_type: RelationshipType,
) -> None:
    repo = Mock()
    repo.get.return_value = Relationship.establish(
        _family_id(), _low(), _high(), relationship_type
    )
    EndRelationship(repo, clock=lambda: NOW).execute(
        _family_id(), _high(), _low(), relationship_type
    )
    repo.get.assert_called_once_with(
        _family_id(), _low(), _high(), relationship_type
    )
