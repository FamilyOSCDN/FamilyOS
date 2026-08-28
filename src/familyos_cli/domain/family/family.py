"""Canonical Family aggregate root."""

from dataclasses import dataclass

from familyos_cli.domain.family.family_id import FamilyId


@dataclass(frozen=True, slots=True)
class Family:
    """Minimal canonical Family aggregate root."""

    family_id: FamilyId

    def __post_init__(self) -> None:
        """Require the canonical Family identity value object."""
        if not isinstance(self.family_id, FamilyId):
            raise TypeError("Family family_id must be a FamilyId")
