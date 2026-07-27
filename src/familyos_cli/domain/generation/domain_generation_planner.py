from __future__ import annotations

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class DomainGenerationPlanner:
    """Creates generation plans from domain specifications."""

    def create_plan(
        self,
        specification: DomainSpecification,
    ) -> DomainGenerationPlan:
        """Build a generation plan for a domain."""

        artifacts: list[ArtifactDefinition] = []

        # Entities
        for entity in specification.entities:
            artifacts.append(
                ArtifactDefinition(
                    artifact_type="entity",
                    name=entity.name,
                    target_path=f"models/{entity.name.lower()}.py",
                )
            )

        # Aggregates
        for aggregate in specification.aggregates:
            artifacts.append(
                ArtifactDefinition(
                    artifact_type="aggregate",
                    name=aggregate.name,
                    target_path=f"aggregates/{aggregate.name.lower()}.py",
                )
            )

        # Repositories
        for repository in specification.repositories:
            artifacts.append(
                ArtifactDefinition(
                    artifact_type="repository",
                    name=repository.name,
                    target_path=(
                        "repositories/"
                        f"{repository.name.lower()}.py"
                    ),
                )
            )

        # Services
        for service in specification.services:
            artifacts.append(
                ArtifactDefinition(
                    artifact_type="service",
                    name=service.name,
                    target_path=(
                        "services/"
                        f"{service.name.lower()}.py"
                    ),
                )
            )

        return DomainGenerationPlan(
            domain_name=specification.name,
            artifacts=artifacts,
        )