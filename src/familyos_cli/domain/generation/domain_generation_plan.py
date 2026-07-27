from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)


@dataclass(frozen=True, slots=True)
class DomainGenerationPlan:
    """Describes the generation plan for a domain."""

    domain_name: str

    artifacts: list[ArtifactDefinition] = field(default_factory=list)

    metadata: dict[str, str] = field(default_factory=dict)