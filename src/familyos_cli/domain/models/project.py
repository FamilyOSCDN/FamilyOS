"""Project domain model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Project:
    """Represents a FamilyOS project."""

    name: str