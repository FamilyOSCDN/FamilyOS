"""Application dependency container."""

from __future__ import annotations

from familyos_cli.application.generation.generation_pipeline import (
    GenerationPipeline,
)
from familyos_cli.application.specifications.specification_service import (
    SpecificationService,
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
from familyos_cli.application.use_cases.get_domain_specification import (
    GetDomainSpecificationUseCase,
)
from familyos_cli.bootstrap.runtime_factory import RuntimeFactory
from familyos_cli.domain.generation.domain_generation_planner import (
    DomainGenerationPlanner,
)
from familyos_cli.domain.specifications.domain_specification_registry import (
    DomainSpecificationRegistry,
)
from familyos_cli.infrastructure.filesystem.project_generator import (
    ProjectGenerator,
)
from familyos_cli.plugins.runtime.plugin_runtime import PluginRuntime


class ApplicationContainer:
    """Application dependency container."""

    def __init__(self) -> None:
        """Initialize container."""

        self.domain_specification_registry = (
            DomainSpecificationRegistry()
        )

        self.specification_service = SpecificationService(
            self.domain_specification_registry,
        )

        self.plugin_runtime = self._create_runtime()

    def _create_runtime(self) -> PluginRuntime:
        """Create plugin runtime."""

        return RuntimeFactory.create()

    def create_domain_use_case(self) -> CreateDomainUseCase:
        """Create domain use case."""

        return CreateDomainUseCase(
            planner=DomainGenerationPlanner(),
            get_specification=GetDomainSpecificationUseCase(
                self.specification_service,
            ),
        )

    def create_artifact_use_case(self) -> CreateArtifactUseCase:
        """Create artifact use case."""

        return CreateArtifactUseCase()

    def create_project_use_case(self) -> CreateProjectUseCase:
        """Create project use case."""

        pipeline = GenerationPipeline(
            generator=ProjectGenerator(
                runtime=self.plugin_runtime,
            ),
            runtime=self.plugin_runtime,
        )

        return CreateProjectUseCase(
            pipeline=pipeline,
        )
