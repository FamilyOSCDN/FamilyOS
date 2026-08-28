"""Canonical EndRelationship application use case."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from familyos_cli.application.ports.family import RelationshipRepository
from familyos_cli.domain.family import (
    FamilyId,
    FamilyRelationshipEnded,
    Relationship,
    RelationshipType,
)
from familyos_cli.domain.person import PersonId


class RelationshipNotFoundError(Exception):
    """Raised when a canonical Relationship continuity does not exist."""


@dataclass(frozen=True, slots=True)
class EndRelationshipResult:
    relationship: Relationship
    event: FamilyRelationshipEnded


class EndRelationship:
    def __init__(
        self,
        repository: RelationshipRepository,
        *,
        clock: Callable[[], datetime],
    ) -> None:
        self._repository = repository
        self._clock = clock

    def execute(
        self,
        family_id: FamilyId,
        source_person_id: PersonId,
        target_person_id: PersonId,
        relationship_type: RelationshipType,
    ) -> EndRelationshipResult:
        if not isinstance(family_id, FamilyId):
            raise TypeError("family_id must be a FamilyId")

        canonical_source, canonical_target, canonical_type = (
            Relationship.normalize_identity(
                source_person_id,
                target_person_id,
                relationship_type,
            )
        )

        relationship = self._repository.get(
            family_id,
            canonical_source,
            canonical_target,
            canonical_type,
        )
        if relationship is None:
            raise RelationshipNotFoundError(
                "Canonical Relationship continuity does not exist"
            )

        transitioned = relationship.end()
        event = FamilyRelationshipEnded(
            family_id=transitioned.family_id,
            source_person_id=transitioned.source_person_id,
            target_person_id=transitioned.target_person_id,
            relationship_type=transitioned.relationship_type,
            occurred_at=self._clock(),
        )

        self._repository.save(transitioned)
        return EndRelationshipResult(relationship=transitioned, event=event)
