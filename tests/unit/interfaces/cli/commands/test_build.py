"""Tests for the canonical package-build CLI command."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any
from uuid import UUID

import familyos_cli.interfaces.cli.commands.build as build_command
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

    def execute(
        self,
        output_dir: Path,
        *,
        validate_functionally: bool,
    ) -> Any:
        del output_dir
        del validate_functionally
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
        diagnostic=None if successful else "package build failed",
    )


def _install_evidence_fakes(
    monkeypatch: Any,
    *,
    package_result: Any,
    captured: dict[str, Any],
) -> None:
    monkeypatch.setattr(
        build_command,
        "CommandContext",
        lambda: _CommandContext(package_result),
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


def test_successful_build_writes_build_evidence(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    result = _package_result(successful=True)
    captured: dict[str, Any] = {}

    _install_evidence_fakes(
        monkeypatch,
        package_result=result,
        captured=captured,
    )

    evidence_output = tmp_path / "build-evidence.json"

    exit_code = build_command.run_package_build(
        tmp_path / "dist",
        functional_validation=False,
        evidence_output=evidence_output,
    )

    assert exit_code == build_command.EXIT_SUCCESS
    assert evidence_output.read_text(encoding="utf-8") == (
        '{"build_id": "01234567-89ab-4cde-8f01-23456789abcd"}\n'
    )

    assert captured["check_result"] is result
    assert (
        captured["functional_requirement"]
        is BuildValidationRequirement.OPTIONAL
    )
    assert captured["validation_build_id"] == _BUILD_ID
    assert captured["validation_profile"] is BuildValidationProfile.CI
    assert captured["validation_checks"] == ("package-checks",)
    assert captured["evidence_package_result"] is result
    assert captured["rendered_evidence"] is not None


def test_functional_build_requires_functional_validation_in_evidence(
    tmp_path: Path,
    monkeypatch: Any,
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
        functional_validation=True,
        evidence_output=tmp_path / "build-evidence.json",
    )

    assert exit_code == build_command.EXIT_SUCCESS
    assert (
        captured["functional_requirement"]
        is BuildValidationRequirement.REQUIRED
    )
    assert captured["validation_profile"] is BuildValidationProfile.CI


def test_failed_build_does_not_write_build_evidence(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    result = _package_result(successful=False)
    captured: dict[str, Any] = {}

    _install_evidence_fakes(
        monkeypatch,
        package_result=result,
        captured=captured,
    )

    evidence_output = tmp_path / "build-evidence.json"

    exit_code = build_command.run_package_build(
        tmp_path / "dist",
        functional_validation=False,
        evidence_output=evidence_output,
    )

    assert exit_code == build_command.EXIT_FAILURE
    assert not evidence_output.exists()
    assert "validation_profile" not in captured
    assert "rendered_evidence" not in captured


def test_build_renders_non_sensitive_build_context(
    tmp_path: Path,
    monkeypatch: Any,
    capsys: Any,
) -> None:
    from familyos_cli.application.build.build_context import (
        BuildContext,
        BuildEffectiveConfiguration,
        BuildProfile,
        BuildTarget,
    )
    from familyos_cli.application.build.dependency_state import (
        DependencyState,
    )
    from familyos_cli.application.build.toolchain_state import (
        ToolchainState,
        ToolchainVersion,
    )

    result = _package_result(successful=True)

    result.build_context = BuildContext(
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
        profile=BuildProfile.CI,
        target=BuildTarget.FAMILYOS_CLI_PACKAGE,
        runtime_version="3.13.7",
        effective_configuration=BuildEffectiveConfiguration(
            functional_validation=False,
        ),
        output_dir=tmp_path / "dist",
    )

    captured: dict[str, Any] = {}

    _install_evidence_fakes(
        monkeypatch,
        package_result=result,
        captured=captured,
    )

    exit_code = build_command.run_package_build(
        tmp_path / "dist",
        functional_validation=False,
    )

    stdout = capsys.readouterr().out

    assert exit_code == build_command.EXIT_SUCCESS
    assert "Build Profile: ci" in stdout
    assert "Build Target: familyos-cli-package" in stdout
    assert "Runtime Version: 3.13.7" in stdout
    assert "Toolchain build: 1.5.0" in stdout
    assert "Toolchain pip-tools: 7.6.1" in stdout
    assert "Toolchain setuptools: 84.0.0" in stdout
    assert "Toolchain wheel: 0.48.0" in stdout
    assert f"Output Directory: {tmp_path / 'dist'}" in stdout
    assert "Functional Validation Requested: False" in stdout
