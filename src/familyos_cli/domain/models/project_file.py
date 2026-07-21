"""Project file model."""

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ProjectFile:
    """Represent a file to generate."""

    path: str
    template: str