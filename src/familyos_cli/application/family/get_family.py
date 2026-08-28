"""Canonical GetFamily application query."""

from __future__ import annotations

from familyos_cli.application.ports.family import FamilyRepository
from familyos_cli.domain.family import Family, FamilyId


class GetFamily:
    """Retrieve one canonical Family through the repository boundary."""

    def __init__(self, repository: FamilyRepository) -> None:
        self._repository = repository

    def execute(self, family_id: FamilyId) -> Family | None:
        """Return the canonical Family, or absence when no Family exists."""

        return self._repository.get(family_id)
