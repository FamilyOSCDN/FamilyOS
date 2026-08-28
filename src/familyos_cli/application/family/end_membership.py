"""Canonical EndMembership application use case."""

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
    FamilyMembershipEnded,
    Membership,
)
from familyos_cli.domain.person import PersonId


@dataclass(frozen=True, slots=True)
class EndMembershipResult:
    """Successful canonical Membership ending result."""

    membership: Membership
    event: FamilyMembershipEnded


class EndMembership:
    """End one existing non-terminal canonical Membership continuity."""

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
    ) -> EndMembershipResult:
        """Validate, transition, persist, and report canonical ending."""

        if not isinstance(family_id, FamilyId):
            raise TypeError("family_id must be a FamilyId")

        if not isinstance(person_id, PersonId):
            raise TypeError("person_id must be a PersonId")

        membership = self._repository.get(family_id, person_id)
        if membership is None:
            raise MembershipNotFoundError(
                f"Membership '{family_id}:{person_id}' does not exist"
            )

        transitioned = membership.end()
        event = FamilyMembershipEnded(
            family_id=family_id,
            person_id=person_id,
            occurred_at=self._clock(),
        )

        self._repository.save(transitioned)

        return EndMembershipResult(
            membership=transitioned,
            event=event,
        )
