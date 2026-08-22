"""Tests for canonical Build Context resolution."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.build_context import (
    BuildProfile,
    BuildTarget,
)
from familyos_cli.application.build.build_context_resolver import (
    BuildContextResolver,
)
from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.dependency_state_provider import (
    DependencyStateProvider,
)
from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.environment_state_provider import (
    EnvironmentStateProvider,
)
from familyos_cli.application.build.source_state import SourceState
from familyos_cli.application.build.toolchain_state import (
    ToolchainState,
    ToolchainVersion,
)
from familyos_cli.application.build.toolchain_state_provider import (
    ToolchainStateProvider,
)
from familyos_cli.application.ports.build.source_state_provider import (
    SourceStateProviderPort,
)

_SOURCE_STATE = SourceState(
    revision="0123456789abcdef0123456789abcdef01234567",
    dirty=False,
)

_TOOLCHAIN_STATE = ToolchainState(
    critical_versions=(
        ToolchainVersion("build", "1.5.0"),
        ToolchainVersion("pip-tools", "7.6.1"),
        ToolchainVersion("setuptools", "84.0.0"),
        ToolchainVersion("wheel", "0.48.0"),
    ),
)

_ENVIRONMENT_STATE = EnvironmentState(
    operating_system="Darwin",
    operating_system_release="24.6.0",
    machine_architecture="arm64",
)


class _SourceStateProvider(SourceStateProviderPort):
    def __init__(
        self,
        events: list[str] | None = None,
    ) -> None:
        self.calls: list[Path] = []
        self.events = events

    def observe(self, *, project_root: Path) -> SourceState:
        self.calls.append(project_root)
        if self.events is not None:
            self.events.append("source-state")
        return _SOURCE_STATE


class _DependencyStateProvider(DependencyStateProvider):
    def __init__(
        self,
        events: list[str] | None = None,
    ) -> None:
        self.calls: list[Path] = []
        self.events = events

    def capture(self, *, project_root: Path) -> DependencyState:
        self.calls.append(project_root)
        if self.events is not None:
            self.events.append("dependency-state")

        return DependencyState(
            declaration_path=project_root / "pyproject.toml",
            declaration_digest="a" * 64,
            lock_path=project_root / "requirements.txt",
            lock_digest="b" * 64,
        )


class _ToolchainStateProvider(ToolchainStateProvider):
    def __init__(
        self,
        events: list[str] | None = None,
    ) -> None:
        self.calls = 0
        self.events = events

    def capture(self) -> ToolchainState:
        self.calls += 1
        if self.events is not None:
            self.events.append("toolchain-state")
        return _TOOLCHAIN_STATE


class _EnvironmentStateProvider(EnvironmentStateProvider):
    def __init__(
        self,
        events: list[str] | None = None,
    ) -> None:
        self.calls = 0
        self.events = events

    def capture(self) -> EnvironmentState:
        self.calls += 1
        if self.events is not None:
            self.events.append("environment-state")
        return _ENVIRONMENT_STATE


def _resolver(
    project_root: Path,
    *,
    source_provider: _SourceStateProvider | None = None,
    dependency_provider: _DependencyStateProvider | None = None,
    toolchain_provider: _ToolchainStateProvider | None = None,
    environment_provider: _EnvironmentStateProvider | None = None,
) -> BuildContextResolver:
    return BuildContextResolver(
        source_provider or _SourceStateProvider(),
        project_root,
        dependency_provider or _DependencyStateProvider(),
        toolchain_provider or _ToolchainStateProvider(),
        environment_provider or _EnvironmentStateProvider(),
    )


def test_resolves_relative_output_from_project_root(
    tmp_path: Path,
) -> None:
    source_provider = _SourceStateProvider()
    dependency_provider = _DependencyStateProvider()
    toolchain_provider = _ToolchainStateProvider()
    environment_provider = _EnvironmentStateProvider()
    project_root = tmp_path / "project"

    context = _resolver(
        project_root,
        source_provider=source_provider,
        dependency_provider=dependency_provider,
        toolchain_provider=toolchain_provider,
        environment_provider=environment_provider,
    ).resolve(
        Path("dist"),
        profile=BuildProfile.VALIDATION,
        target=BuildTarget.FAMILYOS_CLI_PACKAGE,
        functional_validation=False,
    )

    assert context.output_dir == project_root / "dist"
    assert source_provider.calls == [project_root]
    assert dependency_provider.calls == [project_root]
    assert toolchain_provider.calls == 1
    assert environment_provider.calls == 1


def test_preserves_absolute_output_path(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    output_dir = tmp_path / "artifacts"

    context = _resolver(project_root).resolve(
        output_dir,
        profile=BuildProfile.CI,
        target=BuildTarget.FAMILYOS_CLI_PACKAGE,
        functional_validation=True,
    )

    assert context.output_dir == output_dir


def test_captures_source_dependency_toolchain_environment_profile_target_and_configuration(
    tmp_path: Path,
) -> None:
    context = _resolver(tmp_path).resolve(
        Path("dist"),
        profile=BuildProfile.DEVELOPMENT,
        target=BuildTarget.FAMILYOS_CLI_PACKAGE,
        functional_validation=True,
    )

    assert context.source_state is _SOURCE_STATE
    assert context.dependency_state.declaration_path == (
        tmp_path / "pyproject.toml"
    )
    assert context.dependency_state.declaration_digest == "a" * 64
    assert context.dependency_state.lock_path == (
        tmp_path / "requirements.txt"
    )
    assert context.dependency_state.lock_digest == "b" * 64
    assert context.toolchain_state is _TOOLCHAIN_STATE
    assert context.environment_state is _ENVIRONMENT_STATE
    assert context.profile is BuildProfile.DEVELOPMENT
    assert context.target is BuildTarget.FAMILYOS_CLI_PACKAGE
    assert context.effective_configuration.functional_validation is True


def test_captures_runtime_version(
    tmp_path: Path,
) -> None:
    context = _resolver(tmp_path).resolve(
        Path("dist"),
        profile=BuildProfile.VALIDATION,
        target=BuildTarget.FAMILYOS_CLI_PACKAGE,
        functional_validation=False,
    )

    parts = context.runtime_version.split(".")

    assert len(parts) >= 2
    assert all(part.isdigit() for part in parts[:2])


def test_environment_state_is_resolved_before_context_is_returned(
    tmp_path: Path,
) -> None:
    events: list[str] = []

    context = BuildContextResolver(
        _SourceStateProvider(events),
        tmp_path,
        _DependencyStateProvider(events),
        _ToolchainStateProvider(events),
        _EnvironmentStateProvider(events),
    ).resolve(
        Path("dist"),
        profile=BuildProfile.CI,
        target=BuildTarget.FAMILYOS_CLI_PACKAGE,
        functional_validation=False,
    )

    assert events == [
        "source-state",
        "dependency-state",
        "toolchain-state",
        "environment-state",
    ]
    assert context.dependency_state.lock_digest == "b" * 64
    assert context.toolchain_state is _TOOLCHAIN_STATE
    assert context.environment_state is _ENVIRONMENT_STATE
