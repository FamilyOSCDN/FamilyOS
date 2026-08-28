"""Canonical GetRelationship application query."""

from __future__ import annotations

from familyos_cli.application.ports.family import RelationshipRepository
from familyos_cli.domain.family import FamilyId, Relationship, RelationshipType
from familyos_cli.domain.person import PersonId


class GetRelationship:
    def __init__(self, repository: RelationshipRepository) -> None:
        self._repository = repository

    def execute(
        self,
        family_id: FamilyId,
        source_person_id: PersonId,
        target_person_id: PersonId,
        relationship_type: RelationshipType,
    ) -> Relationship | None:
        if not isinstance(family_id, FamilyId):
            raise TypeError("family_id must be a FamilyId")

        canonical_source, canonical_target, canonical_type = (
            Relationship.normalize_identity(
                source_person_id,
                target_person_id,
                relationship_type,
            )
        )
        return self._repository.get(
            family_id,
            canonical_source,
            canonical_target,
            canonical_type,
        )
