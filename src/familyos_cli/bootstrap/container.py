"""Application dependency container."""

from __future__ import annotations

import sys
from pathlib import Path

from familyos_cli.application.build import (
    DiscoverPackageArtifactsUseCase,
    RunPackageBuildUseCase,
    ValidatePythonPackageArtifactsUseCase,
)
from familyos_cli.application.build.build_input_validator import (
    BuildInputValidator,
)
from familyos_cli.application.generation.application_recipe_registry_factory import (
    ApplicationRecipeRegistryFactory,
)
from familyos_cli.application.generation.default_generation_strategy_registry import (
    DefaultGenerationStrategyRegistry,
)
from familyos_cli.application.generation.default_recipe_registry import (
    DefaultRecipeRegistry,
)
from familyos_cli.application.generation.domain_generation_catalog_service import (
    DomainGenerationCatalogService,
)
from familyos_cli.application.generation.domain_generation_pipeline import (
    DomainGenerationPipeline,
)
from familyos_cli.application.generation.generation_catalog_service import (
    GenerationCatalogService,
)
from familyos_cli.application.generation.generation_request_factory import (
    GenerationRequestFactory,
)
from familyos_cli.application.generation.mappers.generation_specification_mapper import (
    GenerationSpecificationMapper,
)
from familyos_cli.application.generation.plugin_generation_preset_contributor import (
    PluginGenerationPresetContributor,
)
from familyos_cli.application.generation.preset_recipe_resolver import (
    PresetRecipeResolver,
)
from familyos_cli.application.generation.recipe_catalog_service import (
    RecipeCatalogService,
)
from familyos_cli.application.specifications import (
    DomainSpecificationLoaderService,
    SpecificationService,
)
from familyos_cli.application.testing import PytestResultNormalizer
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
from familyos_cli.application.use_cases.get_domain_specification import (
    GetDomainSpecificationUseCase,
)
from familyos_cli.application.use_cases.resolve_plugins import (
    ResolvePluginsUseCase,
)
from familyos_cli.application.validation import RunCiValidationUseCase
from familyos_cli.application.validation.builtin_plugin_compliance_gate import (
    BuiltinPluginComplianceGate,
)
from familyos_cli.application.validation.pytest_validation_gate import (
    PytestValidationGate,
)
from familyos_cli.application.validation.subprocess_gate import (
    SubprocessValidationGate,
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
from familyos_cli.infrastructure.build import (
    GitSourceStateProvider,
    PythonPackageBuilder,
    PythonWheelFunctionalValidator,
)
from familyos_cli.infrastructure.generation.generation_engine import (
    GenerationEngine,
)
from familyos_cli.infrastructure.specifications import (
    YamlDomainSpecificationLoader,
)
from familyos_cli.infrastructure.testing import PytestRunner
from familyos_cli.plugins.ecosystem.compliance.compliance_engine import (
    ComplianceEngine,
)
from familyos_cli.plugins.ecosystem.compliance.profiles.default_profile_registry import (
    build_default_profile_registry,
)
from familyos_cli.plugins.ecosystem.compliance.rule_registry import RuleRegistry
from familyos_cli.plugins.ecosystem.compliance.rules.default_rule_catalog import (
    DEFAULT_COMPLIANCE_RULES,
)
from familyos_cli.plugins.ecosystem.compliance.validation_context_builder import (
    ValidationContextBuilder,
)
from familyos_cli.plugins.ecosystem.compliance.validators.default_validator_registry import (
    build_default_validator_registry,
)
from familyos_cli.plugins.ecosystem.discovery import (
    PluginDiscovery,
)
from familyos_cli.plugins.ecosystem.installation import (
    PluginInstaller,
)
from familyos_cli.plugins.ecosystem.lifecycle import (
    PluginLifecycleManager,
)
from familyos_cli.plugins.ecosystem.pipeline import (
    PluginResolutionPipeline,
)
from familyos_cli.plugins.ecosystem.resolution import (
    PluginResolver,
)
from familyos_cli.plugins.ecosystem.verification import (
    PluginVerifier,
)
from familyos_cli.plugins.plugin_loader import PluginLoader
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


class ApplicationContainer:
    """Dependency injection container."""

    def __init__(
        self,
    ) -> None:
        """Initialize application dependencies."""

        self._runtime = RuntimeFactory.create()

        self._plugin_discovery = PluginDiscovery()
        self._plugin_resolver = PluginResolver()
        self._plugin_resolution_pipeline = PluginResolutionPipeline(
            discovery=self._plugin_discovery,
            resolver=self._plugin_resolver,
        )
        self._plugin_verifier = PluginVerifier()
        self._plugin_installer = PluginInstaller()
        self._plugin_lifecycle_manager = PluginLifecycleManager()

        self._domain_specification_registry = (
            DomainSpecificationRegistry()
        )

        self._specification_service = SpecificationService(
            self._domain_specification_registry,
        )

        self._builtin_plugins_root = (
            Path(__file__).resolve().parent.parent / "plugins" / "builtin"
        )

        self._compliance_rule_registry = RuleRegistry()
        for rule in DEFAULT_COMPLIANCE_RULES:
            self._compliance_rule_registry.register(rule)

        self._compliance_profile_registry = build_default_profile_registry()
        self._compliance_validator_registry = build_default_validator_registry()

        self._compliance_context_builder = ValidationContextBuilder(
            discovery_root=self._builtin_plugins_root,
        )

        self._compliance_engine = ComplianceEngine(
            rule_registry=self._compliance_rule_registry,
            profile_registry=self._compliance_profile_registry,
            validator_registry=self._compliance_validator_registry,
            context_builder=self._compliance_context_builder,
        )

    def plugin_runtime(
        self,
    ) -> PluginRuntime:
        """Return plugin runtime."""

        return self._runtime

    def plugin_discovery(
        self,
    ) -> PluginDiscovery:
        """Return plugin discovery service."""

        return self._plugin_discovery

    def plugin_resolver(
        self,
    ) -> PluginResolver:
        """Return plugin resolver service."""

        return self._plugin_resolver

    def plugin_resolution_pipeline(
        self,
    ) -> PluginResolutionPipeline:
        """Return plugin resolution pipeline."""

        return self._plugin_resolution_pipeline

    def resolve_plugins_use_case(
        self,
    ) -> ResolvePluginsUseCase:
        """Create plugin resolution use case."""

        return ResolvePluginsUseCase(
            pipeline=self._plugin_resolution_pipeline,
        )

    def check_plugin_compliance_use_case(
        self,
    ) -> CheckPluginComplianceUseCase:
        """Create plugin compliance checking use case."""

        return CheckPluginComplianceUseCase(
            engine=self._compliance_engine,
            profile_registry=self._compliance_profile_registry,
            plugin_loader=PluginLoader(),
            plugins_root=self._builtin_plugins_root,
        )

    def run_ci_validation_use_case(self) -> RunCiValidationUseCase:
        """Create the provider-neutral canonical CI validation use case."""

        project_root = Path(__file__).resolve().parents[3]
        python = sys.executable
        compliance_use_case = self.check_plugin_compliance_use_case()

        return RunCiValidationUseCase(
            gates=(
                SubprocessValidationGate(
                    gate_id="dependency-freshness",
                    command=(python, "scripts/check_dependency_lock.py"),
                    cwd=project_root,
                ),
                SubprocessValidationGate(
                    gate_id="dependency-consistency",
                    command=(python, "-m", "pip", "check"),
                    cwd=project_root,
                ),
                SubprocessValidationGate(
                    gate_id="ruff",
                    command=(python, "-m", "ruff", "check", "src", "tests", "scripts"),
                    cwd=project_root,
                ),
                SubprocessValidationGate(
                    gate_id="mypy",
                    command=(python, "-m", "mypy", "src", "tests"),
                    cwd=project_root,
                ),
                PytestValidationGate(
                    runner=PytestRunner(
                        python_executable=python,
                    ),
                    normalizer=PytestResultNormalizer(),
                    project_root=project_root,
                ),
                BuiltinPluginComplianceGate(
                    use_case=compliance_use_case,
                    plugin_loader=PluginLoader(),
                    plugins_root=self._builtin_plugins_root,
                ),
            ),
        )

    def run_package_build_use_case(self) -> RunPackageBuildUseCase:
        """Create the provider-neutral canonical package-build use case."""

        project_root = Path(__file__).resolve().parents[3]
        return RunPackageBuildUseCase(
            builder=PythonPackageBuilder(),
            discoverer=DiscoverPackageArtifactsUseCase(),
            validator=ValidatePythonPackageArtifactsUseCase(project_root),
            functional_validator=PythonWheelFunctionalValidator(
                project_root=project_root,
                requirements_lock=project_root / "requirements.txt",
            ),
            source_state_provider=GitSourceStateProvider(),
            project_root=project_root,
            build_input_validator=BuildInputValidator(),
        )

    def plugin_verifier(
        self,
    ) -> PluginVerifier:
        """Return plugin verifier service."""

        return self._plugin_verifier

    def plugin_installer(
        self,
    ) -> PluginInstaller:
        """Return plugin installer service."""

        return self._plugin_installer

    def plugin_lifecycle_manager(
        self,
    ) -> PluginLifecycleManager:
        """Return plugin lifecycle manager."""

        return self._plugin_lifecycle_manager

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

    def generation_catalog_service(
        self,
    ) -> GenerationCatalogService:
        """Return generation catalog service."""

        return GenerationCatalogService(
            generation_contributions=(
                self._runtime.generation_contributions()
            ),
        )

    def domain_generation_catalog_service(
        self,
    ) -> DomainGenerationCatalogService:
        """Return domain generation catalog service."""

        return DomainGenerationCatalogService(
            domain_contributions=(
                self._runtime.domain_generation_contributions()
            ),
        )

    def recipe_catalog_service(
        self,
    ) -> RecipeCatalogService:
        """Return generation recipe catalog service."""

        return RecipeCatalogService(
            registry=DefaultRecipeRegistry.create(),
        )

    def create_domain_use_case(
        self,
    ) -> CreateDomainUseCase:
        """Create domain use case."""

        get_specification = GetDomainSpecificationUseCase(
            self._specification_service,
        )

        recipe_registry = (
            ApplicationRecipeRegistryFactory.create(
                self._runtime.generation_recipe_contributions(),
            )
        )

        strategy_registry = (
            DefaultGenerationStrategyRegistry.create(
                recipe_registry,
            )
        )

        template_directories = (
            Path("templates"),
            *self._runtime.template_directories(),
        )

        pipeline = DomainGenerationPipeline(
            planner=DomainGenerationPlanner(),
            specification_mapper=GenerationSpecificationMapper(),
            engine=GenerationEngine(
                template_directories=template_directories,
            ),
            strategy_registry=strategy_registry,
        )

        preset_registry = (
            DefaultGenerationPresetRegistry.create()
        )

        PluginGenerationPresetContributor().contribute(
            preset_registry,
            self._runtime.generation_contributions(),
        )

        request_factory = GenerationRequestFactory(
            preset_recipe_resolver=PresetRecipeResolver(
                GenerationPresetResolver(
                    preset_registry,
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
