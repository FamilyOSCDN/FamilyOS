"""Domain generation planner."""

from __future__ import annotations

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.artifact_path_policy import (
    ArtifactPathPolicy,
    DefaultArtifactPathPolicy,
)
from familyos_cli.domain.generation.artifact_template_policy import (
    ArtifactTemplatePolicy,
    DefaultArtifactTemplatePolicy,
)
from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)
from familyos_cli.domain.generation.recipe_executor import (
    RecipeExecutor,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class DomainGenerationPlanner:
    """Create generation plans from domain specifications."""

    def __init__(
        self,
        path_policy: ArtifactPathPolicy | None = None,
        template_policy: ArtifactTemplatePolicy | None = None,
        recipe_executor: RecipeExecutor | None = None,
    ) -> None:
        """Initialize the planner."""

        self._path_policy = (
            path_policy
            if path_policy is not None
            else DefaultArtifactPathPolicy()
        )

        self._template_policy = (
            template_policy
            if template_policy is not None
            else DefaultArtifactTemplatePolicy()
        )

        self._recipe_executor = recipe_executor

    def create_plan_from_request(
        self,
        request: GenerationRequest,
    ) -> DomainGenerationPlan:
        """Create a generation plan from a recipe request."""

        if self._recipe_executor is None:
            raise ValueError(
                "Recipe executor is required.",
            )

        return DomainGenerationPlan(
            domain_name=request.domain_name,
            artifacts=self._recipe_executor.execute(
                request,
            ),
        )

    def create_plan(
        self,
        specification: DomainSpecification,
    ) -> DomainGenerationPlan:
        """Build a generation plan for a domain."""

        artifacts: list[ArtifactDefinition] = []

        for entity in specification.entities:
            artifacts.append(
                self._create_artifact(
                    kind=ArtifactKind.ENTITY,
                    name=entity.name,
                )
            )

        for aggregate in specification.aggregates:
            artifacts.append(
                self._create_artifact(
                    kind=ArtifactKind.AGGREGATE,
                    name=aggregate.name,
                )
            )

        for repository in specification.repositories:
            artifacts.append(
                self._create_artifact(
                    kind=ArtifactKind.REPOSITORY,
                    name=repository.name,
                )
            )

        for service in specification.services:
            artifacts.append(
                self._create_artifact(
                    kind=ArtifactKind.SERVICE,
                    name=service.name,
                )
            )

        return DomainGenerationPlan(
            domain_name=specification.name,
            artifacts=artifacts,
        )

    def _create_artifact(
        self,
        *,
        kind: ArtifactKind,
        name: str,
    ) -> ArtifactDefinition:
        """Create an artifact definition."""

        return ArtifactDefinition(
            kind=kind,
            name=name,
            target_path=self._path_policy.path_for(
                kind=kind,
                name=name,
            ),
            template=self._template_policy.template_for(
                kind=kind,
            ),
        )
