"""Tests for the canonical RelationshipRepository port."""

from __future__ import annotations

import inspect
from uuid import UUID

import pytest

from familyos_cli.application.ports.family import RelationshipRepository
from familyos_cli.domain.family import FamilyId, Relationship, RelationshipType
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


def test_concrete_repository_can_implement_canonical_contract() -> None:
    class Repository(RelationshipRepository):
        def __init__(self) -> None:
            self._relationships: dict[
                tuple[FamilyId, PersonId, PersonId, RelationshipType],
                Relationship,
            ] = {}

        def save(self, relationship: Relationship) -> None:
            key = (
                relationship.family_id,
                relationship.source_person_id,
                relationship.target_person_id,
                relationship.relationship_type,
            )
            self._relationships[key] = relationship

        def get(
            self,
            family_id: FamilyId,
            source_person_id: PersonId,
            target_person_id: PersonId,
            relationship_type: RelationshipType,
        ) -> Relationship | None:
            return self._relationships.get(
                (
                    family_id,
                    source_person_id,
                    target_person_id,
                    relationship_type,
                )
            )

    repository = Repository()
    relationship = Relationship.establish(
        _family_id(),
        _source_person_id(),
        _target_person_id(),
        RelationshipType.PARENT_OF,
    )

    assert repository.get(
        relationship.family_id,
        relationship.source_person_id,
        relationship.target_person_id,
        relationship.relationship_type,
    ) is None

    repository.save(relationship)

    assert repository.get(
        relationship.family_id,
        relationship.source_person_id,
        relationship.target_person_id,
        relationship.relationship_type,
    ) == relationship


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
