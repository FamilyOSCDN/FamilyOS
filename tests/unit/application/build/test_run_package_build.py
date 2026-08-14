"""Tests for the canonical package-build use case."""

from __future__ import annotations

from pathlib import Path

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
    ValidatePythonPackageArtifactsUseCase,
    WheelFunctionalValidationFinding,
    WheelFunctionalValidationStage,
)
from familyos_cli.application.ports.build import (
    PackageBuilderPort,
    PythonWheelFunctionalValidatorPort,
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
        tmp_path,
    ).execute(output_dir, validate_functionally=True)

    assert result.status is PackageBuildStatus.FAILED
    assert result.validation is not None
    assert result.validation.successful
    assert result.functional_validation is functional_validator.result
    assert result.diagnostic is not None
    assert "installed CLI smoke" in result.diagnostic
    assert "installed console entry point failed" in result.diagnostic
