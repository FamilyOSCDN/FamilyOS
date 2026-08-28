"""Canonical CreateFamily application use case."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from familyos_cli.application.ports.family import FamilyRepository
from familyos_cli.domain.family import Family, FamilyCreated, FamilyId


@dataclass(frozen=True, slots=True)
class CreateFamilyResult:
    """Successful canonical Family creation result."""

    family: Family
    event: FamilyCreated


class CreateFamily:
    """Create and persist exactly one canonical Family."""

    def __init__(
        self,
        repository: FamilyRepository,
        *,
        family_id_factory: Callable[[], FamilyId] = FamilyId.generate,
        clock: Callable[[], datetime],
    ) -> None:
        self._repository = repository
        self._family_id_factory = family_id_factory
        self._clock = clock

    def execute(self) -> CreateFamilyResult:
        """Create, persist, and report one canonical Family."""

        family = Family(family_id=self._family_id_factory())
        event = FamilyCreated(
            family_id=family.family_id,
            occurred_at=self._clock(),
        )

        self._repository.save(family)

        return CreateFamilyResult(family=family, event=event)
