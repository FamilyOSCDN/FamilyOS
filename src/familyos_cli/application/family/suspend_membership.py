"""Canonical SuspendMembership application use case."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from familyos_cli.application.family.activate_membership import (
    MembershipNotFoundError,
)
from familyos_cli.application.ports.family import MembershipRepository
from familyos_cli.domain.family import (
    FamilyId,
    FamilyMembershipSuspended,
    Membership,
)
from familyos_cli.domain.person import PersonId


@dataclass(frozen=True, slots=True)
class SuspendMembershipResult:
    """Successful canonical Membership suspension result."""

    membership: Membership
    event: FamilyMembershipSuspended


class SuspendMembership:
    """Suspend one existing ACTIVE canonical Membership continuity."""

    def __init__(
        self,
        repository: MembershipRepository,
        *,
        clock: Callable[[], datetime],
    ) -> None:
        self._repository = repository
        self._clock = clock

    def execute(
        self,
        family_id: FamilyId,
        person_id: PersonId,
    ) -> SuspendMembershipResult:
        """Validate, transition, persist, and report canonical suspension."""

        if not isinstance(family_id, FamilyId):
            raise TypeError("family_id must be a FamilyId")

        if not isinstance(person_id, PersonId):
            raise TypeError("person_id must be a PersonId")

        membership = self._repository.get(family_id, person_id)
        if membership is None:
            raise MembershipNotFoundError(
                f"Membership '{family_id}:{person_id}' does not exist"
            )

        transitioned = membership.suspend()
        event = FamilyMembershipSuspended(
            family_id=family_id,
            person_id=person_id,
            occurred_at=self._clock(),
        )

        self._repository.save(transitioned)

        return SuspendMembershipResult(
            membership=transitioned,
            event=event,
        )
