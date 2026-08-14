"""Canonical package-build application use case."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.artifact_discovery import (
    ArtifactClass,
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.discover_package_artifacts import (
    DiscoverPackageArtifactsUseCase,
)
from familyos_cli.application.build.package_build import PackageBuildStatus
from familyos_cli.application.build.validate_python_package_artifacts import (
    ValidatePythonPackageArtifactsUseCase,
)
from familyos_cli.application.ports.build.package_builder import PackageBuilderPort
from familyos_cli.application.ports.build.python_wheel_functional_validator import (
    PythonWheelFunctionalValidatorPort,
)


class RunPackageBuildUseCase:
    """Delegate canonical Python packaging through the configured port."""

    def __init__(
        self,
        builder: PackageBuilderPort,
        discoverer: DiscoverPackageArtifactsUseCase,
        validator: ValidatePythonPackageArtifactsUseCase,
        functional_validator: PythonWheelFunctionalValidatorPort,
        project_root: Path,
    ) -> None:
        self._builder = builder
        self._discoverer = discoverer
        self._validator = validator
        self._functional_validator = functional_validator
        self._project_root = project_root

    def execute(
        self,
        output_dir: Path,
        *,
        validate_functionally: bool = False,
    ) -> CanonicalPackageBuildResult:
        """Build the repository package into an explicit output directory."""

        resolved_output_dir = (
            output_dir if output_dir.is_absolute() else self._project_root / output_dir
        )
        execution = self._builder.build(
            project_root=self._project_root,
            output_dir=resolved_output_dir,
        )
        if not execution.successful:
            return CanonicalPackageBuildResult(
                status=execution.status,
                execution=execution,
            )

        discovery = self._discoverer.execute(
            output_dir=resolved_output_dir,
            current_outputs=execution.outputs,
        )
        if not discovery.successful:
            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=execution,
                discovery=discovery,
            )

        validation = self._validator.execute(discovery.candidates)
        if not validation.successful:
            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.FAILED,
                execution=execution,
                discovery=discovery,
                validation=validation,
            )
        if not validate_functionally:
            return CanonicalPackageBuildResult(
                status=PackageBuildStatus.SUCCEEDED,
                execution=execution,
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
            discovery=discovery,
            validation=validation,
            functional_validation=functional_validation,
        )
