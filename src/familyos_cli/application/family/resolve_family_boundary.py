"""Canonical ResolveFamilyBoundary application query."""

from __future__ import annotations

from familyos_cli.application.ports.family import FamilyRepository
from familyos_cli.domain.family import FamilyId


class ResolveFamilyBoundary:
    """Resolve one existing Family's canonical business-boundary identity."""

    def __init__(self, repository: FamilyRepository) -> None:
        self._repository = repository

    def execute(self, family_id: FamilyId) -> FamilyId | None:
        """Return the FamilyId boundary identity, or absence for an unknown Family."""

        family = self._repository.get(family_id)
        if family is None:
            return None

        return family.family_id
