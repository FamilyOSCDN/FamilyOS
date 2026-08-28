from datetime import UTC, datetime
from unittest.mock import Mock
from uuid import UUID

import pytest

from familyos_cli.application.family import (
    EstablishRelationship,
    FamilyNotFoundError,
    PersonNotFoundError,
)
from familyos_cli.application.ports.family import RelationshipConflictError
from familyos_cli.domain.family import (
    FamilyId,
    Relationship,
    RelationshipType,
)
from familyos_cli.domain.person import PersonId

NOW = datetime(2026, 8, 28, 8, 0, tzinfo=UTC)


def _family_id() -> FamilyId:
    return FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))


def _low() -> PersonId:
    return PersonId(UUID("00000000-0000-4000-8000-000000000001"))


def _high() -> PersonId:
    return PersonId(UUID("ffffffff-ffff-4fff-8fff-ffffffffffff"))


def _uc() -> tuple[EstablishRelationship, Mock]:
    family_repo = Mock()
    family_repo.get.return_value = object()
    person_repo = Mock()
    person_repo.get.return_value = object()
    relationship_repo = Mock()
    relationship_repo.get.return_value = None
    return (
        EstablishRelationship(
            family_repo,
            person_repo,
            relationship_repo,
            clock=lambda: NOW,
        ),
        relationship_repo,
    )


def test_establish_normalizes_child_of_before_conflict_and_persistence() -> None:
    use_case, repo = _uc()
    result = use_case.execute(
        _family_id(), _high(), _low(), RelationshipType.CHILD_OF
    )

    assert result.relationship.relationship_type is RelationshipType.PARENT_OF
    assert result.relationship.source_person_id == _low()
    assert result.relationship.target_person_id == _high()
    assert result.event.source_person_id == _low()
    assert result.event.target_person_id == _high()
    assert result.event.relationship_type is RelationshipType.PARENT_OF
    assert result.event.occurred_at == NOW
    repo.get.assert_called_once_with(
        _family_id(), _low(), _high(), RelationshipType.PARENT_OF
    )
    repo.save.assert_called_once_with(result.relationship)


@pytest.mark.parametrize(
    "relationship_type",
    [RelationshipType.SPOUSE_OF, RelationshipType.SIBLING_OF],
)
def test_establish_normalizes_reversed_symmetric_input(
    relationship_type: RelationshipType,
) -> None:
    use_case, repo = _uc()
    result = use_case.execute(_family_id(), _high(), _low(), relationship_type)

    assert result.relationship.source_person_id == _low()
    assert result.relationship.target_person_id == _high()
    repo.get.assert_called_once_with(
        _family_id(), _low(), _high(), relationship_type
    )


def test_establish_rejects_duplicate_normalized_continuity() -> None:
    use_case, repo = _uc()
    repo.get.return_value = Relationship.establish(
        _family_id(), _low(), _high(), RelationshipType.PARENT_OF
    )
    with pytest.raises(RelationshipConflictError):
        use_case.execute(
            _family_id(), _high(), _low(), RelationshipType.CHILD_OF
        )
    repo.save.assert_not_called()


def test_establish_requires_family() -> None:
    family_repo = Mock()
    family_repo.get.return_value = None
    person_repo = Mock()
    relationship_repo = Mock()
    use_case = EstablishRelationship(
        family_repo, person_repo, relationship_repo, clock=lambda: NOW
    )
    with pytest.raises(FamilyNotFoundError):
        use_case.execute(
            _family_id(), _low(), _high(), RelationshipType.PARENT_OF
        )
    person_repo.get.assert_not_called()
    relationship_repo.get.assert_not_called()


def test_establish_requires_both_persons() -> None:
    family_repo = Mock()
    family_repo.get.return_value = object()
    person_repo = Mock()
    person_repo.get.side_effect = [object(), None]
    relationship_repo = Mock()
    use_case = EstablishRelationship(
        family_repo, person_repo, relationship_repo, clock=lambda: NOW
    )
    with pytest.raises(PersonNotFoundError):
        use_case.execute(
            _family_id(), _low(), _high(), RelationshipType.PARENT_OF
        )
    relationship_repo.get.assert_not_called()


def test_establish_rejects_self_relationship_before_lookup() -> None:
    family_repo = Mock()
    person_repo = Mock()
    relationship_repo = Mock()
    use_case = EstablishRelationship(
        family_repo, person_repo, relationship_repo, clock=lambda: NOW
    )
    with pytest.raises(ValueError, match="must be distinct"):
        use_case.execute(
            _family_id(), _low(), _low(), RelationshipType.SIBLING_OF
        )
    family_repo.get.assert_not_called()


def test_establish_rejects_naive_time_before_save() -> None:
    family_repo = Mock()
    family_repo.get.return_value = object()
    person_repo = Mock()
    person_repo.get.return_value = object()
    relationship_repo = Mock()
    relationship_repo.get.return_value = None
    use_case = EstablishRelationship(
        family_repo,
        person_repo,
        relationship_repo,
        clock=lambda: datetime(2026, 8, 28, 8, 0),
    )
    with pytest.raises(ValueError, match="timezone-aware"):
        use_case.execute(
            _family_id(), _low(), _high(), RelationshipType.PARENT_OF
        )
    relationship_repo.save.assert_not_called()
