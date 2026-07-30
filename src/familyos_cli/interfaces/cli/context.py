"""CLI command context."""

from __future__ import annotations

from functools import cached_property

from familyos_cli.application.generation.domain_generation_catalog_service import (
    DomainGenerationCatalogService,
)
from familyos_cli.application.generation.generation_catalog_service import (
    GenerationCatalogService,
)
from familyos_cli.application.generation.recipe_catalog_service import (
    RecipeCatalogService,
)
from familyos_cli.application.specifications.domain_specification_loader_service import (
    DomainSpecificationLoaderService,
)
from familyos_cli.application.use_cases.create_artifact import (
    CreateArtifactUseCase,
)
from familyos_cli.application.use_cases.create_domain import (
    CreateDomainUseCase,
)
from familyos_cli.application.use_cases.create_project import (
    CreateProjectUseCase,
)
from familyos_cli.bootstrap import (
    ApplicationContainer,
    ApplicationFactory,
)


class CommandContext:
    """Shared context for CLI commands."""

    def __init__(
        self,
        container: ApplicationContainer | None = None,
    ) -> None:
        """Initialize CLI context."""

        self._container = (
            container
            if container is not None
            else ApplicationFactory.create()
        )

    @cached_property
    def create_project(
        self,
    ) -> CreateProjectUseCase:
        """Provide project creation use case."""

        return self._container.create_project_use_case()

    @cached_property
    def create_artifact(
        self,
    ) -> CreateArtifactUseCase:
        """Provide artifact creation use case."""

        return self._container.create_artifact_use_case()

    @cached_property
    def domain_specification_loader(
        self,
    ) -> DomainSpecificationLoaderService:
        """Provide domain specification loader service."""

        return self._container.domain_specification_loader_service()

    @cached_property
    def create_domain(
        self,
    ) -> CreateDomainUseCase:
        """Provide domain creation use case."""

        return self._container.create_domain_use_case()

    @cached_property
    def generation_catalog(
        self,
    ) -> GenerationCatalogService:
        """Provide generation catalog service."""

        return self._container.generation_catalog_service()

    @cached_property
    def domain_generation_catalog(
        self,
    ) -> DomainGenerationCatalogService:
        """Provide domain generation catalog service."""

        return self._container.domain_generation_catalog_service()

    @cached_property
    def recipe_catalog(
        self,
    ) -> RecipeCatalogService:
        """Provide generation recipe catalog service."""

        return self._container.recipe_catalog_service()
