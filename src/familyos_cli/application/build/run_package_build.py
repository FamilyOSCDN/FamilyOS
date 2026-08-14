"""Canonical package-build application use case."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.package_build import PackageBuildResult
from familyos_cli.application.ports.build.package_builder import PackageBuilderPort


class RunPackageBuildUseCase:
    """Delegate canonical Python packaging through the configured port."""

    def __init__(self, builder: PackageBuilderPort, project_root: Path) -> None:
        self._builder = builder
        self._project_root = project_root

    def execute(self, output_dir: Path) -> PackageBuildResult:
        """Build the repository package into an explicit output directory."""

        resolved_output_dir = (
            output_dir
            if output_dir.is_absolute()
            else self._project_root / output_dir
        )
        return self._builder.build(
            project_root=self._project_root,
            output_dir=resolved_output_dir,
        )
