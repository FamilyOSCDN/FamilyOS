"""In-memory adapter for canonical Relationship temporal persistence."""

from threading import Lock

from familyos_cli.application.ports.family import (
    RelationshipConflictError,
    RelationshipRepository,
    RelationshipTemporalFact,
)
from familyos_cli.domain.family import (
    FamilyId,
    FamilyRelationshipEnded,
    FamilyRelationshipEstablished,
    Relationship,
    RelationshipState,
    RelationshipType,
)
from familyos_cli.domain.person import PersonId

RelationshipKey = tuple[FamilyId, PersonId, PersonId, RelationshipType]


class InMemoryRelationshipRepository(RelationshipRepository):
    """Atomically store Relationship continuity and required temporal facts."""

    def __init__(self) -> None:
        self._relationships: dict[RelationshipKey, Relationship] = {}
        self._temporal_facts: dict[
            RelationshipKey,
            tuple[RelationshipTemporalFact, ...],
        ] = {}
        self._lock = Lock()

    def save(
        self,
        relationship: Relationship,
        temporal_fact: RelationshipTemporalFact,
    ) -> None:
        """Persist one canonical transition and its occurrence fact atomically."""

        key = self._key(relationship)

        with self._lock:
            existing = self._relationships.get(key)
            self._validate_temporal_fact(
                existing=existing,
                candidate=relationship,
                temporal_fact=temporal_fact,
            )

            if existing is None:
                if relationship.state is not RelationshipState.ESTABLISHED:
                    raise RelationshipConflictError(
                        "Initial Relationship persistence requires ESTABLISHED state"
                    )
            elif not self._is_valid_successor(existing, relationship):
                raise RelationshipConflictError(
                    "Relationship persistence must preserve one canonical continuity"
                )

            existing_facts = self._temporal_facts.get(key, ())
            self._relationships[key] = relationship
            self._temporal_facts[key] = (*existing_facts, temporal_fact)

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
    def _validate_temporal_fact(
        *,
        existing: Relationship | None,
        candidate: Relationship,
        temporal_fact: RelationshipTemporalFact,
    ) -> None:
        if (
            temporal_fact.family_id != candidate.family_id
            or temporal_fact.source_person_id != candidate.source_person_id
            or temporal_fact.target_person_id != candidate.target_person_id
            or temporal_fact.relationship_type is not candidate.relationship_type
        ):
            raise RelationshipConflictError(
                "Relationship temporal fact must match canonical Relationship identity"
            )

        if existing is None:
            if not isinstance(temporal_fact, FamilyRelationshipEstablished):
                raise RelationshipConflictError(
                    "Initial Relationship persistence requires establishment temporal fact"
                )
            return

        if not (
            existing.state is RelationshipState.ESTABLISHED
            and candidate.state is RelationshipState.ENDED
            and isinstance(temporal_fact, FamilyRelationshipEnded)
        ):
            raise RelationshipConflictError(
                "Relationship temporal fact must match canonical lifecycle transition"
            )

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
