"""Canonical package-build application use case."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.artifact_discovery import (
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.build_artifact_identities import (
    BuildArtifactIdentitiesUseCase,
)
from familyos_cli.application.build.build_artifact_integrities import (
    BuildArtifactIntegritiesUseCase,
)
from familyos_cli.application.build.build_artifact_manifest import (
    BuildArtifactManifestUseCase,
)
from familyos_cli.application.build.build_context import (
    BuildProfile,
    BuildTarget,
)
from familyos_cli.application.build.build_context_resolver import (
    BuildContextResolver,
)
from familyos_cli.application.build.build_id_generator import BuildIdGenerator
from familyos_cli.application.build.build_input_validator import (
    BuildInputValidator,
)
from familyos_cli.application.build.build_profile_registry import (
    validate_profile_target,
)
from familyos_cli.application.build.build_target_registry import (
    get_build_target_definition,
)
from familyos_cli.application.build.dependency_state_provider import (
    DependencyStateProvider,
)
from familyos_cli.application.build.discover_package_artifacts import (
    DiscoverPackageArtifactsUseCase,
)
from familyos_cli.application.build.environment_state_provider import (
    EnvironmentStateProvider,
)
from familyos_cli.application.build.package_build import (
    PackageBuildResult,
    PackageBuildStatus,
)
from familyos_cli.application.build.toolchain_state_provider import (
    ToolchainStateProvider,
)
from familyos_cli.application.build.validate_python_package_artifacts import (
    ValidatePythonPackageArtifactsUseCase,
)
from familyos_cli.application.ports.build.package_builder import PackageBuilderPort
from familyos_cli.application.ports.build.python_wheel_functional_validator import (
    PythonWheelFunctionalValidatorPort,
)
from familyos_cli.application.ports.build.source_state_provider import (
    SourceStateProviderPort,
)


class RunPackageBuildUseCase:
    """Delegate canonical Python packaging through the configured ports."""

    def __init__(
        self,
        builder: PackageBuilderPort,
        discoverer: DiscoverPackageArtifactsUseCase,
        validator: ValidatePythonPackageArtifactsUseCase,
        functional_validator: PythonWheelFunctionalValidatorPort,
        source_state_provider: SourceStateProviderPort,
        project_root: Path,
        build_id_generator: BuildIdGenerator | None = None,
        dependency_state_provider: DependencyStateProvider | None = None,
        toolchain_state_provider: ToolchainStateProvider | None = None,
        environment_state_provider: EnvironmentStateProvider | None = None,
        build_input_validator: BuildInputValidator | None = None,
    ) -> None:
        self._builder = builder
        self._discoverer = discoverer
        self._validator = validator
        self._functional_validator = functional_validator
        self._source_state_provider = source_state_provider
        self._project_root = project_root
        self._build_id_generator = build_id_generator or BuildIdGenerator()
        self._dependency_state_provider = (
            dependency_state_provider or DependencyStateProvider()
        )
        self._toolchain_state_provider = (
            toolchain_state_provider or ToolchainStateProvider()
        )
        self._environment_state_provider = (
            environment_state_provider or EnvironmentStateProvider()
        )
        self._build_input_validator = build_input_validator

    def execute(
        self,
        output_dir: Path,
        *,
        validate_functionally: bool = False,
        profile: BuildProfile = BuildProfile.DEVELOPMENT,
        target: BuildTarget = BuildTarget.FAMILYOS_CLI_PACKAGE,
    ) -> CanonicalPackageBuildResult:
        """Build the repository package from validated canonical inputs."""

        target_definition = get_build_target_definition(target)
        validate_profile_target(profile, target)

        build_id = self._build_id_generator.generate()

        if self._build_input_validator is not None:
            input_validation = self._build_input_validator.validate(
                project_root=self._project_root,
                target_definition=target_definition,
            )

            if not input_validation.successful:
                source_state = self._source_state_provider.observe(
                    project_root=self._project_root,
                )

                return CanonicalPackageBuildResult(
                    status=PackageBuildStatus.FAILED,
                    execution=self._failed_input_execution(
                        input_validation.diagnostic,
                    ),
                    source_state=source_state,
                    build_id=build_id,
                )

        build_context = BuildContextResolver(
            self._source_state_provider,
            self._project_root,
            self._dependency_state_provider,
            self._toolchain_state_provider,
            self._environment_state_provider,
        ).resolve(
            output_dir,
            build_id=build_id,
            profile=profile,
            target=target,
            functional_validation=validate_functionally,
        )

        source_state = build_context.source_state

        execution = self._builder.build(
            project_root=self._project_root,
            output_dir=build_context.output_dir,
        )

        if not execution.successful:
            return CanonicalPackageBuildResult(
                status=execution.status,
                execution=execution,
                source_state=source_state,
                build_context=build_context,
                build_id=build_id,
            )

        discovery = self._discoverer.execute(
            output_dir=build_context.output_dir,
            current_outputs=execution.outputs,
        )

        if not discovery.successful:
            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=execution,
                source_state=source_state,
                build_context=build_context,
                build_id=build_id,
                discovery=discovery,
            )

        validation = self._validator.execute(discovery.candidates)

        if not validation.successful:
            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=execution,
                source_state=source_state,
                build_context=build_context,
                build_id=build_id,
                discovery=discovery,
                validation=validation,
            )

        artifact_identities = BuildArtifactIdentitiesUseCase().execute(
            validation,
            build_id=build_id,
            source_revision=source_state.revision,
        )

        artifact_integrities = BuildArtifactIntegritiesUseCase().execute(
            artifact_identities,
        )

        artifact_manifest = BuildArtifactManifestUseCase().execute(
            artifact_integrities,
            validation,
            build_id=build_id,
        )

        if not validate_functionally:
            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.SUCCEEDED,
                execution=execution,
                source_state=source_state,
                build_context=build_context,
                build_id=build_id,
                artifact_identities=artifact_identities,
                artifact_integrities=artifact_integrities,
                artifact_manifest=artifact_manifest,
                discovery=discovery,
                validation=validation,
            )

        wheel = next(
            candidate
            for candidate in discovery.candidates
            if candidate.artifact_class is ArtifactClass.PYTHON_WHEEL
        )

        functional_validation = self._functional_validator.validate(wheel)

        return CanonicalPackageBuildResult(
            status=(
                PackageBuildStatus.SUCCEEDED
                if functional_validation.successful
                else PackageBuildStatus.FAILED
            ),
            execution=execution,
            source_state=source_state,
            build_context=build_context,
            build_id=build_id,
            artifact_identities=artifact_identities,
            artifact_integrities=artifact_integrities,
            artifact_manifest=artifact_manifest,
            discovery=discovery,
            validation=validation,
            functional_validation=functional_validation,
        )

    @staticmethod
    def _failed_input_execution(
        diagnostic: str | None,
    ) -> PackageBuildResult:
        """Represent execution blocked by canonical input validation."""

        return PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            diagnostic=diagnostic,
        )
