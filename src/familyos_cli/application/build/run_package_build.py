"""Canonical package-build application use case."""

from __future__ import annotations

import platform
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
        build_input_validator: BuildInputValidator | None = None,
        repository_layout_validator: RepositoryLayoutValidator | None = None,
        toolchain_policy_provider: ToolchainPolicyProvider | None = None,
        toolchain_validator: ToolchainValidator | None = None,
        effective_configuration_validator: (
            EffectiveConfigurationValidator | None
        ) = None,
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
                execution=self._failed_pre_execution(
                    input_validation.diagnostic,
                ),
                source_state=source_state,
                build_id=build_id,
            )

        repository_layout = RepositoryLayout.from_project_root(
            self._project_root,
        )

        layout_validation = (
            self._repository_layout_validator.validate_output_dir(
                layout=repository_layout,
                output_dir=output_dir,
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
            )

        evidence_layout_validation = (
            self._repository_layout_validator.validate_evidence_output(
                layout=repository_layout,
                evidence_output=evidence_output,
                package_output_dir=output_dir,
            )
        )

        try:
            toolchain_policy = self._toolchain_policy_provider.resolve(
                project_root=self._project_root,
            )
            runtime_version = platform.python_version()
            toolchain_state = self._toolchain_state_provider.capture()
        except ValueError as error:
            source_state = self._source_state_provider.observe(
                project_root=self._project_root,
            )

            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=self._failed_pre_execution(str(error)),
                source_state=source_state,
                build_id=build_id,
            )

        toolchain_validation = self._toolchain_validator.validate(
            runtime_version=runtime_version,
            toolchain_state=toolchain_state,
            runtime_requirement=toolchain_policy.runtime_requirement,
            distribution_requirements=(
                toolchain_policy.requirements_by_distribution
            ),
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
            )

        try:
            environment_state = self._environment_state_provider.capture()
        except ValueError as error:
            source_state = self._source_state_provider.observe(
                project_root=self._project_root,
            )

            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=self._failed_pre_execution(str(error)),
                source_state=source_state,
                build_id=build_id,
            )

        environment_validation = self._environment_validator.validate(
            state=environment_state,
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
            evidence_output=evidence_output,
            toolchain_state=toolchain_state,
            environment_state=environment_state,
            runtime_version=runtime_version,
        )

        source_state = build_context.source_state

        effective_configuration_validation = (
            self._effective_configuration_validator.validate(
                context=build_context,
                profile_definition=profile_definition,
                output_layout_validation=layout_validation,
                evidence_layout_validation=evidence_layout_validation,
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
            )

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
    def _failed_pre_execution(
        diagnostic: str | None,
    ) -> PackageBuildResult:
        """Represent execution blocked by canonical pre-build validation."""

        return PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            diagnostic=diagnostic,
        )
