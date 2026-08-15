"""Opaque identity for one canonical build execution."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class BuildId:
    """Stable opaque identifier for one canonical build execution."""

    value: UUID

    @classmethod
    def generate(cls) -> BuildId:
        """Generate a new provider-neutral build identity."""

        return cls(uuid4())

    def __str__(self) -> str:
        """Return the canonical UUID string representation."""

        return str(self.value)
