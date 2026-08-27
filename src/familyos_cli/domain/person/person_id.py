"""Canonical Person identifier."""

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class PersonId:
    """Opaque UUID-backed canonical identity of one Person."""

    value: UUID

    @classmethod
    def generate(cls) -> "PersonId":
        """Generate a new canonical Person identity using UUID version 4."""
        return cls(uuid4())

    def __str__(self) -> str:
        """Return the canonical UUID textual representation."""
        return str(self.value)
