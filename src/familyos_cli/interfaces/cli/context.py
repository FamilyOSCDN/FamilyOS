"""CLI command context."""

from __future__ import annotations

from functools import cached_property
from pathlib import Path

from familyos_cli.application.build import RunPackageBuildUseCase
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
from familyos_cli.application.testing import (
    EvaluateTestingEvidenceFreshnessUseCase,
)
from familyos_cli.application.use_cases.check_plugin_compliance import (
    CheckPluginComplianceUseCase,
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
from familyos_cli.application.use_cases.resolve_plugins import (
    ResolvePluginsUseCase,
)
from familyos_cli.application.validation import RunCiValidationUseCase
from familyos_cli.bootstrap import (
    ApplicationContainer,
    ApplicationFactory,
)


class CommandContext:
    """Shared context for CLI commands."""

    def __init__(
        self,
        container: ApplicationContainer | None = None,
        project_root: Path | None = None,
    ) -> None:
        """Initialize CLI context."""

        if container is not None:
            self._container = container
        elif project_root is not None:
            self._container = ApplicationContainer(
                project_root=project_root,
            )
        else:
            self._container = ApplicationFactory.create()

    @property
    def project_root(self) -> Path:
        """Return the repository root selected by CLI composition."""

        return self._container.project_root

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

    @cached_property
    def resolve_plugins(
        self,
    ) -> ResolvePluginsUseCase:
        """Provide plugin resolution use case."""

        return self._container.resolve_plugins_use_case()

    @cached_property
    def check_plugin_compliance(
        self,
    ) -> CheckPluginComplianceUseCase:
        """Provide plugin compliance checking use case."""

        return self._container.check_plugin_compliance_use_case()

    @cached_property
    def testing_evidence_freshness(
        self,
    ) -> EvaluateTestingEvidenceFreshnessUseCase:
        """Provide the canonical Testing Evidence freshness authority."""

        return self._container.testing_evidence_freshness_use_case()

    @cached_property
    def run_ci_validation(self) -> RunCiValidationUseCase:
        """Provide the canonical CI validation use case."""

        return self._container.run_ci_validation_use_case()

    @cached_property
    def run_package_build(self) -> RunPackageBuildUseCase:
        """Provide the canonical package-build use case."""

        return self._container.run_package_build_use_case()
