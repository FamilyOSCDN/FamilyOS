"""Registry domain models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ArtifactDefinition:
    """Describe an artifact registered in the framework."""

    id: str
    specification: str


@dataclass(frozen=True)
class Registry:
    """Represent the FamilyOS artifact registry."""

    version: str
    artifacts: list[ArtifactDefinition]