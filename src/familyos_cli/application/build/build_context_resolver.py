"""Resolve the immutable effective Build Context before build execution."""

from __future__ import annotations

import platform
from pathlib import Path

from familyos_cli.application.build.build_context import (
    BuildContext,
    BuildEffectiveConfiguration,
    BuildProfile,
    BuildTarget,
)
from familyos_cli.application.build.dependency_state_provider import (
    DependencyStateProvider,
)
from familyos_cli.application.build.toolchain_state_provider import (
    ToolchainStateProvider,
)
from familyos_cli.application.ports.build.source_state_provider import (
    SourceStateProviderPort,
)


class BuildContextResolver:
    """Resolve non-sensitive canonical Build Context from explicit inputs."""

    def __init__(
        self,
        source_state_provider: SourceStateProviderPort,
        project_root: Path,
        dependency_state_provider: DependencyStateProvider | None = None,
        toolchain_state_provider: ToolchainStateProvider | None = None,
    ) -> None:
        self._source_state_provider = source_state_provider
        self._dependency_state_provider = (
            dependency_state_provider or DependencyStateProvider()
        )
        self._toolchain_state_provider = (
            toolchain_state_provider or ToolchainStateProvider()
        )
        self._project_root = project_root

    def resolve(
        self,
        output_dir: Path,
        *,
        profile: BuildProfile,
        target: BuildTarget,
        functional_validation: bool,
    ) -> BuildContext:
        """Resolve the immutable context before significant execution."""

        resolved_output_dir = (
            output_dir
            if output_dir.is_absolute()
            else self._project_root / output_dir
        )

        source_state = self._source_state_provider.observe(
            project_root=self._project_root,
        )

        dependency_state = self._dependency_state_provider.capture(
            project_root=self._project_root,
        )

        toolchain_state = self._toolchain_state_provider.capture()

        return BuildContext(
            source_state=source_state,
            dependency_state=dependency_state,
            toolchain_state=toolchain_state,
            profile=profile,
            target=target,
            runtime_version=platform.python_version(),
            effective_configuration=BuildEffectiveConfiguration(
                functional_validation=functional_validation,
            ),
            output_dir=resolved_output_dir,
        )
