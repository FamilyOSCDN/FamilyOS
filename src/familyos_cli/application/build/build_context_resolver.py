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
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.dependency_state_provider import (
    DependencyStateProvider,
)
from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.environment_state_provider import (
    EnvironmentStateProvider,
)
from familyos_cli.application.build.toolchain_state import ToolchainState
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
        environment_state_provider: EnvironmentStateProvider | None = None,
    ) -> None:
        self._source_state_provider = source_state_provider
        self._dependency_state_provider = (
            dependency_state_provider or DependencyStateProvider()
        )
        self._toolchain_state_provider = (
            toolchain_state_provider or ToolchainStateProvider()
        )
        self._environment_state_provider = (
            environment_state_provider or EnvironmentStateProvider()
        )
        self._project_root = project_root

    def resolve(
        self,
        output_dir: Path,
        *,
        build_id: BuildId,
        profile: BuildProfile,
        target: BuildTarget,
        functional_validation: bool,
        evidence_output: Path | None = None,
        toolchain_state: ToolchainState | None = None,
        environment_state: EnvironmentState | None = None,
        runtime_version: str | None = None,
    ) -> BuildContext:
        """Resolve the immutable context before significant execution."""

        resolved_output_dir = self._resolve_path(output_dir)
        resolved_evidence_output = (
            None
            if evidence_output is None
            else self._resolve_path(evidence_output)
        )

        source_state = self._source_state_provider.observe(
            project_root=self._project_root,
        )

        dependency_state = self._dependency_state_provider.capture(
            project_root=self._project_root,
        )

        effective_toolchain_state = (
            toolchain_state
            if toolchain_state is not None
            else self._toolchain_state_provider.capture()
        )

        effective_environment_state = (
            environment_state
            if environment_state is not None
            else self._environment_state_provider.capture()
        )

        effective_runtime_version = (
            runtime_version
            if runtime_version is not None
            else platform.python_version()
        )

        return BuildContext(
            build_id=build_id,
            source_state=source_state,
            dependency_state=dependency_state,
            toolchain_state=effective_toolchain_state,
            environment_state=effective_environment_state,
            profile=profile,
            target=target,
            runtime_version=effective_runtime_version,
            effective_configuration=BuildEffectiveConfiguration(
                functional_validation=functional_validation,
            ),
            output_dir=resolved_output_dir,
            evidence_output=resolved_evidence_output,
        )

    def _resolve_path(self, path: Path) -> Path:
        """Resolve one invocation path against the canonical project root."""

        candidate = (
            path
            if path.is_absolute()
            else self._project_root / path
        )
        return candidate.resolve(strict=False)
