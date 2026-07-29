"""Application dependency container."""

from __future__ import annotations

from familyos_cli.application.generation.default_generation_strategy_registry import (
    DefaultGenerationStrategyRegistry,
)
from familyos_cli.application.generation.domain_generation_pipeline import (
    DomainGenerationPipeline,
)
from familyos_cli.application.generation.generation_request_factory import (
    GenerationRequestFactory,
)
from familyos_cli.application.generation.mappers.generation_specification_mapper import (
    GenerationSpecificationMapper,
)
from familyos_cli.application.generation.preset_recipe_resolver import (
    PresetRecipeResolver,
)
from familyos_cli.application.specifications import (
    DomainSpecificationLoaderService,
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
from familyos_cli.domain.generation.default_generation_preset_registry import (
    DefaultGenerationPresetRegistry,
)
from familyos_cli.domain.generation.domain_generation_planner import (
    DomainGenerationPlanner,
)
from familyos_cli.domain.generation.generation_preset_resolver import (
    GenerationPresetResolver,
)
from familyos_cli.domain.specifications.domain_specification_registry import (
    DomainSpecificationRegistry,
)
from familyos_cli.infrastructure.generation.generation_engine import (
    GenerationEngine,
)
from familyos_cli.infrastructure.specifications import (
    YamlDomainSpecificationLoader,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


class ApplicationContainer:
    """Dependency injection container."""

    def __init__(
        self,
    ) -> None:
        self._runtime = RuntimeFactory.create()

        self._domain_specification_registry = (
            DomainSpecificationRegistry()
        )

        self._specification_service = SpecificationService(
            self._domain_specification_registry,
        )

    def plugin_runtime(
        self,
    ) -> PluginRuntime:
        """Return plugin runtime."""

        return self._runtime

    def create_project_use_case(
        self,
    ) -> CreateProjectUseCase:
        """Create project use case."""

        return CreateProjectUseCase(
            runtime=self._runtime,
        )

    def create_artifact_use_case(
        self,
    ) -> CreateArtifactUseCase:
        """Create artifact use case."""

        return CreateArtifactUseCase()

    def create_domain_use_case(
        self,
    ) -> CreateDomainUseCase:
        """Create domain use case."""

        get_specification = GetDomainSpecificationUseCase(
            self._specification_service,
        )

        strategy_registry = (
            DefaultGenerationStrategyRegistry.create()
        )

        pipeline = DomainGenerationPipeline(
            planner=DomainGenerationPlanner(),
            specification_mapper=GenerationSpecificationMapper(),
            engine=GenerationEngine(),
            strategy_registry=strategy_registry,
        )

        request_factory = GenerationRequestFactory(
            preset_recipe_resolver=PresetRecipeResolver(
                GenerationPresetResolver(
                    DefaultGenerationPresetRegistry.create(),
                ),
            ),
        )

        return CreateDomainUseCase(
            pipeline=pipeline,
            get_specification=get_specification,
            request_factory=request_factory,
        )

    def domain_specification_loader_service(
        self,
    ) -> DomainSpecificationLoaderService:
        """Create domain specification loader service."""

        loader = YamlDomainSpecificationLoader()

        return DomainSpecificationLoaderService(
            loader=loader,
            service=self._specification_service,
        )


class ApplicationFactory:
    """Application factory."""

    @staticmethod
    def create() -> ApplicationContainer:
        """Create application container."""

        return ApplicationContainer()
