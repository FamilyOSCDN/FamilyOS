"""End-to-end tests for the canonical package-build CLI surface."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest
from typer.testing import CliRunner

from familyos_cli.application.build import (
    ArtifactClass,
    ArtifactDiscoveryResult,
    ArtifactDiscoveryStatus,
    CandidatePackageValidationResult,
    CanonicalPackageBuildResult,
    DiscoveredArtifact,
    PackageBuildResult,
    PackageBuildStatus,
    PackageFunctionalValidationStatus,
    PackageStructuralValidationStatus,
    PythonPackageStructuralValidationResult,
    PythonWheelFunctionalValidationResult,
    SourceState,
    WheelFunctionalValidationFinding,
    WheelFunctionalValidationStage,
)
from familyos_cli.application.build.build_context import BuildProfile
from familyos_cli.interfaces.cli.app import app
from familyos_cli.interfaces.cli.commands import build as build_command

runner = CliRunner()


_SOURCE_STATE = SourceState(
    revision="0123456789abcdef0123456789abcdef01234567",
    dirty=False,
)


class _UseCase:
    def __init__(self, result: CanonicalPackageBuildResult) -> None:
        self.result = result
        self.output_dirs: list[Path] = []
        self.functional_validation_requests: list[bool] = []
        self.profile_requests: list[BuildProfile] = []
        self.evidence_output_requests: list[Path | None] = []

    def execute(
        self,
        output_dir: Path,
        *,
        validate_functionally: bool = False,
        profile: BuildProfile = BuildProfile.DEVELOPMENT,
        evidence_output: Path | None = None,
    ) -> CanonicalPackageBuildResult:
        self.output_dirs.append(output_dir)
        self.functional_validation_requests.append(validate_functionally)
        self.profile_requests.append(profile)
        self.evidence_output_requests.append(evidence_output)
        return self.result


class _Context:
    def __init__(self, use_case: _UseCase) -> None:
        self.run_package_build = use_case


def _install_context(
    monkeypatch: pytest.MonkeyPatch,
    result: CanonicalPackageBuildResult,
) -> _UseCase:
    use_case = _UseCase(result)
    monkeypatch.setattr(build_command, "CommandContext", lambda: _Context(use_case))
    return use_case


def _execution(
    status: PackageBuildStatus = PackageBuildStatus.SUCCEEDED,
    *,
    diagnostic: str | None = None,
) -> PackageBuildResult:
    return PackageBuildResult(status=status, diagnostic=diagnostic)


def _successful_result(output_dir: Path) -> CanonicalPackageBuildResult:
    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    discovery = ArtifactDiscoveryResult(
        status=ArtifactDiscoveryStatus.SUCCEEDED,
        output_dir=output_dir,
        candidates=(
            DiscoveredArtifact(sdist, ArtifactClass.SOURCE_DISTRIBUTION),
            DiscoveredArtifact(wheel, ArtifactClass.PYTHON_WHEEL),
        ),
    )
    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.VALID,
        candidate_results=tuple(
            CandidatePackageValidationResult(
                candidate=candidate,
                status=PackageStructuralValidationStatus.VALID,
            )
            for candidate in discovery.candidates
        ),
    )
    return CanonicalPackageBuildResult(
        status=PackageBuildStatus.SUCCEEDED,
        execution=_execution(),
        source_state=_SOURCE_STATE,
        discovery=discovery,
        validation=validation,
    )


def test_familyos_build_is_registered() -> None:
    result = runner.invoke(app, ["--help"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "build" in result.output


def test_build_success_reports_outputs_and_returns_zero(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = tmp_path / "packages"
    use_case = _install_context(
        monkeypatch,
        _successful_result(output_dir),
    )

    result = runner.invoke(
        app,
        ["build", "--output-dir", str(output_dir)],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert "Canonical Package Build: SUCCEEDED" in result.output
    assert "python-wheel:" in result.output
    assert "source-distribution:" in result.output
    assert "Python Package Structural Validation: VALID" in result.output
    assert "validated" not in result.output.lower()
    assert "trusted" not in result.output.lower()
    assert "release-ready" not in result.output.lower()
    assert use_case.output_dirs == [output_dir]
    assert use_case.functional_validation_requests == [False]
    assert use_case.profile_requests == [BuildProfile.DEVELOPMENT]
    assert use_case.evidence_output_requests == [None]


@pytest.mark.parametrize(
    "profile",
    (
        BuildProfile.DEVELOPMENT,
        BuildProfile.VALIDATION,
        BuildProfile.CI,
        BuildProfile.RELEASE_CANDIDATE,
    ),
)
def test_build_explicit_profile_is_forwarded(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    profile: BuildProfile,
) -> None:
    output_dir = tmp_path / "packages"
    use_case = _install_context(
        monkeypatch,
        _successful_result(output_dir),
    )

    result = runner.invoke(
        app,
        [
            "build",
            "--output-dir",
            str(output_dir),
            "--profile",
            profile.value,
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert use_case.profile_requests == [profile]
    assert use_case.evidence_output_requests == [None]


def test_build_rejects_unsupported_profile_before_execution(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = tmp_path / "packages"
    use_case = _install_context(
        monkeypatch,
        _successful_result(output_dir),
    )

    result = runner.invoke(
        app,
        [
            "build",
            "--output-dir",
            str(output_dir),
            "--profile",
            "unsupported",
        ],
    )

    assert result.exit_code != 0
    assert use_case.output_dirs == []
    assert use_case.functional_validation_requests == []
    assert use_case.profile_requests == []
    assert use_case.evidence_output_requests == []


def test_build_functional_validation_option_renders_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = tmp_path / "packages"
    aggregate = _successful_result(output_dir)
    wheel = next(
        candidate
        for candidate in aggregate.candidates
        if candidate.artifact_class is ArtifactClass.PYTHON_WHEEL
    )
    use_case = _install_context(
        monkeypatch,
        replace(
            aggregate,
            functional_validation=PythonWheelFunctionalValidationResult(
                candidate=wheel,
                status=PackageFunctionalValidationStatus.VALID,
            ),
        ),
    )

    result = runner.invoke(
        app,
        [
            "build",
            "--output-dir",
            str(output_dir),
            "--functional-validation",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert "Python Wheel Functional Validation: VALID" in result.output
    assert use_case.functional_validation_requests == [True]
    assert use_case.profile_requests == [BuildProfile.DEVELOPMENT]


def test_build_functional_validation_failure_returns_nonzero_and_diagnostic(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = tmp_path / "packages"
    aggregate = _successful_result(output_dir)
    wheel = next(
        candidate
        for candidate in aggregate.candidates
        if candidate.artifact_class is ArtifactClass.PYTHON_WHEEL
    )
    functional_validation = PythonWheelFunctionalValidationResult(
        candidate=wheel,
        status=PackageFunctionalValidationStatus.INVALID,
        findings=(
            WheelFunctionalValidationFinding(
                WheelFunctionalValidationStage.CLI_SMOKE,
                "installed console entry point failed",
            ),
        ),
    )
    use_case = _install_context(
        monkeypatch,
        replace(
            aggregate,
            status=PackageBuildStatus.FAILED,
            functional_validation=functional_validation,
        ),
    )

    result = runner.invoke(
        app,
        [
            "build",
            "--output-dir",
            str(output_dir),
            "--functional-validation",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert "Canonical Package Build: FAILED" in result.output
    assert "Python Wheel Functional Validation: INVALID" in result.output
    assert "installed CLI smoke" in result.output
    assert "installed console entry point failed" in result.output
    assert use_case.functional_validation_requests == [True]
    assert use_case.profile_requests == [BuildProfile.DEVELOPMENT]
    for term in ("trusted", "release-ready", "integrity-verified"):
        assert term not in result.output.lower()


def test_build_failure_returns_nonzero_and_diagnostic(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = tmp_path / "packages"
    use_case = _install_context(
        monkeypatch,
        CanonicalPackageBuildResult(
            status=PackageBuildStatus.FAILED,
            execution=_execution(
                PackageBuildStatus.FAILED,
                diagnostic="backend failed",
            ),
            source_state=_SOURCE_STATE,
        ),
    )

    result = runner.invoke(
        app,
        ["build", "--output-dir", str(output_dir)],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert "Canonical Package Build: FAILED" in result.output
    assert "backend failed" in result.output
    assert use_case.profile_requests == [BuildProfile.DEVELOPMENT]


@pytest.mark.parametrize("unexpected_name", [None, "extra.whl", "backend.log"])
def test_discovery_failure_returns_nonzero(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    unexpected_name: str | None,
) -> None:
    output_dir = tmp_path / "packages"
    unexpected = (output_dir / unexpected_name,) if unexpected_name else ()
    diagnostic = (
        f"Artifact discovery failed: unexpected {unexpected_name}"
        if unexpected_name
        else "Artifact discovery failed: missing python-wheel"
    )
    aggregate = CanonicalPackageBuildResult(
        status=PackageBuildStatus.FAILED,
        execution=_execution(),
        source_state=_SOURCE_STATE,
        discovery=ArtifactDiscoveryResult(
            status=ArtifactDiscoveryStatus.FAILED,
            output_dir=output_dir,
            unexpected_outputs=unexpected,
            diagnostic=diagnostic,
        ),
    )
    use_case = _install_context(monkeypatch, aggregate)

    result = runner.invoke(
        app,
        ["build", "--output-dir", str(output_dir)],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert diagnostic in result.output
    assert use_case.profile_requests == [BuildProfile.DEVELOPMENT]


def test_structural_validation_failure_returns_nonzero_and_diagnostic(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = tmp_path / "packages"
    wheel = DiscoveredArtifact(
        output_dir / "familyos_cli-0.1.0-py3-none-any.whl",
        ArtifactClass.PYTHON_WHEEL,
    )
    discovery = ArtifactDiscoveryResult(
        status=ArtifactDiscoveryStatus.SUCCEEDED,
        output_dir=output_dir,
        candidates=(wheel,),
    )
    validation = PythonPackageStructuralValidationResult(
        status=PackageStructuralValidationStatus.INVALID,
        candidate_results=(
            CandidatePackageValidationResult(
                candidate=wheel,
                status=PackageStructuralValidationStatus.INVALID,
                diagnostics=("wheel is missing required METADATA metadata",),
            ),
        ),
    )
    use_case = _install_context(
        monkeypatch,
        CanonicalPackageBuildResult(
            status=PackageBuildStatus.FAILED,
            execution=_execution(),
            source_state=_SOURCE_STATE,
            discovery=discovery,
            validation=validation,
        ),
    )

    result = runner.invoke(
        app,
        ["build", "--output-dir", str(output_dir)],
        catch_exceptions=False,
    )

    assert result.exit_code == 1
    assert "Canonical Package Build: FAILED" in result.output
    assert "Python Package Structural Validation: INVALID" in result.output
    assert wheel.path.name in result.output
    assert "missing required METADATA" in result.output
    assert "trusted" not in result.output.lower()
    assert "release-ready" not in result.output.lower()
    assert "integrity-verified" not in result.output.lower()
    assert use_case.profile_requests == [BuildProfile.DEVELOPMENT]


def test_build_defaults_to_conventional_dist_directory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    use_case = _install_context(
        monkeypatch,
        _successful_result(Path("dist")),
    )

    result = runner.invoke(app, ["build"], catch_exceptions=False)

    assert result.exit_code == 0
    assert use_case.output_dirs == [Path("dist")]
    assert use_case.functional_validation_requests == [False]
    assert use_case.profile_requests == [BuildProfile.DEVELOPMENT]


def test_real_familyos_build_reports_valid_structural_packages(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "real-package-output"

    result = runner.invoke(
        app,
        ["build", "--output-dir", str(output_dir)],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output
    assert "Canonical Package Build: SUCCEEDED" in result.output
    assert "Build Profile: development" in result.output
    assert "Profile Supports Target: True" in result.output
    assert "Evidence Required: False" in result.output
    assert "Evidence Requested: False" in result.output
    assert "Python Package Structural Validation: VALID" in result.output
    assert len(tuple(output_dir.glob("*.whl"))) == 1
    assert len(tuple(output_dir.glob("*.tar.gz"))) == 1
    assert "trusted" not in result.output.lower()
    assert "release-ready" not in result.output.lower()
    assert "integrity-verified" not in result.output.lower()


def test_real_familyos_build_rejects_ci_profile_without_evidence(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "real-ci-package-output"

    result = runner.invoke(
        app,
        [
            "build",
            "--output-dir",
            str(output_dir),
            "--profile",
            BuildProfile.CI.value,
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 1, result.output
    assert "Canonical Package Build: FAILED" in result.output
    assert "Build Profile: ci" in result.output
    assert "Evidence Required: True" in result.output
    assert "Evidence Requested: False" in result.output
    assert "build profile requires an evidence output: ci" in result.output
    assert "Python Package Structural Validation" not in result.output
    assert not output_dir.exists()


@pytest.mark.parametrize(
    "profile",
    (BuildProfile.CI, BuildProfile.RELEASE_CANDIDATE),
)
def test_real_familyos_build_evidence_captures_dependency_state_and_profile(
    tmp_path: Path,
    profile: BuildProfile,
) -> None:
    output_dir = tmp_path / f"real-{profile.value}-package-output"
    evidence_output = tmp_path / f"{profile.value}-build-evidence.json"

    result = runner.invoke(
        app,
        [
            "build",
            "--output-dir",
            str(output_dir),
            "--profile",
            profile.value,
            "--evidence-output",
            str(evidence_output),
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output

    payload = json.loads(evidence_output.read_text(encoding="utf-8"))
    dependency_state = payload["dependency_state"]

    assert payload["validation"]["profile"] == profile.value
    assert payload["effective_configuration"] == {
        "profile": profile.value,
        "target": "familyos-cli-package",
        "functional_validation": False,
        "evidence_required": True,
        "evidence_requested": True,
        "target_supported": True,
    }
    assert dependency_state["declaration"]["identity"] == "pyproject.toml"
    assert dependency_state["lock"]["identity"] == "requirements.txt"
    assert len(dependency_state["declaration"]["sha256"]) == 64
    assert len(dependency_state["lock"]["sha256"]) == 64
    assert str(Path.cwd()) not in json.dumps(dependency_state)
