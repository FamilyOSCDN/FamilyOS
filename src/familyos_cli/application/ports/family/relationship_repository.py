"""Persistence port for canonical Family Relationships."""

from __future__ import annotations

from abc import ABC, abstractmethod

from familyos_cli.domain.family import FamilyId, Relationship, RelationshipType
from familyos_cli.domain.person import PersonId


class RelationshipConflictError(Exception):
    """Raised when persistence would violate canonical Relationship continuity."""


class RelationshipRepository(ABC):
    """Persist and retrieve canonical normalized Relationship continuities."""

    @abstractmethod
    def save(self, relationship: Relationship) -> None:
        """Persist canonical creation or the valid terminal lifecycle successor."""

        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        family_id: FamilyId,
        source_person_id: PersonId,
        target_person_id: PersonId,
        relationship_type: RelationshipType,
    ) -> Relationship | None:
        """Return canonical Relationship, including ENDED, or ordinary absence."""

        raise NotImplementedError
