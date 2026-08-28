from unittest.mock import Mock
from uuid import UUID

import pytest

from familyos_cli.application.family import GetRelationship
from familyos_cli.domain.family import FamilyId, Relationship, RelationshipType
from familyos_cli.domain.person import PersonId


def _family_id() -> FamilyId:
    return FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))


def _low() -> PersonId:
    return PersonId(UUID("00000000-0000-4000-8000-000000000001"))


def _high() -> PersonId:
    return PersonId(UUID("ffffffff-ffff-4fff-8fff-ffffffffffff"))


def test_get_normalizes_child_of() -> None:
    repo = Mock()
    relationship = Relationship.establish(
        _family_id(), _low(), _high(), RelationshipType.PARENT_OF
    )
    repo.get.return_value = relationship
    query = GetRelationship(repo)

    assert query.execute(
        _family_id(), _high(), _low(), RelationshipType.CHILD_OF
    ) == relationship
    repo.get.assert_called_once_with(
        _family_id(), _low(), _high(), RelationshipType.PARENT_OF
    )


@pytest.mark.parametrize(
    "relationship_type",
    [RelationshipType.SPOUSE_OF, RelationshipType.SIBLING_OF],
)
def test_get_normalizes_reversed_symmetric(
    relationship_type: RelationshipType,
) -> None:
    repo = Mock()
    query = GetRelationship(repo)
    query.execute(_family_id(), _high(), _low(), relationship_type)
    repo.get.assert_called_once_with(
        _family_id(), _low(), _high(), relationship_type
    )


def test_get_returns_none_for_absence() -> None:
    repo = Mock()
    repo.get.return_value = None
    assert GetRelationship(repo).execute(
        _family_id(), _low(), _high(), RelationshipType.PARENT_OF
    ) is None


def test_get_rejects_self_relationship() -> None:
    repo = Mock()
    with pytest.raises(ValueError, match="must be distinct"):
        GetRelationship(repo).execute(
            _family_id(), _low(), _low(), RelationshipType.SPOUSE_OF
        )
    repo.get.assert_not_called()
