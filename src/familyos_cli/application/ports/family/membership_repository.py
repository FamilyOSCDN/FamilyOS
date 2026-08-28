"""Persistence port for canonical Family Membership."""

from __future__ import annotations

from abc import ABC, abstractmethod

from familyos_cli.domain.family import (
    FamilyId,
    FamilyMembershipActivated,
    FamilyMembershipCreated,
    FamilyMembershipEnded,
    FamilyMembershipReactivated,
    FamilyMembershipSuspended,
    Membership,
)
from familyos_cli.domain.person import PersonId

MembershipTemporalFact = (
    FamilyMembershipCreated
    | FamilyMembershipActivated
    | FamilyMembershipSuspended
    | FamilyMembershipReactivated
    | FamilyMembershipEnded
)


class MembershipConflictError(Exception):
    """Raised when persistence would violate canonical Membership continuity."""


class MembershipRepository(ABC):
    """Persist and retrieve canonical Membership continuities."""

    @abstractmethod
    def save(
        self,
        membership: Membership,
        temporal_fact: MembershipTemporalFact,
    ) -> None:
        """Atomically persist Membership continuity and its temporal fact."""

        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        family_id: FamilyId,
        person_id: PersonId,
    ) -> Membership | None:
        """Return canonical Membership, including ENDED, or ordinary absence."""

        raise NotImplementedError
