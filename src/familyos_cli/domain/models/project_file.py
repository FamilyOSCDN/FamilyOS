"""Project file model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectFile:
    """Describe a generated project file."""

    destination: str
    template: str