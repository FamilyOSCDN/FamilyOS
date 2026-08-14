"""Canonical package-build application use case."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.artifact_discovery import (
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.discover_package_artifacts import (
    DiscoverPackageArtifactsUseCase,
)
from familyos_cli.application.build.package_build import PackageBuildStatus
from familyos_cli.application.ports.build.package_builder import PackageBuilderPort


class RunPackageBuildUseCase:
    """Delegate canonical Python packaging through the configured port."""

    def __init__(
        self,
        builder: PackageBuilderPort,
        discoverer: DiscoverPackageArtifactsUseCase,
        project_root: Path,
    ) -> None:
        self._builder = builder
        self._discoverer = discoverer
        self._project_root = project_root

    def execute(self, output_dir: Path) -> CanonicalPackageBuildResult:
        """Build the repository package into an explicit output directory."""

        resolved_output_dir = (
            output_dir
            if output_dir.is_absolute()
            else self._project_root / output_dir
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
        return CanonicalPackageBuildResult(
            status=(
                PackageBuildStatus.SUCCEEDED
                if discovery.successful
                else PackageBuildStatus.FAILED
            ),
            execution=execution,
            discovery=discovery,
        )
