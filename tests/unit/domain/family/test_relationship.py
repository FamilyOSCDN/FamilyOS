"""Tests for canonical Family Relationship semantics."""

from dataclasses import FrozenInstanceError
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.domain.family import (
    FamilyId,
    InvalidRelationshipTransitionError,
    Relationship,
    RelationshipState,
    RelationshipType,
)
from familyos_cli.domain.person import PersonId


def _family_id() -> FamilyId:
    return FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))


def _low_person_id() -> PersonId:
    return PersonId(UUID("00000000-0000-4000-8000-000000000001"))


def _high_person_id() -> PersonId:
    return PersonId(UUID("ffffffff-ffff-4fff-8fff-ffffffffffff"))


def test_relationship_type_taxonomy_is_exact() -> None:
    assert list(RelationshipType) == [
        RelationshipType.PARENT_OF,
        RelationshipType.CHILD_OF,
        RelationshipType.SPOUSE_OF,
        RelationshipType.SIBLING_OF,
    ]


def test_relationship_state_taxonomy_is_exact() -> None:
    assert list(RelationshipState) == [
        RelationshipState.ESTABLISHED,
        RelationshipState.ENDED,
    ]


def test_establish_parent_of_preserves_direction() -> None:
    relationship = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.PARENT_OF,
    )

    assert relationship.family_id == _family_id()
    assert relationship.source_person_id == _low_person_id()
    assert relationship.target_person_id == _high_person_id()
    assert relationship.relationship_type is RelationshipType.PARENT_OF
    assert relationship.state is RelationshipState.ESTABLISHED


def test_child_of_normalizes_to_parent_of_continuity() -> None:
    parent_view = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.PARENT_OF,
    )
    child_view = Relationship.establish(
        _family_id(),
        _high_person_id(),
        _low_person_id(),
        RelationshipType.CHILD_OF,
    )

    assert child_view == parent_view


@pytest.mark.parametrize(
    "relationship_type",
    [
        RelationshipType.SPOUSE_OF,
        RelationshipType.SIBLING_OF,
    ],
)
def test_symmetric_relationships_normalize_uuid_order(
    relationship_type: RelationshipType,
) -> None:
    forward = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        relationship_type,
    )
    reversed_view = Relationship.establish(
        _family_id(),
        _high_person_id(),
        _low_person_id(),
        relationship_type,
    )

    assert forward == reversed_view
    assert forward.source_person_id == _low_person_id()
    assert forward.target_person_id == _high_person_id()


def test_relationship_identity_is_scoped_by_family() -> None:
    first = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.SPOUSE_OF,
    )
    other_family = Relationship.establish(
        FamilyId(UUID("87654321-4321-4321-8321-cba987654321")),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.SPOUSE_OF,
    )

    assert first != other_family


@pytest.mark.parametrize("relationship_type", list(RelationshipType))
def test_self_relationship_is_rejected(
    relationship_type: RelationshipType,
) -> None:
    with pytest.raises(
        ValueError,
        match="Relationship source and target Persons must be distinct",
    ):
        Relationship.establish(
            _family_id(),
            _low_person_id(),
            _low_person_id(),
            relationship_type,
        )


def test_end_transitions_established_to_ended_and_preserves_identity() -> None:
    established = Relationship.establish(
        _family_id(),
        _high_person_id(),
        _low_person_id(),
        RelationshipType.SPOUSE_OF,
    )

    ended = established.end()

    assert established.state is RelationshipState.ESTABLISHED
    assert ended.state is RelationshipState.ENDED
    assert ended.family_id == established.family_id
    assert ended.source_person_id == established.source_person_id
    assert ended.target_person_id == established.target_person_id
    assert ended.relationship_type is established.relationship_type


def test_ended_relationship_is_terminal() -> None:
    ended = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.SIBLING_OF,
    ).end()

    with pytest.raises(InvalidRelationshipTransitionError):
        ended.end()


def test_relationship_is_immutable() -> None:
    relationship = Relationship.establish(
        _family_id(),
        _low_person_id(),
        _high_person_id(),
        RelationshipType.PARENT_OF,
    )

    with pytest.raises(FrozenInstanceError):
        relationship.state = RelationshipState.ENDED  # type: ignore[misc]


def test_direct_child_of_canonical_state_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="canonical state must not store CHILD_OF",
    ):
        Relationship(
            family_id=_family_id(),
            source_person_id=_high_person_id(),
            target_person_id=_low_person_id(),
            relationship_type=RelationshipType.CHILD_OF,
            state=RelationshipState.ESTABLISHED,
        )


@pytest.mark.parametrize(
    "relationship_type",
    [
        RelationshipType.SPOUSE_OF,
        RelationshipType.SIBLING_OF,
    ],
)
def test_direct_reversed_symmetric_canonical_state_is_rejected(
    relationship_type: RelationshipType,
) -> None:
    with pytest.raises(
        ValueError,
        match="canonical UUID order",
    ):
        Relationship(
            family_id=_family_id(),
            source_person_id=_high_person_id(),
            target_person_id=_low_person_id(),
            relationship_type=relationship_type,
            state=RelationshipState.ESTABLISHED,
        )


def test_establish_rejects_invalid_types() -> None:
    with pytest.raises(TypeError, match="family_id must be a FamilyId"):
        Relationship.establish(
            cast(FamilyId, "family-001"),
            _low_person_id(),
            _high_person_id(),
            RelationshipType.PARENT_OF,
        )

    with pytest.raises(TypeError, match="source_person_id must be a PersonId"):
        Relationship.establish(
            _family_id(),
            cast(PersonId, "person-a"),
            _high_person_id(),
            RelationshipType.PARENT_OF,
        )

    with pytest.raises(TypeError, match="target_person_id must be a PersonId"):
        Relationship.establish(
            _family_id(),
            _low_person_id(),
            cast(PersonId, "person-b"),
            RelationshipType.PARENT_OF,
        )

    with pytest.raises(
        TypeError,
        match="relationship_type must be a RelationshipType",
    ):
        Relationship.establish(
            _family_id(),
            _low_person_id(),
            _high_person_id(),
            cast(RelationshipType, "parent_of"),
        )
