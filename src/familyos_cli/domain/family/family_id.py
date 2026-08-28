"""Canonical Family identifier."""

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class FamilyId:
    """Opaque UUID-v4-backed canonical identity of one Family."""

    value: UUID

    def __post_init__(self) -> None:
        """Reject non-canonical or non-UUID-v4 backing values without coercion."""
        if not isinstance(self.value, UUID):
            raise TypeError("FamilyId value must be a UUID")

        if self.value.version != 4:
            raise ValueError("FamilyId value must be a UUID version 4")

    @classmethod
    def generate(cls) -> "FamilyId":
        """Generate a new canonical Family identity using UUID version 4."""
        return cls(uuid4())

    def __str__(self) -> str:
        """Return the canonical UUID textual representation."""
        return str(self.value)
