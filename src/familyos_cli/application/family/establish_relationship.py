"""Canonical EstablishRelationship application use case."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from familyos_cli.application.family.establish_membership import (
    FamilyNotFoundError,
    PersonNotFoundError,
)
from familyos_cli.application.ports.family import (
    FamilyRepository,
    RelationshipConflictError,
    RelationshipRepository,
)
from familyos_cli.application.ports.person import PersonRepository
from familyos_cli.domain.family import (
    FamilyId,
    FamilyRelationshipEstablished,
    Relationship,
    RelationshipType,
)
from familyos_cli.domain.person import PersonId


@dataclass(frozen=True, slots=True)
class EstablishRelationshipResult:
    relationship: Relationship
    event: FamilyRelationshipEstablished


class EstablishRelationship:
    def __init__(
        self,
        family_repository: FamilyRepository,
        person_repository: PersonRepository,
        relationship_repository: RelationshipRepository,
        *,
        clock: Callable[[], datetime],
    ) -> None:
        self._family_repository = family_repository
        self._person_repository = person_repository
        self._relationship_repository = relationship_repository
        self._clock = clock

    def execute(
        self,
        family_id: FamilyId,
        source_person_id: PersonId,
        target_person_id: PersonId,
        relationship_type: RelationshipType,
    ) -> EstablishRelationshipResult:
        if not isinstance(family_id, FamilyId):
            raise TypeError("family_id must be a FamilyId")
        if not isinstance(source_person_id, PersonId):
            raise TypeError("source_person_id must be a PersonId")
        if not isinstance(target_person_id, PersonId):
            raise TypeError("target_person_id must be a PersonId")
        if not isinstance(relationship_type, RelationshipType):
            raise TypeError("relationship_type must be a RelationshipType")
        if source_person_id == target_person_id:
            raise ValueError("Relationship source and target Persons must be distinct")

        if self._family_repository.get(family_id) is None:
            raise FamilyNotFoundError(f"Family '{family_id}' does not exist")
        if self._person_repository.get(source_person_id) is None:
            raise PersonNotFoundError(f"Person '{source_person_id}' does not exist")
        if self._person_repository.get(target_person_id) is None:
            raise PersonNotFoundError(f"Person '{target_person_id}' does not exist")

        canonical_source, canonical_target, canonical_type = (
            Relationship.normalize_identity(
                source_person_id,
                target_person_id,
                relationship_type,
            )
        )

        if self._relationship_repository.get(
            family_id,
            canonical_source,
            canonical_target,
            canonical_type,
        ) is not None:
            raise RelationshipConflictError(
                "Canonical Relationship continuity already exists"
            )

        relationship = Relationship.establish(
            family_id,
            source_person_id,
            target_person_id,
            relationship_type,
        )
        event = FamilyRelationshipEstablished(
            family_id=relationship.family_id,
            source_person_id=relationship.source_person_id,
            target_person_id=relationship.target_person_id,
            relationship_type=relationship.relationship_type,
            occurred_at=self._clock(),
        )

        self._relationship_repository.save(relationship, event)
        return EstablishRelationshipResult(relationship=relationship, event=event)
