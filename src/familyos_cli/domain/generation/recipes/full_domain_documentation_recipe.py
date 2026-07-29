"""Full domain documentation generation recipe."""

from __future__ import annotations

from familyos_cli.domain.generation.artifact_definition import (
    ArtifactDefinition,
)
from familyos_cli.domain.generation.recipes.aggregate_documentation_recipe import (
    AggregateDocumentationRecipe,
)
from familyos_cli.domain.generation.recipes.domain_context_documentation_recipe import (
    DomainContextDocumentationRecipe,
)
from familyos_cli.domain.generation.recipes.domain_documentation_recipe import (
    DomainDocumentationRecipe,
)
from familyos_cli.domain.generation.recipes.entity_documentation_recipe import (
    EntityDocumentationRecipe,
)
from familyos_cli.domain.generation.recipes.repository_documentation_recipe import (
    RepositoryDocumentationRecipe,
)
from familyos_cli.domain.generation.recipes.service_documentation_recipe import (
    ServiceDocumentationRecipe,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class FullDomainDocumentationRecipe:
    """Compose all domain documentation recipes."""

    @property
    def name(
        self,
    ) -> str:
        """Return recipe name."""

        return "full_domain_documentation"

    def build_artifacts(
        self,
        specification: DomainSpecification,
    ) -> list[ArtifactDefinition]:
        """Build complete domain documentation artifacts."""

        recipes = (
            DomainDocumentationRecipe(),
            EntityDocumentationRecipe(),
            AggregateDocumentationRecipe(),
            DomainContextDocumentationRecipe(),
            RepositoryDocumentationRecipe(),
            ServiceDocumentationRecipe(),
        )

        artifacts: list[ArtifactDefinition] = []

        for recipe in recipes:
            artifacts.extend(
                recipe.build_artifacts(
                    specification,
                ),
            )

        return artifacts
