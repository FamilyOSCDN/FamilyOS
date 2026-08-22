"""Tests for minimal canonical build identity."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

from familyos_cli.application.build import (
    BuildId,
    BuildIdGenerator,
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

_FIRST_UUID = UUID("01234567-89ab-4cde-8f01-23456789abcd")
_SECOND_UUID = UUID("fedcba98-7654-4321-8abc-def012345678")


class _FailingBuilder(PackageBuilderPort):
    def __init__(self, events: list[str] | None = None) -> None:
        self.events = events

    def build(
        self,
        *,
        project_root: Path,
        output_dir: Path,
    ) -> PackageBuildResult:
        del project_root, output_dir
        if self.events is not None:
            self.events.append("build")
        return PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            exit_code=2,
            diagnostic="backend failed",
        )


class _SourceStateProvider(SourceStateProviderPort):
    def __init__(self, events: list[str] | None = None) -> None:
        self.events = events

    def observe(self, *, project_root: Path) -> SourceState:
        del project_root
        if self.events is not None:
            self.events.append("source-state")
        return SourceState(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=False,
        )


class _DependencyStateProvider(DependencyStateProvider):
    def capture(self, *, project_root: Path) -> DependencyState:
        return DependencyState(
            declaration_path=project_root / "pyproject.toml",
            declaration_digest="a" * 64,
            lock_path=project_root / "requirements.txt",
            lock_digest="b" * 64,
        )


class _ToolchainStateProvider(ToolchainStateProvider):
    def capture(self) -> ToolchainState:
        return ToolchainState(
            critical_versions=(
                ToolchainVersion("build", "1.5.0"),
                ToolchainVersion("pip-tools", "7.6.1"),
                ToolchainVersion("setuptools", "84.0.0"),
                ToolchainVersion("wheel", "0.48.0"),
            ),
        )


class _FunctionalValidator(PythonWheelFunctionalValidatorPort):
    def validate(
        self,
        candidate: DiscoveredArtifact,
    ) -> PythonWheelFunctionalValidationResult:
        raise AssertionError(
            f"functional validation must not run for failed build: {candidate}"
        )


def test_build_id_has_canonical_uuid_string_representation() -> None:
    build_id = BuildId(_FIRST_UUID)

    assert str(build_id) == "01234567-89ab-4cde-8f01-23456789abcd"


def test_build_id_generator_uses_injected_uuid_factory() -> None:
    generated = BuildIdGenerator(lambda: _FIRST_UUID).generate()

    assert generated == BuildId(_FIRST_UUID)


def test_build_id_generator_distinguishes_separate_executions() -> None:
    values = iter((_FIRST_UUID, _SECOND_UUID))
    generator = BuildIdGenerator(lambda: next(values))

    first = generator.generate()
    second = generator.generate()

    assert first == BuildId(_FIRST_UUID)
    assert second == BuildId(_SECOND_UUID)
    assert first != second


def test_build_id_is_generated_before_source_observation_and_execution(
    tmp_path: Path,
) -> None:
    events: list[str] = []

    def uuid_factory() -> UUID:
        events.append("build-id")
        return _FIRST_UUID

    result = RunPackageBuildUseCase(
        builder=_FailingBuilder(events),
        discoverer=DiscoverPackageArtifactsUseCase(),
        validator=ValidatePythonPackageArtifactsUseCase(tmp_path),
        functional_validator=_FunctionalValidator(),
        source_state_provider=_SourceStateProvider(events),
        project_root=tmp_path,
        build_id_generator=BuildIdGenerator(uuid_factory),
        dependency_state_provider=_DependencyStateProvider(),
        toolchain_state_provider=_ToolchainStateProvider(),
    ).execute(Path("dist"))

    assert events == ["build-id", "source-state", "build"]
    assert result.build_id == BuildId(_FIRST_UUID)


def test_failed_build_preserves_generated_build_id(
    tmp_path: Path,
) -> None:
    expected_build_id = BuildId(_FIRST_UUID)

    result = RunPackageBuildUseCase(
        builder=_FailingBuilder(),
        discoverer=DiscoverPackageArtifactsUseCase(),
        validator=ValidatePythonPackageArtifactsUseCase(tmp_path),
        functional_validator=_FunctionalValidator(),
        source_state_provider=_SourceStateProvider(),
        project_root=tmp_path,
        build_id_generator=BuildIdGenerator(lambda: _FIRST_UUID),
        dependency_state_provider=_DependencyStateProvider(),
        toolchain_state_provider=_ToolchainStateProvider(),
    ).execute(Path("dist"))

    assert result.status is PackageBuildStatus.FAILED
    assert result.build_id == expected_build_id
    assert result.diagnostic == "backend failed"
