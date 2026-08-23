"""Tests for the canonical package-build use case."""

from __future__ import annotations

from pathlib import Path

import pytest

import familyos_cli.application.build.toolchain_state_provider as toolchain_provider_module
from familyos_cli.application.build import (
    ArtifactClass,
    ArtifactDiscoveryResult,
    ArtifactDiscoveryStatus,
    CandidatePackageValidationResult,
    DiscoveredArtifact,
    DiscoverPackageArtifactsUseCase,
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
    from familyos_cli.application.build.build_input_validator import (
        BuildInputValidator,
    )

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
        build_input_validator=BuildInputValidator(),
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
    import familyos_cli.application.build.run_package_build as run_module

    builder = _PackageBuilder(
        PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
        )
    )

    monkeypatch.setattr(
        run_module.platform,
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
    import familyos_cli.application.build.run_package_build as run_module

    monkeypatch.setattr(
        run_module.platform,
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
