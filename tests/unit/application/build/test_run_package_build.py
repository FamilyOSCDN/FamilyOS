"""Tests for the canonical package-build use case."""

from __future__ import annotations

import platform
from pathlib import Path

import pytest

import familyos_cli.application.build.toolchain_state_provider as toolchain_provider_module
from familyos_cli.application.build import (
    ArtifactClass,
    ArtifactDiscoveryResult,
    ArtifactDiscoveryStatus,
    BuildContext,
    BuildProfile,
    BuildTarget,
    CandidatePackageValidationResult,
    DiscoveredArtifact,
    DiscoverPackageArtifactsUseCase,
    EffectiveConfigurationValidationFinding,
    EffectiveConfigurationValidationResult,
    EffectiveConfigurationValidationStatus,
    EffectiveConfigurationValidator,
    PackageBuildResult,
    PackageBuildStatus,
    PackageFunctionalValidationStatus,
    PackageStructuralValidationStatus,
    PythonPackageStructuralValidationResult,
    PythonWheelFunctionalValidationResult,
    RunPackageBuildUseCase,
    SourceState,
    ValidatePythonPackageArtifactsUseCase,
    WheelFunctionalValidationFinding,
    WheelFunctionalValidationStage,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_profile_definition import (
    BuildProfileDefinition,
)
from familyos_cli.application.build.build_workspace import BuildWorkspace
from familyos_cli.application.build.build_workspace_initializer import (
    BuildWorkspaceInitializer,
)
from familyos_cli.application.build.repository_layout_validation import (
    RepositoryLayoutValidationResult,
)
from familyos_cli.application.ports.build import (
    PackageBuilderPort,
    PythonWheelFunctionalValidatorPort,
    SourceStateProviderPort,
)

_SOURCE_STATE = SourceState(
    revision="0123456789abcdef0123456789abcdef01234567",
    dirty=False,
)

_TOOLCHAIN_VERSIONS = {
    "build": "1.5.0",
    "pip-tools": "7.6.1",
    "setuptools": "84.0.0",
    "wheel": "0.48.0",
}


def _write_canonical_dependency_inputs(
    project_root: Path,
) -> None:
    from familyos_cli.application.build.dependency_input_freshness import (
        DEPENDENCY_DIGEST_PREFIX,
        dependency_input_digest,
    )

    project_root.mkdir(parents=True, exist_ok=True)
    (project_root / "src").mkdir(exist_ok=True)

    pyproject_path = project_root / "pyproject.toml"
    requirements_path = project_root / "requirements.txt"

    pyproject_path.write_text(
        "[build-system]\n"
        'requires = ["setuptools>=75", "wheel"]\n'
        'build-backend = "setuptools.build_meta"\n'
        "\n"
        "[project]\n"
        'name = "familyos-cli-test"\n'
        'version = "0.0.0"\n'
        'requires-python = ">=3.13"\n'
        'dependencies = ["typer>=0.16"]\n'
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

    digest = dependency_input_digest(pyproject_path)

    requirements_path.write_text(
        f"{DEPENDENCY_DIGEST_PREFIX}{digest}\n"
        "# canonical test lock\n",
        encoding="utf-8",
    )


@pytest.fixture(autouse=True)
def _canonical_build_inputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_canonical_dependency_inputs(tmp_path)
    _write_canonical_dependency_inputs(tmp_path / "project")
    monkeypatch.setattr(
        toolchain_provider_module,
        "distribution_version",
        _TOOLCHAIN_VERSIONS.__getitem__,
    )


class _SourceStateProvider(SourceStateProviderPort):
    def __init__(
        self,
        source_state: SourceState = _SOURCE_STATE,
        events: list[str] | None = None,
    ) -> None:
        self.source_state = source_state
        self.events = events
        self.calls: list[Path] = []

    def observe(self, *, project_root: Path) -> SourceState:
        self.calls.append(project_root)
        if self.events is not None:
            self.events.append("source-state")
        return self.source_state


class _RecordingBuildWorkspaceInitializer(
    BuildWorkspaceInitializer,
):
    def __init__(
        self,
        *,
        error: OSError | None = None,
    ) -> None:
        self.error = error
        self.calls: list[tuple[BuildId, Path]] = []

    def initialize(
        self,
        *,
        build_id: BuildId,
        temporary_directory: Path,
    ) -> BuildWorkspace:
        self.calls.append((build_id, temporary_directory))

        if self.error is not None:
            raise self.error

        root = (
            temporary_directory.resolve()
            / "familyos-build"
            / str(build_id)
        )

        return BuildWorkspace(
            root=root,
            staging_dir=root / "staging",
            intermediate_dir=root / "intermediate",
        )


class _PackageBuilder(PackageBuilderPort):
    def __init__(self, result: PackageBuildResult) -> None:
        self.result = result
        self.calls: list[tuple[Path, Path]] = []

    def build(
        self,
        *,
        project_root: Path,
        output_dir: Path,
    ) -> PackageBuildResult:
        self.calls.append((project_root, output_dir))
        return self.result


class _RecordingValidator(ValidatePythonPackageArtifactsUseCase):
    def __init__(
        self,
        result: PythonPackageStructuralValidationResult | None = None,
    ) -> None:
        self.result = result or PythonPackageStructuralValidationResult(
            status=PackageStructuralValidationStatus.VALID,
            candidate_results=(),
        )
        self.calls: list[tuple[DiscoveredArtifact, ...]] = []

    def execute(
        self,
        candidates: tuple[DiscoveredArtifact, ...],
    ) -> PythonPackageStructuralValidationResult:
        self.calls.append(candidates)
        return self.result


class _RecordingFunctionalValidator(PythonWheelFunctionalValidatorPort):
    def __init__(
        self,
        status: PackageFunctionalValidationStatus = (
            PackageFunctionalValidationStatus.VALID
        ),
        finding: WheelFunctionalValidationFinding | None = None,
    ) -> None:
        self.status = status
        self.finding = finding
        self.calls: list[DiscoveredArtifact] = []
        self.result: PythonWheelFunctionalValidationResult | None = None

    def validate(
        self,
        candidate: DiscoveredArtifact,
    ) -> PythonWheelFunctionalValidationResult:
        self.calls.append(candidate)
        self.result = PythonWheelFunctionalValidationResult(
            candidate=candidate,
            status=self.status,
            findings=(self.finding,) if self.finding is not None else (),
        )
        return self.result


class _RecordingEffectiveConfigurationValidator(
    EffectiveConfigurationValidator,
):
    def __init__(
        self,
        result: EffectiveConfigurationValidationResult | None = None,
        events: list[str] | None = None,
    ) -> None:
        self.result = result or EffectiveConfigurationValidationResult(
            status=EffectiveConfigurationValidationStatus.SUCCEEDED,
        )
        self.events = events
        self.calls: list[
            tuple[
                BuildContext,
                BuildProfileDefinition,
                RepositoryLayoutValidationResult,
                RepositoryLayoutValidationResult,
            ]
        ] = []

    def validate(
        self,
        *,
        context: BuildContext,
        profile_definition: BuildProfileDefinition,
        output_layout_validation: RepositoryLayoutValidationResult,
        evidence_layout_validation: RepositoryLayoutValidationResult,
    ) -> EffectiveConfigurationValidationResult:
        if self.events is not None:
            self.events.append("effective-configuration")
        self.calls.append(
            (
                context,
                profile_definition,
                output_layout_validation,
                evidence_layout_validation,
            )
        )
        return self.result


def test_use_case_delegates_explicit_paths_to_packaging_port(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    output_dir = tmp_path / "packages"
    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    output_dir.mkdir()
    wheel.touch()
    sdist.touch()
    expected = PackageBuildResult(
        status=PackageBuildStatus.SUCCEEDED,
        outputs=(wheel, sdist),
    )
    builder = _PackageBuilder(expected)

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        project_root,
    ).execute(output_dir)

    assert result.execution is expected
    assert result.successful
    assert builder.calls == [(project_root, output_dir)]


def test_use_case_resolves_relative_output_from_project_root(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    output_dir = project_root / "dist"
    output_dir.mkdir(parents=True)
    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    wheel.touch()
    sdist.touch()
    expected = PackageBuildResult(
        status=PackageBuildStatus.SUCCEEDED,
        outputs=(wheel, sdist),
    )
    builder = _PackageBuilder(expected)

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        project_root,
    ).execute(Path("dist"))

    assert builder.calls == [(project_root, project_root / "dist")]
    assert result.discovery is not None
    assert result.discovery.output_dir == output_dir


def test_result_reports_package_outputs_without_trust_metadata(
    tmp_path: Path,
) -> None:
    wheel = tmp_path / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = tmp_path / "familyos_cli-0.1.0.tar.gz"

    result = PackageBuildResult(
        status=PackageBuildStatus.SUCCEEDED,
        outputs=(wheel, sdist),
        exit_code=0,
    )

    assert result.successful
    assert result.outputs == (wheel, sdist)
    assert not hasattr(result, "validated")
    assert not hasattr(result, "trusted")
    assert not hasattr(result, "digest")
    assert not hasattr(result, "build_id")


class _RecordingDiscoverer(DiscoverPackageArtifactsUseCase):
    def __init__(self) -> None:
        self.called = False

    def execute(
        self,
        *,
        output_dir: Path,
        current_outputs: tuple[Path, ...],
    ) -> ArtifactDiscoveryResult:
        self.called = True
        return super().execute(
            output_dir=output_dir,
            current_outputs=current_outputs,
        )


def test_execution_failure_skips_discovery(tmp_path: Path) -> None:
    execution = PackageBuildResult(
        status=PackageBuildStatus.FAILED,
        exit_code=2,
        diagnostic="backend failed",
    )
    builder = _PackageBuilder(execution)
    discoverer = _RecordingDiscoverer()
    validator = _RecordingValidator()
    functional_validator = _RecordingFunctionalValidator()

    result = RunPackageBuildUseCase(
        builder,
        discoverer,
        validator,
        functional_validator,
        _SourceStateProvider(),
        tmp_path,
    ).execute(Path("dist"), validate_functionally=True)

    assert result.status is PackageBuildStatus.FAILED
    assert result.discovery is None
    assert result.diagnostic == "backend failed"
    assert not discoverer.called
    assert validator.calls == []
    assert functional_validator.calls == []


def test_discovery_failure_makes_aggregate_build_fail(tmp_path: Path) -> None:
    execution = PackageBuildResult(status=PackageBuildStatus.SUCCEEDED, outputs=())

    validator = _RecordingValidator()
    functional_validator = _RecordingFunctionalValidator()
    result = RunPackageBuildUseCase(
        _PackageBuilder(execution),
        DiscoverPackageArtifactsUseCase(),
        validator,
        functional_validator,
        _SourceStateProvider(),
        tmp_path,
    ).execute(Path("dist"), validate_functionally=True)

    assert result.status is PackageBuildStatus.FAILED
    assert result.discovery is not None
    assert result.discovery.status is ArtifactDiscoveryStatus.FAILED
    assert result.diagnostic == (
        "Artifact discovery failed: missing python-wheel; missing source-distribution"
    )
    assert result.validation is None
    assert validator.calls == []
    assert functional_validator.calls == []


def test_validation_runs_only_after_successful_discovery(tmp_path: Path) -> None:
    output_dir = tmp_path / "dist"
    output_dir.mkdir()
    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    wheel.touch()
    sdist.touch()
    execution = PackageBuildResult(
        status=PackageBuildStatus.SUCCEEDED,
        outputs=(sdist, wheel),
    )
    validator = _RecordingValidator()
    functional_validator = _RecordingFunctionalValidator()

    result = RunPackageBuildUseCase(
        _PackageBuilder(execution),
        DiscoverPackageArtifactsUseCase(),
        validator,
        functional_validator,
        _SourceStateProvider(),
        tmp_path,
    ).execute(output_dir)

    assert result.successful
    assert result.validation is validator.result
    assert len(validator.calls) == 1
    assert tuple(candidate.path for candidate in validator.calls[0]) == (
        wheel,
        sdist,
    )
    assert result.functional_validation is None
    assert functional_validator.calls == []


def test_validation_failure_makes_aggregate_build_fail(tmp_path: Path) -> None:
    output_dir = tmp_path / "dist"
    output_dir.mkdir()
    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    wheel.touch()
    sdist.touch()
    execution = PackageBuildResult(
        status=PackageBuildStatus.SUCCEEDED,
        outputs=(wheel, sdist),
    )
    invalid = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.INVALID,
        candidate_results=(
            CandidatePackageValidationResult(
                candidate=DiscoveredArtifact(wheel, ArtifactClass.PYTHON_WHEEL),
                status=PackageStructuralValidationStatus.INVALID,
                diagnostics=("wheel is corrupt",),
            ),
        ),
    )
    functional_validator = _RecordingFunctionalValidator()

    result = RunPackageBuildUseCase(
        _PackageBuilder(execution),
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(invalid),
        functional_validator,
        _SourceStateProvider(),
        tmp_path,
    ).execute(output_dir, validate_functionally=True)

    assert result.status is PackageBuildStatus.FAILED
    assert result.discovery is not None
    assert result.discovery.successful
    assert result.validation is invalid
    assert result.diagnostic is not None
    assert "wheel is corrupt" in result.diagnostic
    assert result.functional_validation is None
    assert functional_validator.calls == []


def test_functional_validation_receives_exact_wheel_after_static_validation(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "dist"
    output_dir.mkdir()
    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    wheel.touch()
    sdist.touch()
    execution = PackageBuildResult(
        status=PackageBuildStatus.SUCCEEDED,
        outputs=(sdist, wheel),
    )
    functional_validator = _RecordingFunctionalValidator()

    result = RunPackageBuildUseCase(
        _PackageBuilder(execution),
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        functional_validator,
        _SourceStateProvider(),
        tmp_path,
    ).execute(output_dir, validate_functionally=True)

    assert result.status is PackageBuildStatus.SUCCEEDED
    assert result.functional_validation is functional_validator.result
    assert functional_validator.calls == [
        DiscoveredArtifact(wheel, ArtifactClass.PYTHON_WHEEL)
    ]


def test_functional_validation_failure_makes_aggregate_build_fail(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "dist"
    output_dir.mkdir()
    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    wheel.touch()
    sdist.touch()
    execution = PackageBuildResult(
        status=PackageBuildStatus.SUCCEEDED,
        outputs=(wheel, sdist),
    )
    functional_validator = _RecordingFunctionalValidator(
        status=PackageFunctionalValidationStatus.INVALID,
        finding=WheelFunctionalValidationFinding(
            WheelFunctionalValidationStage.CLI_SMOKE,
            "installed console entry point failed",
        ),
    )

    result = RunPackageBuildUseCase(
        _PackageBuilder(execution),
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        functional_validator,
        _SourceStateProvider(),
        tmp_path,
    ).execute(output_dir, validate_functionally=True)

    assert result.status is PackageBuildStatus.FAILED
    assert result.validation is not None
    assert result.validation.successful
    assert result.functional_validation is functional_validator.result
    assert result.diagnostic is not None
    assert "installed CLI smoke" in result.diagnostic
    assert "installed console entry point failed" in result.diagnostic


def test_source_state_is_observed_before_package_build(tmp_path: Path) -> None:
    events: list[str] = []
    source_state_provider = _SourceStateProvider(events=events)

    class _OrderingBuilder(_PackageBuilder):
        def build(
            self,
            *,
            project_root: Path,
            output_dir: Path,
        ) -> PackageBuildResult:
            events.append("build")
            return super().build(
                project_root=project_root,
                output_dir=output_dir,
            )

    execution = PackageBuildResult(
        status=PackageBuildStatus.FAILED,
        exit_code=2,
        diagnostic="backend failed",
    )

    result = RunPackageBuildUseCase(
        _OrderingBuilder(execution),
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        source_state_provider,
        tmp_path,
    ).execute(Path("dist"))

    assert events == ["source-state", "build"]
    assert source_state_provider.calls == [tmp_path]
    assert result.source_state is _SOURCE_STATE


def test_execution_failure_preserves_pre_build_source_state(
    tmp_path: Path,
) -> None:
    source_state = SourceState(
        revision="fedcba9876543210fedcba9876543210fedcba98",
        dirty=True,
    )
    source_state_provider = _SourceStateProvider(source_state)

    execution = PackageBuildResult(
        status=PackageBuildStatus.ERROR,
        diagnostic="builder unavailable",
    )

    result = RunPackageBuildUseCase(
        _PackageBuilder(execution),
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        source_state_provider,
        tmp_path,
    ).execute(Path("dist"), validate_functionally=True)

    assert source_state_provider.calls == [tmp_path]
    assert result.status is PackageBuildStatus.ERROR
    assert result.source_state is source_state
    assert result.discovery is None
    assert result.validation is None
    assert result.functional_validation is None


def test_canonical_build_preserves_resolved_build_context(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.build_context import (
        BuildProfile,
        BuildTarget,
    )

    output_dir = tmp_path / "dist"
    output_dir.mkdir()

    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    wheel.touch()
    sdist.touch()

    execution = PackageBuildResult(
        status=PackageBuildStatus.SUCCEEDED,
        outputs=(wheel, sdist),
    )

    result = RunPackageBuildUseCase(
        _PackageBuilder(execution),
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
    ).execute(
        Path("dist"),
        profile=BuildProfile.VALIDATION,
        target=BuildTarget.FAMILYOS_CLI_PACKAGE,
    )

    assert result.build_context is not None
    assert result.build_context.source_state is result.source_state
    assert tuple(
        (component.distribution, component.version)
        for component in result.build_context.toolchain_state.critical_versions
    ) == tuple(_TOOLCHAIN_VERSIONS.items())
    assert result.build_context.profile is BuildProfile.VALIDATION
    assert (
        result.build_context.target
        is BuildTarget.FAMILYOS_CLI_PACKAGE
    )
    assert result.build_context.output_dir == output_dir
    assert (
        result.build_context.effective_configuration.functional_validation
        is False
    )


def test_build_context_is_resolved_before_package_execution(
    tmp_path: Path,
) -> None:
    events: list[str] = []

    class _OrderedBuilder(PackageBuilderPort):
        def build(
            self,
            *,
            project_root: Path,
            output_dir: Path,
        ) -> PackageBuildResult:
            events.append("build")
            return PackageBuildResult(
                status=PackageBuildStatus.FAILED,
                diagnostic="expected test failure",
            )

    provider = _SourceStateProvider(events=events)

    result = RunPackageBuildUseCase(
        _OrderedBuilder(),
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        provider,
        tmp_path,
    ).execute(Path("dist"))

    assert events == ["source-state", "build"]
    assert result.build_context is not None
    assert result.build_context.source_state is _SOURCE_STATE


def test_failed_execution_preserves_resolved_build_context(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.build_context import BuildProfile

    execution = PackageBuildResult(
        status=PackageBuildStatus.FAILED,
        exit_code=2,
        diagnostic="backend failed",
    )

    result = RunPackageBuildUseCase(
        _PackageBuilder(execution),
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
    ).execute(
        Path("dist"),
        validate_functionally=True,
        profile=BuildProfile.CI,
        evidence_output=tmp_path / "build-evidence.json",
    )

    assert not result.successful
    assert result.build_context is not None
    assert result.build_context.profile is BuildProfile.CI
    assert (
        result.build_context.effective_configuration.functional_validation
        is True
    )
    assert result.build_context.output_dir == tmp_path / "dist"


def test_dependency_state_is_captured_before_package_execution(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.dependency_state import DependencyState
    from familyos_cli.application.build.dependency_state_provider import (
        DependencyStateProvider,
    )

    events: list[str] = []

    class _OrderedDependencyStateProvider(DependencyStateProvider):
        def capture(self, *, project_root: Path) -> DependencyState:
            events.append("dependency-state")
            return DependencyState(
                declaration_path=project_root / "pyproject.toml",
                declaration_digest="a" * 64,
                lock_path=project_root / "requirements.txt",
                lock_digest="b" * 64,
            )

    class _OrderedBuilder(PackageBuilderPort):
        def build(
            self,
            *,
            project_root: Path,
            output_dir: Path,
        ) -> PackageBuildResult:
            events.append("build")
            return PackageBuildResult(
                status=PackageBuildStatus.FAILED,
                diagnostic="expected test failure",
            )

    source_provider = _SourceStateProvider(events=events)

    result = RunPackageBuildUseCase(
        _OrderedBuilder(),
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        source_provider,
        tmp_path,
        dependency_state_provider=_OrderedDependencyStateProvider(),
    ).execute(Path("dist"))

    assert events == [
        "source-state",
        "dependency-state",
        "build",
    ]

    assert result.build_context is not None
    assert (
        result.build_context.dependency_state.declaration_digest
        == "a" * 64
    )
    assert (
        result.build_context.dependency_state.lock_digest
        == "b" * 64
    )


def test_toolchain_state_is_captured_before_package_execution(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.toolchain_state import (
        ToolchainState,
        ToolchainVersion,
    )
    from familyos_cli.application.build.toolchain_state_provider import (
        ToolchainStateProvider,
    )

    events: list[str] = []

    class _OrderedToolchainStateProvider(ToolchainStateProvider):
        def capture(self) -> ToolchainState:
            events.append("toolchain-state")
            return ToolchainState(
                critical_versions=tuple(
                    ToolchainVersion(distribution, version)
                    for distribution, version in _TOOLCHAIN_VERSIONS.items()
                ),
            )

    class _OrderedBuilder(PackageBuilderPort):
        def build(
            self,
            *,
            project_root: Path,
            output_dir: Path,
        ) -> PackageBuildResult:
            events.append("build")
            return PackageBuildResult(
                status=PackageBuildStatus.FAILED,
                diagnostic="expected test failure",
            )

    source_provider = _SourceStateProvider(events=events)

    result = RunPackageBuildUseCase(
        _OrderedBuilder(),
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        source_provider,
        tmp_path,
        toolchain_state_provider=_OrderedToolchainStateProvider(),
    ).execute(Path("dist"))

    assert events == [
        "toolchain-state",
        "source-state",
        "build",
    ]
    assert result.build_context is not None
    assert tuple(
        component.distribution
        for component in result.build_context.toolchain_state.critical_versions
    ) == tuple(_TOOLCHAIN_VERSIONS)

def test_use_case_validates_build_inputs_before_execution(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.build_input_validator import (
        BuildInputValidator,
    )

    events: list[str] = []

    (tmp_path / "src").mkdir(exist_ok=True)

    class RecordingBuilder(_PackageBuilder):
        def build(
            self,
            *,
            project_root: Path,
            output_dir: Path,
        ) -> PackageBuildResult:
            events.append("package-build")
            return super().build(
                project_root=project_root,
                output_dir=output_dir,
            )

    output_dir = tmp_path / "packages"
    output_dir.mkdir()

    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    wheel.touch()
    sdist.touch()

    builder = RecordingBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
            outputs=(wheel, sdist),
        )
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(events=events),
        tmp_path,
        build_input_validator=BuildInputValidator(),
    ).execute(output_dir)

    assert result.successful is True
    assert events == ["source-state", "package-build"]
    assert builder.calls == [(tmp_path, output_dir)]
    assert result.build_context is not None
    assert result.build_context.build_id == result.build_id


def test_missing_build_input_prevents_package_execution(
    tmp_path: Path,
) -> None:
    (tmp_path / "pyproject.toml").unlink()
    (tmp_path / "src").mkdir(exist_ok=True)

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
        )
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
    ).execute(tmp_path / "packages")

    assert result.successful is False
    assert result.status is PackageBuildStatus.FAILED
    assert builder.calls == []

    assert result.build_context is None
    assert result.build_id is not None
    assert result.source_state is _SOURCE_STATE

    assert result.discovery is None
    assert result.validation is None
    assert result.functional_validation is None

    assert result.diagnostic == (
        "required build input missing: pyproject.toml"
    )


def test_stale_generated_dependency_input_prevents_package_execution(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.build_input_validator import (
        BuildInputValidator,
    )
    from familyos_cli.application.build.dependency_input_freshness import (
        DEPENDENCY_DIGEST_PREFIX,
    )

    # The autouse fixture provides the canonical metadata and dependency
    # inputs. Add the required package source so freshness is the only
    # intentionally invalid canonical input.
    (tmp_path / "src").mkdir(exist_ok=True)

    requirements_path = tmp_path / "requirements.txt"
    requirements_path.write_text(
        f"{DEPENDENCY_DIGEST_PREFIX}{'0' * 64}\n"
        "# stale canonical test lock\n",
        encoding="utf-8",
    )

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
        )
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
        build_input_validator=BuildInputValidator(),
    ).execute(tmp_path / "packages")

    assert result.successful is False
    assert result.status is PackageBuildStatus.FAILED
    assert builder.calls == []

    assert result.build_context is None
    assert result.discovery is None
    assert result.validation is None
    assert result.functional_validation is None

    assert result.diagnostic == (
        "generated dependency input requirements.txt is stale; "
        "regenerate requirements.txt"
    )


@pytest.mark.parametrize(
    ("output_dir", "diagnostic"),
    (
        (
            Path("."),
            "build output directory must not be the repository root",
        ),
        (
            Path("src"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path("src/generated"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path("src/familyos_cli/dist"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path("tests"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path("tests/build-output"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path("docs"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path("docs/generated"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path("scripts"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path("scripts/output"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path(".github"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path(".github/artifacts"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path("specifications"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path("specifications/generated"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path("templates"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path("templates/packages"),
            (
                "build output directory must not overlap "
                "authoritative repository content"
            ),
        ),
        (
            Path("pyproject.toml"),
            (
                "build output directory must not replace "
                "authoritative repository files"
            ),
        ),
        (
            Path("requirements.txt"),
            (
                "build output directory must not replace "
                "authoritative repository files"
            ),
        ),
    ),
)
def test_unsafe_repository_output_prevents_package_execution(
    tmp_path: Path,
    output_dir: Path,
    diagnostic: str,
) -> None:
    from familyos_cli.application.build.build_input_validator import (
        BuildInputValidator,
    )

    (tmp_path / "src").mkdir(exist_ok=True)
    (tmp_path / "tests").mkdir(exist_ok=True)

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
        )
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
        build_input_validator=BuildInputValidator(),
    ).execute(output_dir)

    assert result.successful is False
    assert result.status is PackageBuildStatus.FAILED
    assert builder.calls == []

    assert result.build_context is None
    assert result.discovery is None
    assert result.validation is None
    assert result.functional_validation is None

    assert result.diagnostic == diagnostic


def test_canonical_dist_output_passes_repository_layout_gate(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.build_input_validator import (
        BuildInputValidator,
    )

    (tmp_path / "src").mkdir(exist_ok=True)

    output_dir = tmp_path / "dist"
    output_dir.mkdir()

    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    wheel.touch()
    sdist.touch()

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
            outputs=(wheel, sdist),
        )
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
        build_input_validator=BuildInputValidator(),
    ).execute(Path("dist"))

    assert result.successful is True
    assert builder.calls == [
        (
            tmp_path,
            output_dir,
        )
    ]

    assert result.build_context is not None
    assert result.build_context.output_dir == output_dir


def test_unsupported_runtime_prevents_package_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
        )
    )

    monkeypatch.setattr(
        platform,
        "python_version",
        lambda: "3.14.0",
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
    ).execute(Path("dist"))

    assert result.successful is False
    assert result.status is PackageBuildStatus.FAILED
    assert builder.calls == []
    assert result.build_context is None
    assert result.diagnostic == (
        "python 3.14.0 does not satisfy <3.14,>=3.13"
    )


def test_unsupported_build_tool_version_prevents_package_execution(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.toolchain_state import (
        ToolchainState,
        ToolchainVersion,
    )
    from familyos_cli.application.build.toolchain_state_provider import (
        ToolchainStateProvider,
    )

    class UnsupportedBuildToolchainProvider(ToolchainStateProvider):
        def capture(self) -> ToolchainState:
            return ToolchainState(
                critical_versions=(
                    ToolchainVersion("build", "1.4.9"),
                    ToolchainVersion("pip-tools", "7.6.1"),
                    ToolchainVersion("setuptools", "84.0.0"),
                    ToolchainVersion("wheel", "0.48.0"),
                ),
            )

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
        )
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
        toolchain_state_provider=UnsupportedBuildToolchainProvider(),
    ).execute(Path("dist"))

    assert result.successful is False
    assert result.status is PackageBuildStatus.FAILED
    assert builder.calls == []
    assert result.build_context is None
    assert result.diagnostic == (
        "build 1.4.9 does not satisfy >=1.5"
    )


def test_invalid_toolchain_policy_prevents_package_execution(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.dependency_input_freshness import (
        DEPENDENCY_DIGEST_PREFIX,
        dependency_input_digest,
    )

    (tmp_path / "pyproject.toml").write_text(
        "[build-system]\n"
        'requires = ["setuptools>=75", "wheel"]\n'
        'build-backend = "setuptools.build_meta"\n'
        "\n"
        "[project]\n"
        'name = "familyos-cli-test"\n'
        'version = "0.0.0"\n'
        'requires-python = ">=3.13"\n'
        'dependencies = ["typer>=0.16"]\n'
        "\n"
        "[project.optional-dependencies]\n"
        'dev = ["pip-tools==7.6.1"]\n'
        "\n"
        "[tool.mypy]\n"
        'python_version = "3.13"\n',
        encoding="utf-8",
    )
    digest = dependency_input_digest(tmp_path / "pyproject.toml")
    (tmp_path / "requirements.txt").write_text(
        f"{DEPENDENCY_DIGEST_PREFIX}{digest}\n"
        "# canonical test lock\n",
        encoding="utf-8",
    )

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
        )
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
    ).execute(Path("dist"))

    assert result.successful is False
    assert result.status is PackageBuildStatus.FAILED
    assert builder.calls == []
    assert result.build_context is None
    assert result.diagnostic == (
        "required canonical toolchain declaration 'build' is missing"
    )


def test_compatible_toolchain_is_captured_once_and_reused_in_context(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.toolchain_state import (
        ToolchainState,
        ToolchainVersion,
    )
    from familyos_cli.application.build.toolchain_state_provider import (
        ToolchainStateProvider,
    )

    observed_state = ToolchainState(
        critical_versions=tuple(
            ToolchainVersion(distribution, version)
            for distribution, version in _TOOLCHAIN_VERSIONS.items()
        ),
    )

    class RecordingToolchainProvider(ToolchainStateProvider):
        def __init__(self) -> None:
            self.calls = 0

        def capture(self) -> ToolchainState:
            self.calls += 1
            return observed_state

    provider = RecordingToolchainProvider()

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            diagnostic="expected test failure",
        )
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
        toolchain_state_provider=provider,
    ).execute(Path("dist"))

    assert provider.calls == 1
    assert result.build_context is not None
    assert result.build_context.toolchain_state is observed_state
    assert builder.calls == [
        (
            tmp_path,
            tmp_path / "dist",
        )
    ]


def test_validated_runtime_is_reused_in_build_context(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        platform,
        "python_version",
        lambda: "3.13.42",
    )

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            diagnostic="expected test failure",
        )
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
    ).execute(Path("dist"))

    assert result.build_context is not None
    assert result.build_context.runtime_version == "3.13.42"


def test_invalid_environment_fails_before_package_execution(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.environment_state import (
        EnvironmentState,
    )
    from familyos_cli.application.build.environment_state_provider import (
        EnvironmentStateProvider,
    )

    unavailable = tmp_path / "missing-environment-temp"

    class _InvalidEnvironmentStateProvider(EnvironmentStateProvider):
        def capture(self) -> EnvironmentState:
            return EnvironmentState(
                operating_system="TestOS",
                operating_system_release="1.0",
                machine_architecture="test-machine",
                virtual_environment_active=True,
                temporary_directory=str(unavailable),
                filesystem_encoding="utf-8",
            )

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            diagnostic="builder must not execute",
        )
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
        environment_state_provider=_InvalidEnvironmentStateProvider(),
    ).execute(Path("dist"))

    assert result.status is PackageBuildStatus.FAILED
    assert result.successful is False
    assert result.execution.diagnostic == (
        f"temporary directory is unavailable: {unavailable}"
    )
    assert result.build_context is None
    assert builder.calls == []


def test_environment_state_is_captured_once_and_reused_in_build_context(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.environment_state import (
        EnvironmentState,
    )
    from familyos_cli.application.build.environment_state_provider import (
        EnvironmentStateProvider,
    )

    observed_state = EnvironmentState(
        operating_system="TestOS",
        operating_system_release="1.0",
        machine_architecture="test-machine",
        virtual_environment_active=True,
        temporary_directory=str(tmp_path),
        filesystem_encoding="utf-8",
    )

    class _RecordingEnvironmentStateProvider(EnvironmentStateProvider):
        def __init__(self) -> None:
            self.calls = 0

        def capture(self) -> EnvironmentState:
            self.calls += 1
            return observed_state

    provider = _RecordingEnvironmentStateProvider()

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            diagnostic="expected test failure",
        )
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
        environment_state_provider=provider,
    ).execute(Path("dist"))

    assert provider.calls == 1
    assert result.build_context is not None
    assert result.build_context.environment_state is observed_state
    assert builder.calls == [
        (
            tmp_path,
            tmp_path / "dist",
        )
    ]


def test_effective_configuration_validation_precedes_package_execution(
    tmp_path: Path,
) -> None:
    events: list[str] = []

    class _OrderedBuilder(_PackageBuilder):
        def build(
            self,
            *,
            project_root: Path,
            output_dir: Path,
        ) -> PackageBuildResult:
            events.append("build")
            return super().build(
                project_root=project_root,
                output_dir=output_dir,
            )

    builder = _OrderedBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            diagnostic="expected test failure",
        )
    )
    source_state_provider = _SourceStateProvider(events=events)
    effective_validator = _RecordingEffectiveConfigurationValidator(
        events=events,
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        source_state_provider,
        tmp_path,
        effective_configuration_validator=effective_validator,
    ).execute(Path("dist"))

    assert events == [
        "source-state",
        "effective-configuration",
        "build",
    ]
    assert len(effective_validator.calls) == 1
    (
        validated_context,
        profile_definition,
        layout_validation,
        evidence_layout_validation,
    ) = (
        effective_validator.calls[0]
    )
    assert result.build_context is validated_context
    assert profile_definition.profile is BuildProfile.DEVELOPMENT
    assert validated_context.target in profile_definition.supported_targets
    assert layout_validation.successful is True
    assert evidence_layout_validation.successful is True
    assert source_state_provider.calls == [tmp_path]
    assert builder.calls == [(tmp_path, validated_context.output_dir)]


def test_invalid_effective_configuration_prevents_package_execution(
    tmp_path: Path,
) -> None:
    failure = EffectiveConfigurationValidationResult(
        status=EffectiveConfigurationValidationStatus.FAILED,
        findings=(
            EffectiveConfigurationValidationFinding(
                component="profile",
                diagnostic="resolved effective configuration is inconsistent",
            ),
        ),
    )
    effective_validator = _RecordingEffectiveConfigurationValidator(
        result=failure,
    )
    builder = _PackageBuilder(
        PackageBuildResult(status=PackageBuildStatus.SUCCEEDED)
    )
    source_state_provider = _SourceStateProvider()

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        source_state_provider,
        tmp_path,
        effective_configuration_validator=effective_validator,
    ).execute(Path("dist"))

    assert result.status is PackageBuildStatus.FAILED
    assert result.diagnostic == (
        "resolved effective configuration is inconsistent"
    )
    assert builder.calls == []
    assert len(effective_validator.calls) == 1
    assert result.build_context is effective_validator.calls[0][0]
    assert result.source_state is result.build_context.source_state
    assert result.build_id == result.build_context.build_id
    assert result.discovery is None
    assert result.validation is None
    assert result.functional_validation is None
    assert source_state_provider.calls == [tmp_path]


def test_equivalent_default_and_explicit_inputs_resolve_equivalently(
    tmp_path: Path,
) -> None:
    effective_validator = _RecordingEffectiveConfigurationValidator()
    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            diagnostic="expected test failure",
        )
    )
    use_case = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
        effective_configuration_validator=effective_validator,
    )

    default_result = use_case.execute(Path("dist"))
    explicit_result = use_case.execute(
        tmp_path / "dist",
        validate_functionally=False,
        profile=BuildProfile.DEVELOPMENT,
        target=BuildTarget.FAMILYOS_CLI_PACKAGE,
    )

    assert len(effective_validator.calls) == 2
    default_context = effective_validator.calls[0][0]
    explicit_context = effective_validator.calls[1][0]
    assert default_result.build_context is default_context
    assert explicit_result.build_context is explicit_context
    assert default_context.profile is explicit_context.profile
    assert default_context.target is explicit_context.target
    assert default_context.output_dir == explicit_context.output_dir
    assert (
        default_context.effective_configuration
        == explicit_context.effective_configuration
    )


@pytest.mark.parametrize(
    "profile",
    (BuildProfile.CI, BuildProfile.RELEASE_CANDIDATE),
)
def test_required_evidence_profile_cannot_bypass_evidence_destination(
    tmp_path: Path,
    profile: BuildProfile,
) -> None:
    builder = _PackageBuilder(
        PackageBuildResult(status=PackageBuildStatus.SUCCEEDED)
    )
    discoverer = _RecordingDiscoverer()

    result = RunPackageBuildUseCase(
        builder,
        discoverer,
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
    ).execute(
        Path("dist"),
        profile=profile,
    )

    assert result.status is PackageBuildStatus.FAILED
    assert result.diagnostic == (
        f"build profile requires an evidence output: {profile.value}"
    )
    assert result.build_context is not None
    assert result.build_context.profile is profile
    assert result.build_context.evidence_output is None
    assert result.source_state is result.build_context.source_state
    assert result.build_id == result.build_context.build_id
    assert builder.calls == []
    assert discoverer.called is False
    assert result.discovery is None
    assert result.validation is None
    assert result.artifact_manifest is None
    assert result.artifact_integrities == ()


@pytest.mark.parametrize(
    "profile",
    (BuildProfile.CI, BuildProfile.RELEASE_CANDIDATE),
)
def test_required_evidence_profile_accepts_explicit_destination(
    tmp_path: Path,
    profile: BuildProfile,
) -> None:
    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            diagnostic="expected test failure",
        )
    )
    evidence_output = tmp_path / "build-evidence.json"

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
    ).execute(
        Path("dist"),
        profile=profile,
        evidence_output=evidence_output,
    )

    assert result.diagnostic == "expected test failure"
    assert result.build_context is not None
    assert result.build_context.evidence_output == evidence_output
    assert builder.calls == [(tmp_path, tmp_path / "dist")]


@pytest.mark.parametrize(
    ("evidence_output", "diagnostic"),
    (
        (
            Path("pyproject.toml"),
            "build evidence output must not replace "
            "authoritative repository files",
        ),
        (
            Path("requirements.txt"),
            "build evidence output must not replace "
            "authoritative repository files",
        ),
        (
            Path("src/build-evidence.json"),
            "build evidence output must not overlap "
            "authoritative repository content",
        ),
        (
            Path("dist/build-evidence.json"),
            "build evidence output must not overlap package output directory",
        ),
    ),
)
def test_evidence_output_conflict_prevents_package_execution(
    tmp_path: Path,
    evidence_output: Path,
    diagnostic: str,
) -> None:
    builder = _PackageBuilder(
        PackageBuildResult(status=PackageBuildStatus.SUCCEEDED)
    )
    discoverer = _RecordingDiscoverer()

    result = RunPackageBuildUseCase(
        builder,
        discoverer,
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
    ).execute(
        Path("dist"),
        evidence_output=evidence_output,
    )

    assert result.status is PackageBuildStatus.FAILED
    assert result.diagnostic == diagnostic
    assert result.build_context is not None
    assert result.build_context.evidence_output == tmp_path / evidence_output
    assert builder.calls == []
    assert discoverer.called is False
    assert result.discovery is None
    assert result.validation is None
    assert result.artifact_manifest is None


def test_optional_functional_validation_remains_explicit_and_optional(
    tmp_path: Path,
) -> None:
    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            diagnostic="expected test failure",
        )
    )
    use_case = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
    )

    optional_result = use_case.execute(Path("dist"))
    requested_result = use_case.execute(
        Path("dist"),
        validate_functionally=True,
    )

    assert optional_result.build_context is not None
    assert requested_result.build_context is not None
    assert (
        optional_result.build_context.effective_configuration.functional_validation
        is False
    )
    assert (
        requested_result.build_context.effective_configuration.functional_validation
        is True
    )
    assert builder.calls == [
        (tmp_path, tmp_path / "dist"),
        (tmp_path, tmp_path / "dist"),
    ]


def test_package_execution_observation_records_success_duration(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.build_execution_observation import (
        BuildExecutionStage,
        BuildExecutionStageStatus,
    )

    output_dir = tmp_path / "dist"
    output_dir.mkdir()

    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    wheel.touch()
    sdist.touch()

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
            outputs=(wheel, sdist),
        )
    )

    clock_values = iter(
        (
            10.0,
            10.01,
            20.0,
            20.02,
            30.0,
            30.03,
            40.0,
            40.04,
            50.0,
            50.05,
            60.0,
            60.06,
            70.0,
            70.07,
            80.0,
            80.08,
            90.0,
            90.09,
            100.0,
            100.10,
            110.0,
            110.11,
            120.0,
            120.12,
            130.0,
            130.13,
        )
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
        monotonic_clock=lambda: next(clock_values),
    ).execute(output_dir)

    assert result.successful is True

    expected_stages = (
        BuildExecutionStage.VALIDATE_INPUTS,
        BuildExecutionStage.VALIDATE_REPOSITORY_LAYOUT,
        BuildExecutionStage.VALIDATE_TOOLCHAIN,
        BuildExecutionStage.VALIDATE_ENVIRONMENT,
        BuildExecutionStage.INITIALIZE_WORKSPACE,
        BuildExecutionStage.RESOLVE_BUILD_CONTEXT,
        BuildExecutionStage.VALIDATE_EFFECTIVE_CONFIGURATION,
        BuildExecutionStage.PACKAGE,
        BuildExecutionStage.DISCOVER_ARTIFACTS,
        BuildExecutionStage.VALIDATE_ARTIFACTS,
        BuildExecutionStage.ESTABLISH_ARTIFACT_IDENTITY,
        BuildExecutionStage.ESTABLISH_ARTIFACT_INTEGRITY,
        BuildExecutionStage.BUILD_ARTIFACT_MANIFEST,
    )

    assert tuple(
        observation.stage
        for observation in result.execution_observations
    ) == expected_stages

    assert len(result.execution_observations) == 13

    for observation in result.execution_observations:
        assert observation.status is BuildExecutionStageStatus.SUCCEEDED
        assert observation.duration_seconds > 0
        assert observation.diagnostic is None

    assert (
        BuildExecutionStage.FUNCTIONALLY_VALIDATE_WHEEL
        not in expected_stages
    )


def test_package_execution_observation_records_failure_duration_and_diagnostic(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.build_execution_observation import (
        BuildExecutionStage,
        BuildExecutionStageStatus,
    )

    output_dir = tmp_path / "dist"
    output_dir.mkdir()

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            exit_code=1,
            diagnostic="package frontend failed",
        )
    )

    clock_values = iter(
        (
            10.0,
            10.01,
            20.0,
            20.02,
            30.0,
            30.03,
            40.0,
            40.04,
            50.0,
            50.05,
            60.0,
            60.06,
            70.0,
            70.07,
            80.0,
            80.50,
        )
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
        monotonic_clock=lambda: next(clock_values),
    ).execute(output_dir)

    assert result.successful is False

    assert tuple(
        observation.stage
        for observation in result.execution_observations
    ) == (
        BuildExecutionStage.VALIDATE_INPUTS,
        BuildExecutionStage.VALIDATE_REPOSITORY_LAYOUT,
        BuildExecutionStage.VALIDATE_TOOLCHAIN,
        BuildExecutionStage.VALIDATE_ENVIRONMENT,
        BuildExecutionStage.INITIALIZE_WORKSPACE,
        BuildExecutionStage.RESOLVE_BUILD_CONTEXT,
        BuildExecutionStage.VALIDATE_EFFECTIVE_CONFIGURATION,
        BuildExecutionStage.PACKAGE,
    )

    *successful_observations, package = result.execution_observations

    assert all(
        observation.status is BuildExecutionStageStatus.SUCCEEDED
        for observation in successful_observations
    )

    assert package.stage is BuildExecutionStage.PACKAGE
    assert package.status is BuildExecutionStageStatus.FAILED
    assert package.duration_seconds == pytest.approx(0.50)
    assert package.diagnostic == "package frontend failed"

    assert BuildExecutionStage.DISCOVER_ARTIFACTS not in tuple(
        observation.stage
        for observation in result.execution_observations
    )


def test_functional_validation_execution_observation_is_recorded_last(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.build_execution_observation import (
        BuildExecutionStage,
        BuildExecutionStageStatus,
    )

    output_dir = tmp_path / "dist"
    output_dir.mkdir()

    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    wheel.touch()
    sdist.touch()

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
            outputs=(wheel, sdist),
        )
    )

    clock_values = iter(
        (
            10.0,
            10.01,
            20.0,
            20.02,
            30.0,
            30.03,
            40.0,
            40.04,
            50.0,
            50.05,
            60.0,
            60.06,
            70.0,
            70.07,
            80.0,
            80.08,
            90.0,
            90.09,
            100.0,
            100.10,
            110.0,
            110.11,
            120.0,
            120.12,
            130.0,
            130.13,
            140.0,
            140.14,
        )
    )

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
        monotonic_clock=lambda: next(clock_values),
    ).execute(
        output_dir,
        validate_functionally=True,
    )

    assert result.successful is True
    assert len(result.execution_observations) == 14

    final_observation = result.execution_observations[-1]

    assert (
        final_observation.stage
        is BuildExecutionStage.FUNCTIONALLY_VALIDATE_WHEEL
    )
    assert (
        final_observation.status
        is BuildExecutionStageStatus.SUCCEEDED
    )
    assert final_observation.duration_seconds == pytest.approx(0.14)
    assert final_observation.diagnostic is None


def test_workspace_initialization_receives_build_id_and_environment_temp_dir(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.environment_state import EnvironmentState
    from familyos_cli.application.build.environment_state_provider import (
        EnvironmentStateProvider,
    )

    class _EnvironmentStateProvider(EnvironmentStateProvider):
        def capture(self) -> EnvironmentState:
            return EnvironmentState(
                operating_system="test-os",
                operating_system_release="1",
                machine_architecture="test-machine",
                virtual_environment_active=True,
                temporary_directory=str(tmp_path / "canonical-temp"),
            )

    canonical_temp = tmp_path / "canonical-temp"
    canonical_temp.mkdir()

    output_dir = tmp_path / "dist"
    output_dir.mkdir()

    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    wheel.touch()
    sdist.touch()

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
            outputs=(wheel, sdist),
        )
    )
    workspace_initializer = _RecordingBuildWorkspaceInitializer()

    result = RunPackageBuildUseCase(
        builder,
        DiscoverPackageArtifactsUseCase(),
        _RecordingValidator(),
        _RecordingFunctionalValidator(),
        _SourceStateProvider(),
        tmp_path,
        environment_state_provider=_EnvironmentStateProvider(),
        build_workspace_initializer=workspace_initializer,
    ).execute(output_dir)

    assert result.successful is True
    assert len(workspace_initializer.calls) == 1

    observed_build_id, observed_temporary_directory = (
        workspace_initializer.calls[0]
    )

    assert observed_build_id == result.build_id
    assert observed_temporary_directory == canonical_temp


def test_workspace_initialization_failure_is_fail_fast_before_packaging(
    tmp_path: Path,
) -> None:
    from familyos_cli.application.build.build_execution_observation import (
        BuildExecutionStage,
        BuildExecutionStageStatus,
    )

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
        )
    )
    discoverer = _RecordingDiscoverer()
    validator = _RecordingValidator()
    functional_validator = _RecordingFunctionalValidator()
    workspace_initializer = _RecordingBuildWorkspaceInitializer(
        error=OSError("workspace initialization failed"),
    )

    result = RunPackageBuildUseCase(
        builder,
        discoverer,
        validator,
        functional_validator,
        _SourceStateProvider(),
        tmp_path,
        build_workspace_initializer=workspace_initializer,
    ).execute(tmp_path / "dist")

    assert result.successful is False
    assert result.execution.diagnostic == "workspace initialization failed"

    assert len(workspace_initializer.calls) == 1
    assert builder.calls == []
    assert discoverer.called is False
    assert validator.calls == []
    assert functional_validator.calls == []

    final_observation = result.execution_observations[-1]

    assert final_observation.stage is BuildExecutionStage.INITIALIZE_WORKSPACE
    assert final_observation.status is BuildExecutionStageStatus.FAILED
    assert final_observation.diagnostic == "workspace initialization failed"

    reached_stages = tuple(
        observation.stage
        for observation in result.execution_observations
    )

    assert BuildExecutionStage.RESOLVE_BUILD_CONTEXT not in reached_stages
    assert BuildExecutionStage.VALIDATE_EFFECTIVE_CONFIGURATION not in reached_stages
    assert BuildExecutionStage.PACKAGE not in reached_stages
