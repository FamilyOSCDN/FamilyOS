"""Canonical Family domain model."""

from familyos_cli.domain.family.events import FamilyCreated
from familyos_cli.domain.family.family import Family
from familyos_cli.domain.family.family_id import FamilyId

__all__ = [
    "Family",
    "FamilyCreated",
    "FamilyId",
]
