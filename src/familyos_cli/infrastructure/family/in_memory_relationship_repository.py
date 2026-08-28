"""In-memory adapter for the canonical Relationship repository port."""

from threading import Lock

from familyos_cli.application.ports.family import (
    RelationshipConflictError,
    RelationshipRepository,
)
from familyos_cli.domain.family import (
    FamilyId,
    Relationship,
    RelationshipState,
    RelationshipType,
)
from familyos_cli.domain.person import PersonId

RelationshipKey = tuple[FamilyId, PersonId, PersonId, RelationshipType]


class InMemoryRelationshipRepository(RelationshipRepository):
    """Store canonical Relationship continuities by normalized business key."""

    def __init__(self) -> None:
        self._relationships: dict[RelationshipKey, Relationship] = {}
        self._lock = Lock()

    def save(self, relationship: Relationship) -> None:
        """Persist ESTABLISHED creation or its canonical ENDED successor."""

        key = self._key(relationship)

        with self._lock:
            existing = self._relationships.get(key)

            if existing is None:
                if relationship.state is not RelationshipState.ESTABLISHED:
                    raise RelationshipConflictError(
                        "Initial Relationship persistence requires ESTABLISHED state"
                    )

                self._relationships[key] = relationship
                return

            if not self._is_valid_successor(existing, relationship):
                raise RelationshipConflictError(
                    "Relationship persistence must preserve one canonical continuity"
                )

            self._relationships[key] = relationship

    def get(
        self,
        family_id: FamilyId,
        source_person_id: PersonId,
        target_person_id: PersonId,
        relationship_type: RelationshipType,
    ) -> Relationship | None:
        """Return Relationship for an already canonical normalized business key."""

        key = (
            family_id,
            source_person_id,
            target_person_id,
            relationship_type,
        )

        with self._lock:
            return self._relationships.get(key)

    @staticmethod
    def _key(relationship: Relationship) -> RelationshipKey:
        return (
            relationship.family_id,
            relationship.source_person_id,
            relationship.target_person_id,
            relationship.relationship_type,
        )

    @staticmethod
    def _is_valid_successor(
        existing: Relationship,
        candidate: Relationship,
    ) -> bool:
        return (
            existing.state is RelationshipState.ESTABLISHED
            and candidate.state is RelationshipState.ENDED
        )
