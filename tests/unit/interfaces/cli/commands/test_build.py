"""Tests for the canonical package-build CLI command."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any
from uuid import UUID

import pytest

import familyos_cli.interfaces.cli.commands.build as build_command
from familyos_cli.application.build.build_context import BuildProfile, BuildTarget
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationProfile,
    BuildValidationRequirement,
)

_BUILD_ID = BuildId(
    UUID("01234567-89ab-4cde-8f01-23456789abcd")
)


class _RunPackageBuild:
    def __init__(self, result: Any) -> None:
        self._result = result
        self.calls: list[
            tuple[Path, bool, BuildProfile, Path | None]
        ] = []

    def execute(
        self,
        output_dir: Path,
        *,
        validate_functionally: bool,
        profile: BuildProfile = BuildProfile.DEVELOPMENT,
        evidence_output: Path | None = None,
    ) -> Any:
        self.calls.append(
            (
                output_dir,
                validate_functionally,
                profile,
                evidence_output,
            )
        )
        if (
            evidence_output is not None
            and self._result.build_context is None
        ):
            self._result.build_context = SimpleNamespace(
                profile=profile,
                target=BuildTarget.FAMILYOS_CLI_PACKAGE,
                runtime_version="3.13.7",
                environment_state=SimpleNamespace(
                    operating_system="TestOS",
                    operating_system_release="1.0",
                    machine_architecture="test-machine",
                    virtual_environment_active=True,
                    temporary_directory="/tmp",
                    filesystem_encoding="utf-8",
                ),
                toolchain_state=SimpleNamespace(critical_versions=()),
                output_dir=output_dir,
                evidence_output=evidence_output,
                effective_configuration=SimpleNamespace(
                    functional_validation=validate_functionally,
                ),
            )
        return self._result


class _CommandContext:
    def __init__(self, result: Any) -> None:
        self.run_package_build = _RunPackageBuild(result)


def _package_result(*, successful: bool) -> Any:
    return SimpleNamespace(
        successful=successful,
        status=SimpleNamespace(
            value="succeeded" if successful else "failed",
        ),
        build_id=_BUILD_ID,
        source_state=SimpleNamespace(
            revision="0123456789abcdef0123456789abcdef01234567",
            dirty=False,
        ),
        build_context=None,
        candidates=(),
        validation=None,
        functional_validation=None,
        execution_observations=(),
        diagnostic=None if successful else "package build failed",
    )


def _install_evidence_fakes(
    monkeypatch: Any,
    *,
    package_result: Any,
    captured: dict[str, Any],
) -> _CommandContext:
    context = _CommandContext(package_result)

    monkeypatch.setattr(
        build_command,
        "CommandContext",
        lambda: context,
    )

    class CheckFactory:
        def from_package_build(
            self,
            result: Any,
            *,
            functional_requirement: BuildValidationRequirement,
        ) -> tuple[str, ...]:
            captured["check_result"] = result
            captured["functional_requirement"] = functional_requirement
            return ("package-checks",)

    class Orchestrator:
        def execute(
            self,
            *,
            build_id: BuildId,
            profile: BuildValidationProfile,
            checks: tuple[str, ...],
        ) -> Any:
            captured["validation_build_id"] = build_id
            captured["validation_profile"] = profile
            captured["validation_checks"] = checks
            return SimpleNamespace(
                build_id=build_id,
                profile=profile,
                checks=checks,
                status=SimpleNamespace(value="passed"),
                successful=True,
            )

    evidence = object()

    class EvidenceFactory:
        def from_package_build(
            self,
            result: Any,
            validation_result: Any,
        ) -> object:
            captured["evidence_package_result"] = result
            captured["evidence_validation_result"] = validation_result
            return evidence

    class EvidenceRenderer:
        def render(self, received_evidence: object) -> str:
            captured["rendered_evidence"] = received_evidence
            return '{"build_id": "01234567-89ab-4cde-8f01-23456789abcd"}\n'

    monkeypatch.setattr(
        build_command,
        "BuildValidationCheckFactory",
        CheckFactory,
        raising=False,
    )
    monkeypatch.setattr(
        build_command,
        "BuildValidationOrchestrator",
        Orchestrator,
        raising=False,
    )
    monkeypatch.setattr(
        build_command,
        "BuildEvidenceFactory",
        EvidenceFactory,
        raising=False,
    )
    monkeypatch.setattr(
        build_command,
        "BuildEvidenceJsonRenderer",
        EvidenceRenderer,
        raising=False,
    )

    return context


def test_successful_build_writes_build_evidence(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    result = _package_result(successful=True)
    captured: dict[str, Any] = {}

    context = _install_evidence_fakes(
        monkeypatch,
        package_result=result,
        captured=captured,
    )

    output_dir = tmp_path / "dist"
    evidence_output = tmp_path / "build-evidence.json"

    exit_code = build_command.run_package_build(
        output_dir,
        functional_validation=False,
        evidence_output=evidence_output,
    )

    assert exit_code == build_command.EXIT_SUCCESS
    assert evidence_output.read_text(encoding="utf-8") == (
        '{"build_id": "01234567-89ab-4cde-8f01-23456789abcd"}\n'
    )

    assert context.run_package_build.calls == [
        (
            output_dir,
            False,
            BuildProfile.DEVELOPMENT,
            evidence_output,
        )
    ]

    assert captured["check_result"] is result
    assert (
        captured["functional_requirement"]
        is BuildValidationRequirement.OPTIONAL
    )
    assert captured["validation_build_id"] == _BUILD_ID
    assert (
        captured["validation_profile"]
        is BuildValidationProfile.DEVELOPMENT
    )
    assert captured["validation_checks"] == ("package-checks",)
    assert captured["evidence_package_result"] is result
    assert captured["rendered_evidence"] is not None


def test_explicit_build_profile_is_forwarded_to_use_case(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    result = _package_result(successful=True)
    captured: dict[str, Any] = {}

    context = _install_evidence_fakes(
        monkeypatch,
        package_result=result,
        captured=captured,
    )

    output_dir = tmp_path / "dist"
    evidence_output = tmp_path / "build-evidence.json"

    exit_code = build_command.run_package_build(
        output_dir,
        functional_validation=False,
        profile=BuildProfile.CI,
        evidence_output=evidence_output,
    )

    assert exit_code == build_command.EXIT_SUCCESS
    assert context.run_package_build.calls == [
        (
            output_dir,
            False,
            BuildProfile.CI,
            evidence_output,
        )
    ]


def test_evidence_output_does_not_implicitly_select_ci_build_profile(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    result = _package_result(successful=True)
    captured: dict[str, Any] = {}

    context = _install_evidence_fakes(
        monkeypatch,
        package_result=result,
        captured=captured,
    )

    output_dir = tmp_path / "dist"

    exit_code = build_command.run_package_build(
        output_dir,
        functional_validation=False,
        evidence_output=tmp_path / "build-evidence.json",
    )

    assert exit_code == build_command.EXIT_SUCCESS
    assert context.run_package_build.calls == [
        (
            output_dir,
            False,
            BuildProfile.DEVELOPMENT,
            tmp_path / "build-evidence.json",
        )
    ]

    assert (
        captured["validation_profile"]
        is BuildValidationProfile.DEVELOPMENT
    )


def test_functional_build_requires_functional_validation_in_evidence(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    result = _package_result(successful=True)
    captured: dict[str, Any] = {}

    context = _install_evidence_fakes(
        monkeypatch,
        package_result=result,
        captured=captured,
    )

    output_dir = tmp_path / "dist"

    exit_code = build_command.run_package_build(
        output_dir,
        functional_validation=True,
        evidence_output=tmp_path / "build-evidence.json",
    )

    assert exit_code == build_command.EXIT_SUCCESS
    assert context.run_package_build.calls == [
        (
            output_dir,
            True,
            BuildProfile.DEVELOPMENT,
            tmp_path / "build-evidence.json",
        )
    ]
    assert (
        captured["functional_requirement"]
        is BuildValidationRequirement.REQUIRED
    )
    assert (
        captured["validation_profile"]
        is BuildValidationProfile.DEVELOPMENT
    )


@pytest.mark.parametrize(
    ("build_profile", "validation_profile"),
    (
        (
            BuildProfile.DEVELOPMENT,
            BuildValidationProfile.DEVELOPMENT,
        ),
        (
            BuildProfile.VALIDATION,
            BuildValidationProfile.VALIDATION,
        ),
        (BuildProfile.CI, BuildValidationProfile.CI),
        (
            BuildProfile.RELEASE_CANDIDATE,
            BuildValidationProfile.RELEASE_CANDIDATE,
        ),
    ),
)
def test_evidence_validation_profile_matches_build_profile(
    tmp_path: Path,
    monkeypatch: Any,
    build_profile: BuildProfile,
    validation_profile: BuildValidationProfile,
) -> None:
    result = _package_result(successful=True)
    captured: dict[str, Any] = {}

    _install_evidence_fakes(
        monkeypatch,
        package_result=result,
        captured=captured,
    )

    exit_code = build_command.run_package_build(
        tmp_path / "dist",
        functional_validation=False,
        profile=build_profile,
        evidence_output=tmp_path / "build-evidence.json",
    )

    assert exit_code == build_command.EXIT_SUCCESS
    assert captured["validation_profile"] is validation_profile


def test_failed_build_does_not_write_build_evidence(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    result = _package_result(successful=False)
    captured: dict[str, Any] = {}

    context = _install_evidence_fakes(
        monkeypatch,
        package_result=result,
        captured=captured,
    )

    output_dir = tmp_path / "dist"
    evidence_output = tmp_path / "build-evidence.json"

    exit_code = build_command.run_package_build(
        output_dir,
        functional_validation=False,
        evidence_output=evidence_output,
    )

    assert exit_code == build_command.EXIT_FAILURE
    assert context.run_package_build.calls == [
        (
            output_dir,
            False,
            BuildProfile.DEVELOPMENT,
            evidence_output,
        )
    ]
    assert not evidence_output.exists()
    assert "validation_profile" not in captured
    assert "rendered_evidence" not in captured


def test_evidence_is_written_to_resolved_context_destination(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    result = _package_result(successful=True)
    project_root = tmp_path / "project"
    caller_directory = tmp_path / "caller"
    caller_directory.mkdir()
    resolved_evidence_output = project_root / "build-evidence.json"
    result.build_context = SimpleNamespace(
        evidence_output=resolved_evidence_output,
    )
    captured: dict[str, Any] = {}

    context = _install_evidence_fakes(
        monkeypatch,
        package_result=result,
        captured=captured,
    )
    monkeypatch.setattr(build_command, "_render_result", lambda _: None)
    monkeypatch.chdir(caller_directory)

    exit_code = build_command.run_package_build(
        Path("dist"),
        functional_validation=False,
        evidence_output=Path("build-evidence.json"),
    )

    assert exit_code == build_command.EXIT_SUCCESS
    assert resolved_evidence_output.is_file()
    assert not (caller_directory / "build-evidence.json").exists()
    assert context.run_package_build.calls == [
        (
            Path("dist"),
            False,
            BuildProfile.DEVELOPMENT,
            Path("build-evidence.json"),
        )
    ]


def test_build_renders_non_sensitive_build_context(
    tmp_path: Path,
    monkeypatch: Any,
    capsys: Any,
) -> None:
    from familyos_cli.application.build.build_context import (
        BuildContext,
        BuildEffectiveConfiguration,
        BuildTarget,
    )
    from familyos_cli.application.build.dependency_state import (
        DependencyState,
    )
    from familyos_cli.application.build.environment_state import (
        EnvironmentState,
    )
    from familyos_cli.application.build.toolchain_state import (
        ToolchainState,
        ToolchainVersion,
    )

    result = _package_result(successful=True)

    result.build_context = BuildContext(
        build_id=_BUILD_ID,
        source_state=result.source_state,
        dependency_state=DependencyState(
            declaration_path=tmp_path / "pyproject.toml",
            declaration_digest="a" * 64,
            lock_path=tmp_path / "requirements.txt",
            lock_digest="b" * 64,
        ),
        toolchain_state=ToolchainState(
            critical_versions=(
                ToolchainVersion("build", "1.5.0"),
                ToolchainVersion("pip-tools", "7.6.1"),
                ToolchainVersion("setuptools", "84.0.0"),
                ToolchainVersion("wheel", "0.48.0"),
            ),
        ),
        environment_state=EnvironmentState(
            operating_system="Darwin",
            operating_system_release="24.6.0",
            machine_architecture="arm64",
        ),
        profile=BuildProfile.CI,
        target=BuildTarget.FAMILYOS_CLI_PACKAGE,
        runtime_version="3.13.7",
        effective_configuration=BuildEffectiveConfiguration(
            functional_validation=False,
        ),
        output_dir=tmp_path / "dist",
        evidence_output=None,
    )

    captured: dict[str, Any] = {}

    context = _install_evidence_fakes(
        monkeypatch,
        package_result=result,
        captured=captured,
    )

    output_dir = tmp_path / "dist"

    exit_code = build_command.run_package_build(
        output_dir,
        functional_validation=False,
        profile=BuildProfile.CI,
    )

    stdout = capsys.readouterr().out

    assert exit_code == build_command.EXIT_SUCCESS
    assert context.run_package_build.calls == [
        (
            output_dir,
            False,
            BuildProfile.CI,
            None,
        )
    ]
    assert "Build Profile: ci" in stdout
    assert "Build Target: familyos-cli-package" in stdout
    assert "Profile Supports Target: True" in stdout
    assert "Runtime Version: 3.13.7" in stdout
    assert "Operating System: Darwin" in stdout
    assert "Operating System Release: 24.6.0" in stdout
    assert "Machine Architecture: arm64" in stdout
    assert "Virtual Environment Active: False" in stdout
    assert "Temporary Directory: /tmp" in stdout
    assert "Filesystem Encoding: utf-8" in stdout
    assert "Toolchain build: 1.5.0" in stdout
    assert "Toolchain pip-tools: 7.6.1" in stdout
    assert "Toolchain setuptools: 84.0.0" in stdout
    assert "Toolchain wheel: 0.48.0" in stdout
    assert f"Output Directory: {tmp_path / 'dist'}" in stdout
    assert "Evidence Required: True" in stdout
    assert "Evidence Requested: False" in stdout
    assert "Evidence Output: not requested" in stdout
    assert "Functional Validation Requested: False" in stdout


def test_build_renders_execution_observations_in_order(
    monkeypatch: Any,
    capsys: Any,
) -> None:
    from familyos_cli.application.build.build_execution_observation import (
        BuildExecutionObservation,
        BuildExecutionStage,
        BuildExecutionStageStatus,
    )

    result = _package_result(successful=True)
    result.execution_observations = (
        BuildExecutionObservation(
            stage=BuildExecutionStage.VALIDATE_INPUTS,
            status=BuildExecutionStageStatus.SUCCEEDED,
            duration_seconds=0.01,
        ),
        BuildExecutionObservation(
            stage=BuildExecutionStage.PACKAGE,
            status=BuildExecutionStageStatus.SUCCEEDED,
            duration_seconds=0.25,
        ),
    )

    context = _CommandContext(result)
    monkeypatch.setattr(
        build_command,
        "CommandContext",
        lambda: context,
    )

    exit_code = build_command.run_package_build(
        Path("dist"),
        functional_validation=False,
    )

    stdout = capsys.readouterr().out

    assert exit_code == build_command.EXIT_SUCCESS
    assert "Execution Stages:" in stdout

    first = "- validate-inputs: SUCCEEDED (0.010000s)"
    second = "- package: SUCCEEDED (0.250000s)"

    assert first in stdout
    assert second in stdout
    assert stdout.index(first) < stdout.index(second)


def test_build_renders_failed_execution_observation_diagnostic(
    monkeypatch: Any,
    capsys: Any,
) -> None:
    from familyos_cli.application.build.build_execution_observation import (
        BuildExecutionObservation,
        BuildExecutionStage,
        BuildExecutionStageStatus,
    )

    result = _package_result(successful=False)
    result.execution_observations = (
        BuildExecutionObservation(
            stage=BuildExecutionStage.PACKAGE,
            status=BuildExecutionStageStatus.FAILED,
            duration_seconds=0.5,
            diagnostic="package frontend failed",
        ),
    )

    context = _CommandContext(result)
    monkeypatch.setattr(
        build_command,
        "CommandContext",
        lambda: context,
    )

    exit_code = build_command.run_package_build(
        Path("dist"),
        functional_validation=False,
    )

    captured = capsys.readouterr()

    assert exit_code == build_command.EXIT_FAILURE
    assert (
        "- package: FAILED (0.500000s) — package frontend failed"
        in captured.out
    )
