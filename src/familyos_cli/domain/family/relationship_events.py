"""Canonical Family Relationship domain events."""

from dataclasses import dataclass
from datetime import datetime

from familyos_cli.domain.family.family_id import FamilyId
from familyos_cli.domain.family.relationship_type import RelationshipType
from familyos_cli.domain.person import PersonId


@dataclass(frozen=True, slots=True)
class FamilyRelationshipEstablished:
    """Canonical fact that one Family Relationship was established."""

    family_id: FamilyId
    source_person_id: PersonId
    target_person_id: PersonId
    relationship_type: RelationshipType
    occurred_at: datetime

    def __post_init__(self) -> None:
        _validate_event(
            "FamilyRelationshipEstablished",
            self.family_id,
            self.source_person_id,
            self.target_person_id,
            self.relationship_type,
            self.occurred_at,
        )


@dataclass(frozen=True, slots=True)
class FamilyRelationshipEnded:
    """Canonical fact that one Family Relationship was ended."""

    family_id: FamilyId
    source_person_id: PersonId
    target_person_id: PersonId
    relationship_type: RelationshipType
    occurred_at: datetime

    def __post_init__(self) -> None:
        _validate_event(
            "FamilyRelationshipEnded",
            self.family_id,
            self.source_person_id,
            self.target_person_id,
            self.relationship_type,
            self.occurred_at,
        )


def _validate_event(
    event_name: str,
    family_id: FamilyId,
    source_person_id: PersonId,
    target_person_id: PersonId,
    relationship_type: RelationshipType,
    occurred_at: datetime,
) -> None:
    if not isinstance(family_id, FamilyId):
        raise TypeError(f"{event_name} family_id must be a FamilyId")
    if not isinstance(source_person_id, PersonId):
        raise TypeError(
            f"{event_name} source_person_id must be a PersonId"
        )
    if not isinstance(target_person_id, PersonId):
        raise TypeError(
            f"{event_name} target_person_id must be a PersonId"
        )
    if not isinstance(relationship_type, RelationshipType):
        raise TypeError(
            f"{event_name} relationship_type must be a RelationshipType"
        )
    if not isinstance(occurred_at, datetime):
        raise TypeError(f"{event_name} occurred_at must be a datetime")
    if occurred_at.tzinfo is None or occurred_at.utcoffset() is None:
        raise ValueError(
            f"{event_name} occurrence time must be timezone-aware"
        )
