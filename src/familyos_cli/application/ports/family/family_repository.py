"""Persistence port for the canonical Family domain."""

from __future__ import annotations

from abc import ABC, abstractmethod

from familyos_cli.domain.family import Family, FamilyId


class FamilyConflictError(Exception):
    """Raised when persistence would replace an established Family identity."""


class FamilyRepository(ABC):
    """Persist and retrieve canonical Family aggregates."""

    @abstractmethod
    def save(self, family: Family) -> None:
        """Atomically persist a new Family, rejecting an established identity."""

        raise NotImplementedError

    @abstractmethod
    def get(self, family_id: FamilyId) -> Family | None:
        """Return one Family, or absence when no Family exists for the identifier."""

        raise NotImplementedError
