"""Canonical GetMembership application query."""

from __future__ import annotations

from familyos_cli.application.ports.family import MembershipRepository
from familyos_cli.domain.family import FamilyId, Membership
from familyos_cli.domain.person import PersonId


class GetMembership:
    """Retrieve one canonical Membership through the repository boundary."""

    def __init__(self, repository: MembershipRepository) -> None:
        self._repository = repository

    def execute(
        self,
        family_id: FamilyId,
        person_id: PersonId,
    ) -> Membership | None:
        """Return canonical Membership, including ENDED, or ordinary absence."""

        return self._repository.get(family_id, person_id)
