"""Canonical Family Relationship entity and normalization rules."""

from __future__ import annotations

from dataclasses import dataclass, replace

from familyos_cli.domain.family.family_id import FamilyId
from familyos_cli.domain.family.relationship_state import RelationshipState
from familyos_cli.domain.family.relationship_type import RelationshipType
from familyos_cli.domain.person import PersonId


class InvalidRelationshipTransitionError(Exception):
    """Raised when a Relationship lifecycle transition is not canonical."""


@dataclass(frozen=True, slots=True)
class Relationship:
    """One canonical Family Relationship continuity."""

    family_id: FamilyId
    source_person_id: PersonId
    target_person_id: PersonId
    relationship_type: RelationshipType
    state: RelationshipState

    def __post_init__(self) -> None:
        if not isinstance(self.family_id, FamilyId):
            raise TypeError("Relationship family_id must be a FamilyId")
        if not isinstance(self.source_person_id, PersonId):
            raise TypeError(
                "Relationship source_person_id must be a PersonId"
            )
        if not isinstance(self.target_person_id, PersonId):
            raise TypeError(
                "Relationship target_person_id must be a PersonId"
            )
        if not isinstance(self.relationship_type, RelationshipType):
            raise TypeError(
                "Relationship relationship_type must be a RelationshipType"
            )
        if not isinstance(self.state, RelationshipState):
            raise TypeError(
                "Relationship state must be a RelationshipState"
            )
        if self.source_person_id == self.target_person_id:
            raise ValueError(
                "Relationship source and target Persons must be distinct"
            )
        if self.relationship_type is RelationshipType.CHILD_OF:
            raise ValueError(
                "Relationship canonical state must not store CHILD_OF"
            )
        if self.relationship_type in {
            RelationshipType.SPOUSE_OF,
            RelationshipType.SIBLING_OF,
        } and not self._is_canonical_symmetric_order(
            self.source_person_id,
            self.target_person_id,
        ):
            raise ValueError(
                "Symmetric Relationship endpoints must use canonical UUID order"
            )

    @classmethod
    def establish(
        cls,
        family_id: FamilyId,
        source_person_id: PersonId,
        target_person_id: PersonId,
        relationship_type: RelationshipType,
    ) -> Relationship:
        """Establish one normalized canonical Relationship continuity."""

        cls._validate_inputs(
            family_id,
            source_person_id,
            target_person_id,
            relationship_type,
        )

        (
            canonical_source,
            canonical_target,
            canonical_type,
        ) = cls.normalize_identity(
            source_person_id,
            target_person_id,
            relationship_type,
        )

        return cls(
            family_id=family_id,
            source_person_id=canonical_source,
            target_person_id=canonical_target,
            relationship_type=canonical_type,
            state=RelationshipState.ESTABLISHED,
        )

    @staticmethod
    def normalize_identity(
        source_person_id: PersonId,
        target_person_id: PersonId,
        relationship_type: RelationshipType,
    ) -> tuple[PersonId, PersonId, RelationshipType]:
        """Normalize inverse and symmetric views to canonical identity."""

        if not isinstance(source_person_id, PersonId):
            raise TypeError("source_person_id must be a PersonId")
        if not isinstance(target_person_id, PersonId):
            raise TypeError("target_person_id must be a PersonId")
        if not isinstance(relationship_type, RelationshipType):
            raise TypeError("relationship_type must be a RelationshipType")
        if source_person_id == target_person_id:
            raise ValueError(
                "Relationship source and target Persons must be distinct"
            )

        if relationship_type is RelationshipType.CHILD_OF:
            return (
                target_person_id,
                source_person_id,
                RelationshipType.PARENT_OF,
            )

        if relationship_type in {
            RelationshipType.SPOUSE_OF,
            RelationshipType.SIBLING_OF,
        }:
            if Relationship._is_canonical_symmetric_order(
                source_person_id,
                target_person_id,
            ):
                return (
                    source_person_id,
                    target_person_id,
                    relationship_type,
                )
            return (
                target_person_id,
                source_person_id,
                relationship_type,
            )

        return source_person_id, target_person_id, relationship_type

    def end(self) -> Relationship:
        """Apply the only canonical terminal Relationship transition."""

        if self.state is not RelationshipState.ESTABLISHED:
            raise InvalidRelationshipTransitionError(
                f"Relationship transition from {self.state.value} "
                "to ended is not allowed"
            )

        return replace(self, state=RelationshipState.ENDED)

    @staticmethod
    def _is_canonical_symmetric_order(
        source_person_id: PersonId,
        target_person_id: PersonId,
    ) -> bool:
        return source_person_id.value.int < target_person_id.value.int

    @staticmethod
    def _validate_inputs(
        family_id: FamilyId,
        source_person_id: PersonId,
        target_person_id: PersonId,
        relationship_type: RelationshipType,
    ) -> None:
        if not isinstance(family_id, FamilyId):
            raise TypeError("family_id must be a FamilyId")
        if not isinstance(source_person_id, PersonId):
            raise TypeError("source_person_id must be a PersonId")
        if not isinstance(target_person_id, PersonId):
            raise TypeError("target_person_id must be a PersonId")
        if not isinstance(relationship_type, RelationshipType):
            raise TypeError("relationship_type must be a RelationshipType")
        if source_person_id == target_person_id:
            raise ValueError(
                "Relationship source and target Persons must be distinct"
            )
