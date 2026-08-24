"""Canonical package-build application use case."""

from __future__ import annotations

import platform
from collections.abc import Callable
from pathlib import Path
from time import perf_counter

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
from familyos_cli.application.build.build_execution_observation import (
    BuildExecutionObservation,
    BuildExecutionStage,
    BuildExecutionStageStatus,
)
from familyos_cli.application.build.build_id_generator import BuildIdGenerator
from familyos_cli.application.build.build_input_stager import (
    BuildInputStager,
)
from familyos_cli.application.build.build_input_validator import (
    BuildInputValidator,
)
from familyos_cli.application.build.build_profile_registry import (
    validate_profile_target,
)
from familyos_cli.application.build.build_target_registry import (
    get_build_target_definition,
)
from familyos_cli.application.build.build_workspace_initializer import (
    BuildWorkspaceInitializer,
)
from familyos_cli.application.build.dependency_state_provider import (
    DependencyStateProvider,
)
from familyos_cli.application.build.discover_package_artifacts import (
    DiscoverPackageArtifactsUseCase,
)
from familyos_cli.application.build.effective_configuration_validator import (
    EffectiveConfigurationValidator,
)
from familyos_cli.application.build.environment_state_provider import (
    EnvironmentStateProvider,
)
from familyos_cli.application.build.environment_validator import (
    EnvironmentValidator,
)
from familyos_cli.application.build.package_build import (
    PackageBuildResult,
    PackageBuildStatus,
)
from familyos_cli.application.build.repository_layout import RepositoryLayout
from familyos_cli.application.build.repository_layout_validator import (
    RepositoryLayoutValidator,
)
from familyos_cli.application.build.toolchain_policy_provider import (
    ToolchainPolicyProvider,
)
from familyos_cli.application.build.toolchain_state_provider import (
    ToolchainStateProvider,
)
from familyos_cli.application.build.toolchain_validator import (
    ToolchainValidator,
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
        environment_validator: EnvironmentValidator | None = None,
        build_workspace_initializer: BuildWorkspaceInitializer | None = None,
        build_input_stager: BuildInputStager | None = None,
        build_input_validator: BuildInputValidator | None = None,
        repository_layout_validator: RepositoryLayoutValidator | None = None,
        toolchain_policy_provider: ToolchainPolicyProvider | None = None,
        toolchain_validator: ToolchainValidator | None = None,
        effective_configuration_validator: (
            EffectiveConfigurationValidator | None
        ) = None,
        monotonic_clock: Callable[[], float] | None = None,
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
        self._environment_validator = (
            environment_validator or EnvironmentValidator()
        )
        self._build_workspace_initializer = (
            build_workspace_initializer or BuildWorkspaceInitializer()
        )
        self._build_input_stager = (
            build_input_stager or BuildInputStager()
        )
        self._build_input_validator = (
            build_input_validator or BuildInputValidator()
        )
        self._repository_layout_validator = (
            repository_layout_validator or RepositoryLayoutValidator()
        )
        self._toolchain_policy_provider = (
            toolchain_policy_provider or ToolchainPolicyProvider()
        )
        self._toolchain_validator = (
            toolchain_validator or ToolchainValidator()
        )
        self._effective_configuration_validator = (
            effective_configuration_validator
            or EffectiveConfigurationValidator()
        )
        self._monotonic_clock = monotonic_clock or perf_counter

    def execute(
        self,
        output_dir: Path,
        *,
        validate_functionally: bool = False,
        profile: BuildProfile = BuildProfile.DEVELOPMENT,
        target: BuildTarget = BuildTarget.FAMILYOS_CLI_PACKAGE,
        evidence_output: Path | None = None,
    ) -> CanonicalPackageBuildResult:
        """Build the repository package from validated canonical inputs."""

        target_definition = get_build_target_definition(target)
        profile_definition = validate_profile_target(profile, target)

        build_id = self._build_id_generator.generate()
        execution_observations: list[BuildExecutionObservation] = []

        input_validation_started = self._monotonic_clock()
        input_validation = self._build_input_validator.validate(
            project_root=self._project_root,
            target_definition=target_definition,
        )

        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.VALIDATE_INPUTS,
                started_at=input_validation_started,
                successful=input_validation.successful,
                diagnostic=input_validation.diagnostic,
            )
        )

        if not input_validation.successful:
            source_state = self._source_state_provider.observe(
                project_root=self._project_root,
            )

            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=self._failed_pre_execution(
                    input_validation.diagnostic,
                ),
                source_state=source_state,
                build_id=build_id,
                execution_observations=tuple(execution_observations),
            )

        repository_layout = RepositoryLayout.from_project_root(
            self._project_root,
        )

        layout_validation_started = self._monotonic_clock()
        layout_validation = (
            self._repository_layout_validator.validate_output_dir(
                layout=repository_layout,
                output_dir=output_dir,
            )
        )
        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.VALIDATE_REPOSITORY_LAYOUT,
                started_at=layout_validation_started,
                successful=layout_validation.successful,
                diagnostic=layout_validation.diagnostic,
            )
        )

        if not layout_validation.successful:
            source_state = self._source_state_provider.observe(
                project_root=self._project_root,
            )

            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=self._failed_pre_execution(
                    layout_validation.diagnostic,
                ),
                source_state=source_state,
                build_id=build_id,
                execution_observations=tuple(execution_observations),
            )

        evidence_layout_validation = (
            self._repository_layout_validator.validate_evidence_output(
                layout=repository_layout,
                evidence_output=evidence_output,
                package_output_dir=output_dir,
            )
        )

        toolchain_started = self._monotonic_clock()
        try:
            toolchain_policy = self._toolchain_policy_provider.resolve(
                project_root=self._project_root,
            )
            runtime_version = platform.python_version()
            toolchain_state = self._toolchain_state_provider.capture()
        except ValueError as error:
            execution_observations.append(
                self._execution_observation(
                    stage=BuildExecutionStage.VALIDATE_TOOLCHAIN,
                    started_at=toolchain_started,
                    successful=False,
                    diagnostic=str(error),
                )
            )

            source_state = self._source_state_provider.observe(
                project_root=self._project_root,
            )

            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=self._failed_pre_execution(str(error)),
                source_state=source_state,
                build_id=build_id,
                execution_observations=tuple(execution_observations),
            )

        toolchain_validation = self._toolchain_validator.validate(
            runtime_version=runtime_version,
            toolchain_state=toolchain_state,
            runtime_requirement=toolchain_policy.runtime_requirement,
            distribution_requirements=(
                toolchain_policy.requirements_by_distribution
            ),
        )

        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.VALIDATE_TOOLCHAIN,
                started_at=toolchain_started,
                successful=toolchain_validation.successful,
                diagnostic=toolchain_validation.diagnostic,
            )
        )

        if not toolchain_validation.successful:
            source_state = self._source_state_provider.observe(
                project_root=self._project_root,
            )

            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=self._failed_pre_execution(
                    toolchain_validation.diagnostic,
                ),
                source_state=source_state,
                build_id=build_id,
                execution_observations=tuple(execution_observations),
            )

        environment_started = self._monotonic_clock()
        try:
            environment_state = self._environment_state_provider.capture()
        except ValueError as error:
            execution_observations.append(
                self._execution_observation(
                    stage=BuildExecutionStage.VALIDATE_ENVIRONMENT,
                    started_at=environment_started,
                    successful=False,
                    diagnostic=str(error),
                )
            )

            source_state = self._source_state_provider.observe(
                project_root=self._project_root,
            )

            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=self._failed_pre_execution(str(error)),
                source_state=source_state,
                build_id=build_id,
                execution_observations=tuple(execution_observations),
            )

        environment_validation = self._environment_validator.validate(
            state=environment_state,
        )

        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.VALIDATE_ENVIRONMENT,
                started_at=environment_started,
                successful=environment_validation.successful,
                diagnostic=environment_validation.diagnostic,
            )
        )

        if not environment_validation.successful:
            source_state = self._source_state_provider.observe(
                project_root=self._project_root,
            )

            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=self._failed_pre_execution(
                    environment_validation.diagnostic,
                ),
                source_state=source_state,
                build_id=build_id,
                execution_observations=tuple(execution_observations),
            )

        workspace_started = self._monotonic_clock()
        try:
            workspace = self._build_workspace_initializer.initialize(
                build_id=build_id,
                temporary_directory=Path(
                    environment_state.temporary_directory
                ),
            )
        except OSError as error:
            execution_observations.append(
                self._execution_observation(
                    stage=BuildExecutionStage.INITIALIZE_WORKSPACE,
                    started_at=workspace_started,
                    successful=False,
                    diagnostic=str(error),
                )
            )

            source_state = self._source_state_provider.observe(
                project_root=self._project_root,
            )

            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=self._failed_pre_execution(str(error)),
                source_state=source_state,
                build_id=build_id,
                execution_observations=tuple(execution_observations),
            )

        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.INITIALIZE_WORKSPACE,
                started_at=workspace_started,
                successful=True,
            )
        )

        context_started = self._monotonic_clock()
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
            evidence_output=evidence_output,
            toolchain_state=toolchain_state,
            environment_state=environment_state,
            runtime_version=runtime_version,
        )

        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.RESOLVE_BUILD_CONTEXT,
                started_at=context_started,
                successful=True,
            )
        )

        source_state = build_context.source_state

        effective_configuration_started = self._monotonic_clock()
        effective_configuration_validation = (
            self._effective_configuration_validator.validate(
                context=build_context,
                profile_definition=profile_definition,
                output_layout_validation=layout_validation,
                evidence_layout_validation=evidence_layout_validation,
            )
        )
        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.VALIDATE_EFFECTIVE_CONFIGURATION,
                started_at=effective_configuration_started,
                successful=effective_configuration_validation.successful,
                diagnostic=effective_configuration_validation.diagnostic,
            )
        )

        if not effective_configuration_validation.successful:
            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=self._failed_pre_execution(
                    effective_configuration_validation.diagnostic,
                ),
                source_state=source_state,
                build_context=build_context,
                build_id=build_id,
                execution_observations=tuple(execution_observations),
            )

        staging_started = self._monotonic_clock()
        try:
            staged_build_inputs = self._build_input_stager.stage(
                project_root=self._project_root,
                workspace=workspace,
            )
        except OSError as error:
            execution_observations.append(
                self._execution_observation(
                    stage=BuildExecutionStage.STAGE_BUILD_INPUTS,
                    started_at=staging_started,
                    successful=False,
                    diagnostic=str(error),
                )
            )

            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=self._failed_pre_execution(str(error)),
                source_state=source_state,
                build_context=build_context,
                build_id=build_id,
                execution_observations=tuple(execution_observations),
            )

        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.STAGE_BUILD_INPUTS,
                started_at=staging_started,
                successful=True,
            )
        )

        package_started = self._monotonic_clock()
        execution = self._builder.build(
            project_root=staged_build_inputs.project_root,
            output_dir=build_context.output_dir,
        )
        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.PACKAGE,
                started_at=package_started,
                successful=execution.successful,
                diagnostic=execution.diagnostic,
            )
        )

        if not execution.successful:
            return CanonicalPackageBuildResult(
                status=execution.status,
                execution=execution,
                source_state=source_state,
                build_context=build_context,
                build_id=build_id,
                execution_observations=tuple(execution_observations),
            )

        discovery_started = self._monotonic_clock()
        discovery = self._discoverer.execute(
            output_dir=build_context.output_dir,
            current_outputs=execution.outputs,
        )
        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.DISCOVER_ARTIFACTS,
                started_at=discovery_started,
                successful=discovery.successful,
                diagnostic=discovery.diagnostic,
            )
        )

        if not discovery.successful:
            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=execution,
                source_state=source_state,
                build_context=build_context,
                build_id=build_id,
                execution_observations=tuple(execution_observations),
                discovery=discovery,
            )

        validation_started = self._monotonic_clock()
        validation = self._validator.execute(discovery.candidates)
        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.VALIDATE_ARTIFACTS,
                started_at=validation_started,
                successful=validation.successful,
                diagnostic=validation.diagnostic,
            )
        )

        if not validation.successful:
            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=execution,
                source_state=source_state,
                build_context=build_context,
                build_id=build_id,
                execution_observations=tuple(execution_observations),
                discovery=discovery,
                validation=validation,
            )

        identity_started = self._monotonic_clock()
        artifact_identities = BuildArtifactIdentitiesUseCase().execute(
            validation,
            build_id=build_id,
            source_revision=source_state.revision,
        )
        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.ESTABLISH_ARTIFACT_IDENTITY,
                started_at=identity_started,
                successful=True,
            )
        )

        integrity_started = self._monotonic_clock()
        artifact_integrities = BuildArtifactIntegritiesUseCase().execute(
            artifact_identities,
        )
        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.ESTABLISH_ARTIFACT_INTEGRITY,
                started_at=integrity_started,
                successful=True,
            )
        )

        manifest_started = self._monotonic_clock()
        artifact_manifest = BuildArtifactManifestUseCase().execute(
            artifact_integrities,
            validation,
            build_id=build_id,
        )
        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.BUILD_ARTIFACT_MANIFEST,
                started_at=manifest_started,
                successful=True,
            )
        )

        if not validate_functionally:
            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.SUCCEEDED,
                execution=execution,
                source_state=source_state,
                build_context=build_context,
                build_id=build_id,
                execution_observations=tuple(execution_observations),
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

        functional_validation_started = self._monotonic_clock()
        functional_validation = self._functional_validator.validate(wheel)
        execution_observations.append(
            self._execution_observation(
                stage=BuildExecutionStage.FUNCTIONALLY_VALIDATE_WHEEL,
                started_at=functional_validation_started,
                successful=functional_validation.successful,
                diagnostic=functional_validation.diagnostic,
            )
        )

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
            execution_observations=tuple(execution_observations),
            artifact_identities=artifact_identities,
            artifact_integrities=artifact_integrities,
            artifact_manifest=artifact_manifest,
            discovery=discovery,
            validation=validation,
            functional_validation=functional_validation,
        )

    def _execution_observation(
        self,
        *,
        stage: BuildExecutionStage,
        started_at: float,
        successful: bool,
        diagnostic: str | None = None,
    ) -> BuildExecutionObservation:
        """Create one terminal observation for a completed build stage."""

        return BuildExecutionObservation(
            stage=stage,
            status=(
                BuildExecutionStageStatus.SUCCEEDED
                if successful
                else BuildExecutionStageStatus.FAILED
            ),
            duration_seconds=self._monotonic_clock() - started_at,
            diagnostic=diagnostic,
        )

    @staticmethod
    def _failed_pre_execution(
        diagnostic: str | None,
    ) -> PackageBuildResult:
        """Represent execution blocked by canonical pre-build validation."""

        return PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            diagnostic=diagnostic,
        )
