"""Canonical EstablishMembership application use case."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from familyos_cli.application.ports.family import (
    FamilyRepository,
    MembershipConflictError,
    MembershipRepository,
)
from familyos_cli.application.ports.person import PersonRepository
from familyos_cli.domain.family import (
    FamilyId,
    FamilyMembershipCreated,
    Membership,
)
from familyos_cli.domain.person import PersonId


class FamilyNotFoundError(Exception):
    """Raised when Membership establishment references an absent Family."""


class PersonNotFoundError(Exception):
    """Raised when Membership establishment references an absent Person."""


@dataclass(frozen=True, slots=True)
class EstablishMembershipResult:
    """Successful canonical Membership establishment result."""

    membership: Membership
    event: FamilyMembershipCreated


class EstablishMembership:
    """Establish and persist one canonical Membership continuity."""

    def __init__(
        self,
        family_repository: FamilyRepository,
        person_repository: PersonRepository,
        membership_repository: MembershipRepository,
        *,
        clock: Callable[[], datetime],
    ) -> None:
        self._family_repository = family_repository
        self._person_repository = person_repository
        self._membership_repository = membership_repository
        self._clock = clock

    def execute(
        self,
        family_id: FamilyId,
        person_id: PersonId,
    ) -> EstablishMembershipResult:
        """Resolve prerequisites, establish Membership, persist, and report success."""

        if not isinstance(family_id, FamilyId):
            raise TypeError("family_id must be a FamilyId")

        if not isinstance(person_id, PersonId):
            raise TypeError("person_id must be a PersonId")

        if self._family_repository.get(family_id) is None:
            raise FamilyNotFoundError(f"Family '{family_id}' does not exist")

        if self._person_repository.get(person_id) is None:
            raise PersonNotFoundError(f"Person '{person_id}' does not exist")

        if self._membership_repository.get(family_id, person_id) is not None:
            raise MembershipConflictError(
                f"Membership '{family_id}:{person_id}' already exists"
            )

        membership = Membership.establish(family_id, person_id)
        event = FamilyMembershipCreated(
            family_id=family_id,
            person_id=person_id,
            occurred_at=self._clock(),
        )

        self._membership_repository.save(membership, event)

        return EstablishMembershipResult(
            membership=membership,
            event=event,
        )
