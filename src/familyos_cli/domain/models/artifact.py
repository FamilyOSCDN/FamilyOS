"""Artifact domain model."""

from dataclasses import dataclass


@dataclass(slots=True)
class Artifact:
    """Represent an artifact to generate."""

    type: str
    name: str