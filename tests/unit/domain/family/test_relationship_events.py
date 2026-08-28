"""Tests for canonical Family Relationship events."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.domain.family import (
    FamilyId,
    FamilyRelationshipEnded,
    FamilyRelationshipEstablished,
    RelationshipType,
)
from familyos_cli.domain.person import PersonId


def _family_id() -> FamilyId:
    return FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))


def _source_person_id() -> PersonId:
    return PersonId(UUID("00000000-0000-4000-8000-000000000001"))


def _target_person_id() -> PersonId:
    return PersonId(UUID("ffffffff-ffff-4fff-8fff-ffffffffffff"))


@pytest.mark.parametrize(
    "event_type",
    [FamilyRelationshipEstablished, FamilyRelationshipEnded],
)
def test_relationship_event_preserves_canonical_payload(event_type: type) -> None:
    occurred_at = datetime(2026, 8, 28, 8, 30, tzinfo=UTC)

    event = event_type(
        family_id=_family_id(),
        source_person_id=_source_person_id(),
        target_person_id=_target_person_id(),
        relationship_type=RelationshipType.PARENT_OF,
        occurred_at=occurred_at,
    )

    assert event.family_id == _family_id()
    assert event.source_person_id == _source_person_id()
    assert event.target_person_id == _target_person_id()
    assert event.relationship_type is RelationshipType.PARENT_OF
    assert event.occurred_at == occurred_at


@pytest.mark.parametrize(
    "event_type,event_name",
    [
        (FamilyRelationshipEstablished, "FamilyRelationshipEstablished"),
        (FamilyRelationshipEnded, "FamilyRelationshipEnded"),
    ],
)
def test_relationship_event_requires_timezone_aware_occurrence_time(
    event_type: type,
    event_name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=f"{event_name} occurrence time must be timezone-aware",
    ):
        event_type(
            family_id=_family_id(),
            source_person_id=_source_person_id(),
            target_person_id=_target_person_id(),
            relationship_type=RelationshipType.PARENT_OF,
            occurred_at=datetime(2026, 8, 28, 8, 30),
        )


def test_relationship_event_is_immutable() -> None:
    event = FamilyRelationshipEstablished(
        family_id=_family_id(),
        source_person_id=_source_person_id(),
        target_person_id=_target_person_id(),
        relationship_type=RelationshipType.SPOUSE_OF,
        occurred_at=datetime(2026, 8, 28, 8, 30, tzinfo=UTC),
    )

    with pytest.raises(FrozenInstanceError):
        event.relationship_type = RelationshipType.SIBLING_OF  # type: ignore[misc]


def test_relationship_event_rejects_invalid_payload_types() -> None:
    occurred_at = datetime(2026, 8, 28, 8, 30, tzinfo=UTC)

    with pytest.raises(TypeError, match="family_id must be a FamilyId"):
        FamilyRelationshipEstablished(
            family_id=cast(FamilyId, "family-001"),
            source_person_id=_source_person_id(),
            target_person_id=_target_person_id(),
            relationship_type=RelationshipType.PARENT_OF,
            occurred_at=occurred_at,
        )

    with pytest.raises(
        TypeError,
        match="source_person_id must be a PersonId",
    ):
        FamilyRelationshipEstablished(
            family_id=_family_id(),
            source_person_id=cast(PersonId, "person-a"),
            target_person_id=_target_person_id(),
            relationship_type=RelationshipType.PARENT_OF,
            occurred_at=occurred_at,
        )

    with pytest.raises(
        TypeError,
        match="target_person_id must be a PersonId",
    ):
        FamilyRelationshipEstablished(
            family_id=_family_id(),
            source_person_id=_source_person_id(),
            target_person_id=cast(PersonId, "person-b"),
            relationship_type=RelationshipType.PARENT_OF,
            occurred_at=occurred_at,
        )

    with pytest.raises(
        TypeError,
        match="relationship_type must be a RelationshipType",
    ):
        FamilyRelationshipEstablished(
            family_id=_family_id(),
            source_person_id=_source_person_id(),
            target_person_id=_target_person_id(),
            relationship_type=cast(RelationshipType, "parent_of"),
            occurred_at=occurred_at,
        )

    with pytest.raises(TypeError, match="occurred_at must be a datetime"):
        FamilyRelationshipEstablished(
            family_id=_family_id(),
            source_person_id=_source_person_id(),
            target_person_id=_target_person_id(),
            relationship_type=RelationshipType.PARENT_OF,
            occurred_at=cast(datetime, "2026-08-28T08:30:00Z"),
        )
