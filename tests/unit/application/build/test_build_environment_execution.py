"""Tests for build-environment capture before canonical execution."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build import (
    DiscoverPackageArtifactsUseCase,
    PackageBuildResult,
    PackageBuildStatus,
    RunPackageBuildUseCase,
    SourceState,
    ValidatePythonPackageArtifactsUseCase,
)
from familyos_cli.application.build.artifact_discovery import DiscoveredArtifact
from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.dependency_state_provider import (
    DependencyStateProvider,
)
from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.environment_state_provider import (
    EnvironmentStateProvider,
)
from familyos_cli.application.build.package_functional_validation import (
    PythonWheelFunctionalValidationResult,
)
from familyos_cli.application.build.toolchain_state import (
    ToolchainState,
    ToolchainVersion,
)
from familyos_cli.application.build.toolchain_state_provider import (
    ToolchainStateProvider,
)
from familyos_cli.application.ports.build.package_builder import PackageBuilderPort
from familyos_cli.application.ports.build.python_wheel_functional_validator import (
    PythonWheelFunctionalValidatorPort,
)
from familyos_cli.application.ports.build.source_state_provider import (
    SourceStateProviderPort,
)


class _SourceStateProvider(SourceStateProviderPort):
    def __init__(self, events: list[str]) -> None:
        self._events = events

    def observe(self, *, project_root: Path) -> SourceState:
        del project_root
        self._events.append("source-state")
        return SourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=False,
        )


class _DependencyStateProvider(DependencyStateProvider):
    def __init__(self, events: list[str]) -> None:
        self._events = events

    def capture(self, *, project_root: Path) -> DependencyState:
        self._events.append("dependency-state")
        return DependencyState(
            declaration_path=project_root / "pyproject.toml",
            declaration_digest="a" * 64,
            lock_path=project_root / "requirements.txt",
            lock_digest="b" * 64,
        )


class _ToolchainStateProvider(ToolchainStateProvider):
    def __init__(self, events: list[str]) -> None:
        self._events = events

    def capture(self) -> ToolchainState:
        self._events.append("toolchain-state")
        return ToolchainState(
            critical_versions=(
                ToolchainVersion("build", "1.5.0"),
                ToolchainVersion("pip-tools", "7.6.1"),
                ToolchainVersion("setuptools", "84.0.0"),
                ToolchainVersion("wheel", "0.48.0"),
            ),
        )


class _EnvironmentStateProvider(EnvironmentStateProvider):
    def __init__(self, events: list[str]) -> None:
        self._events = events

    def capture(self) -> EnvironmentState:
        self._events.append("environment-state")
        return EnvironmentState(
            operating_system="Darwin",
            operating_system_release="24.6.0",
            machine_architecture="arm64",
        )


class _Builder(PackageBuilderPort):
    def __init__(self, events: list[str]) -> None:
        self._events = events

    def build(
        self,
        *,
        project_root: Path,
        output_dir: Path,
    ) -> PackageBuildResult:
        del project_root, output_dir
        self._events.append("build")
        return PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            diagnostic="expected test failure",
        )


class _FunctionalValidator(PythonWheelFunctionalValidatorPort):
    def validate(
        self,
        candidate: DiscoveredArtifact,
    ) -> PythonWheelFunctionalValidationResult:
        raise AssertionError(
            f"functional validation must not execute: {candidate}"
        )


def _write_toolchain_policy(project_root: Path) -> None:
    from familyos_cli.application.build.dependency_input_freshness import (
        DEPENDENCY_DIGEST_PREFIX,
        dependency_input_digest,
    )

    (project_root / "pyproject.toml").write_text(
        "[build-system]\n"
        'requires = ["setuptools>=75", "wheel"]\n'
        'build-backend = "setuptools.build_meta"\n'
        "\n"
        "[project]\n"
        'name = "familyos-cli-test"\n'
        'version = "0.0.0"\n'
        'requires-python = ">=3.13"\n'
        'dependencies = []\n'
        "\n"
        "[project.optional-dependencies]\n"
        'dev = [\n'
        '    "build>=1.5",\n'
        '    "pytest>=8.4",\n'
        '    "ruff>=0.12",\n'
        '    "mypy>=1.17",\n'
        '    "pip-tools==7.6.1",\n'
        ']\n'
        "\n"
        "[tool.mypy]\n"
        'python_version = "3.13"\n',
        encoding="utf-8",
    )
    (project_root / "src").mkdir()
    digest = dependency_input_digest(project_root / "pyproject.toml")
    (project_root / "requirements.txt").write_text(
        f"{DEPENDENCY_DIGEST_PREFIX}{digest}\n"
        "# canonical test lock\n",
        encoding="utf-8",
    )


def test_environment_state_is_captured_before_package_execution(
    tmp_path: Path,
) -> None:
    events: list[str] = []
    _write_toolchain_policy(tmp_path)

    result = RunPackageBuildUseCase(
        builder=_Builder(events),
        discoverer=DiscoverPackageArtifactsUseCase(),
        validator=ValidatePythonPackageArtifactsUseCase(tmp_path),
        functional_validator=_FunctionalValidator(),
        source_state_provider=_SourceStateProvider(events),
        project_root=tmp_path,
        dependency_state_provider=_DependencyStateProvider(events),
        toolchain_state_provider=_ToolchainStateProvider(events),
        environment_state_provider=_EnvironmentStateProvider(events),
    ).execute(Path("dist"))

    assert events == [
        "toolchain-state",
        "environment-state",
        "source-state",
        "dependency-state",
        "build",
    ]

    assert result.build_context is not None
    assert result.build_context.environment_state == EnvironmentState(
        operating_system="Darwin",
        operating_system_release="24.6.0",
        machine_architecture="arm64",
    )
