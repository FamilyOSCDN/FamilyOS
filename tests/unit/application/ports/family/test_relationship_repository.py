"""Tests for the canonical RelationshipRepository temporal persistence port."""

from __future__ import annotations

import inspect
from datetime import UTC, datetime
from uuid import UUID

import pytest

from familyos_cli.application.ports.family import (
    RelationshipRepository,
    RelationshipTemporalFact,
)
from familyos_cli.domain.family import (
    FamilyId,
    FamilyRelationshipEstablished,
    Relationship,
    RelationshipType,
)
from familyos_cli.domain.person import PersonId


def _family_id() -> FamilyId:
    return FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))


def _source_person_id() -> PersonId:
    return PersonId(UUID("00000000-0000-4000-8000-000000000001"))


def _target_person_id() -> PersonId:
    return PersonId(UUID("ffffffff-ffff-4fff-8fff-ffffffffffff"))


def test_relationship_repository_is_abstract() -> None:
    assert inspect.isabstract(RelationshipRepository)


def test_relationship_repository_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        RelationshipRepository()  # type: ignore[abstract]


def test_concrete_repository_accepts_entity_and_temporal_fact_atomically() -> None:
    class Repository(RelationshipRepository):
        def __init__(self) -> None:
            self.relationship: Relationship | None = None
            self.fact: RelationshipTemporalFact | None = None

        def save(
            self,
            relationship: Relationship,
            temporal_fact: RelationshipTemporalFact,
        ) -> None:
            self.relationship = relationship
            self.fact = temporal_fact

        def get(
            self,
            family_id: FamilyId,
            source_person_id: PersonId,
            target_person_id: PersonId,
            relationship_type: RelationshipType,
        ) -> Relationship | None:
            if self.relationship is None:
                return None
            key = (
                family_id,
                source_person_id,
                target_person_id,
                relationship_type,
            )
            stored_key = (
                self.relationship.family_id,
                self.relationship.source_person_id,
                self.relationship.target_person_id,
                self.relationship.relationship_type,
            )
            return self.relationship if key == stored_key else None

    repository = Repository()
    relationship = Relationship.establish(
        _family_id(),
        _source_person_id(),
        _target_person_id(),
        RelationshipType.PARENT_OF,
    )
    event = FamilyRelationshipEstablished(
        family_id=relationship.family_id,
        source_person_id=relationship.source_person_id,
        target_person_id=relationship.target_person_id,
        relationship_type=relationship.relationship_type,
        occurred_at=datetime(2026, 8, 28, 10, 0, tzinfo=UTC),
    )

    repository.save(relationship, event)

    assert repository.get(
        relationship.family_id,
        relationship.source_person_id,
        relationship.target_person_id,
        relationship.relationship_type,
    ) == relationship
    assert repository.fact == event


def test_relationship_repository_exposes_only_canonical_operations() -> None:
    public_operations = {
        name
        for name, member in inspect.getmembers(
            RelationshipRepository,
            inspect.isfunction,
        )
        if not name.startswith("_")
    }

    assert public_operations == {"get", "save"}
