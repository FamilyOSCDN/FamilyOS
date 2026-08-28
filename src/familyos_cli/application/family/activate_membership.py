"""Canonical ActivateMembership application use case."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from familyos_cli.application.ports.family import MembershipRepository
from familyos_cli.domain.family import (
    FamilyId,
    FamilyMembershipActivated,
    FamilyMembershipReactivated,
    Membership,
    MembershipState,
)
from familyos_cli.domain.person import PersonId

ActivationEvent = FamilyMembershipActivated | FamilyMembershipReactivated


class MembershipNotFoundError(Exception):
    """Raised when a Membership lifecycle command targets ordinary absence."""


@dataclass(frozen=True, slots=True)
class ActivateMembershipResult:
    """Successful canonical Membership activation result."""

    membership: Membership
    event: ActivationEvent


class ActivateMembership:
    """Activate or reactivate one existing canonical Membership continuity."""

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
    ) -> ActivateMembershipResult:
        """Validate, transition, persist, and report canonical activation."""

        if not isinstance(family_id, FamilyId):
            raise TypeError("family_id must be a FamilyId")

        if not isinstance(person_id, PersonId):
            raise TypeError("person_id must be a PersonId")

        membership = self._repository.get(family_id, person_id)
        if membership is None:
            raise MembershipNotFoundError(
                f"Membership '{family_id}:{person_id}' does not exist"
            )

        source_state = membership.state

        # Validate the transition before consulting the clock. The immutable
        # transitioned value is not observable until repository.save succeeds.
        transitioned = membership.activate()

        occurred_at = self._clock()
        if source_state is MembershipState.PENDING:
            event: ActivationEvent = FamilyMembershipActivated(
                family_id=family_id,
                person_id=person_id,
                occurred_at=occurred_at,
            )
        else:
            event = FamilyMembershipReactivated(
                family_id=family_id,
                person_id=person_id,
                occurred_at=occurred_at,
            )

        self._repository.save(transitioned, event)

        return ActivateMembershipResult(
            membership=transitioned,
            event=event,
        )
