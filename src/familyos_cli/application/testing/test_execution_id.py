"""Opaque identity for one canonical Testing Framework execution."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class TestExecutionId:
    """Stable opaque identifier for one canonical test execution."""

    value: UUID

    @classmethod
    def generate(cls) -> TestExecutionId:
        """Generate a new provider-neutral test execution identity."""

        return cls(uuid4())

    def __str__(self) -> str:
        """Return the canonical UUID string representation."""

        return str(self.value)
