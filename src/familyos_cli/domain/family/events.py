"""Canonical Family domain events."""

from dataclasses import dataclass
from datetime import datetime

from familyos_cli.domain.family.family_id import FamilyId


@dataclass(frozen=True, slots=True)
class FamilyCreated:
    """Immutable business fact that one canonical Family was created."""

    family_id: FamilyId
    occurred_at: datetime

    def __post_init__(self) -> None:
        """Validate the canonical event payload."""
        if not isinstance(self.family_id, FamilyId):
            raise TypeError("FamilyCreated family_id must be a FamilyId")

        if not isinstance(self.occurred_at, datetime):
            raise TypeError("FamilyCreated occurred_at must be a datetime")

        if self.occurred_at.tzinfo is None or self.occurred_at.utcoffset() is None:
            raise ValueError(
                "FamilyCreated occurrence time must be timezone-aware"
            )
