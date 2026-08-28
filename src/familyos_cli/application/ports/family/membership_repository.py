"""Persistence port for canonical Family Membership."""

from __future__ import annotations

from abc import ABC, abstractmethod

from familyos_cli.domain.family import FamilyId, Membership
from familyos_cli.domain.person import PersonId


class MembershipConflictError(Exception):
    """Raised when persistence would violate canonical Membership continuity."""


class MembershipRepository(ABC):
    """Persist and retrieve canonical Membership continuities."""

    @abstractmethod
    def save(self, membership: Membership) -> None:
        """Persist canonical Membership creation or a valid lifecycle successor."""

        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        family_id: FamilyId,
        person_id: PersonId,
    ) -> Membership | None:
        """Return canonical Membership, including ENDED, or ordinary absence."""

        raise NotImplementedError
