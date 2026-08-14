"""Tests for clean-environment Python wheel functional validation."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from familyos_cli.application.build import (
    ArtifactClass,
    DiscoveredArtifact,
    PackageFunctionalValidationStatus,
    WheelFunctionalValidationStage,
)
from familyos_cli.infrastructure.build import PythonWheelFunctionalValidator


class _CommandRunner:
    def __init__(
        self,
        project_root: Path,
        *,
        failure_stage: WheelFunctionalValidationStage | None = None,
        resolve_import_from_checkout: bool = False,
    ) -> None:
        self.project_root = project_root
        self.failure_stage = failure_stage
        self.resolve_import_from_checkout = resolve_import_from_checkout
        self.environment_root: Path | None = None
        self.calls: list[tuple[tuple[str, ...], Path, dict[str, str]]] = []

    def __call__(
        self,
        command: tuple[str, ...],
        *,
        cwd: Path,
        env: dict[str, str],
        capture_output: bool,
        check: bool,
        text: bool,
        timeout: int,
    ) -> subprocess.CompletedProcess[str]:
        assert capture_output
        assert not check
        assert text
        assert timeout > 0
        self.calls.append((command, cwd, env))
        if command[1:3] == ("-m", "venv"):
            self.environment_root = Path(command[-1])
            return subprocess.CompletedProcess(command, 0, "", "")
        if command[1:3] == ("-m", "pip"):
            if self.failure_stage is WheelFunctionalValidationStage.INSTALLATION:
                return subprocess.CompletedProcess(
                    command, 1, "", "dependency installation failed"
                )
            return subprocess.CompletedProcess(command, 0, "", "")
        if command[1:3] == ("-I", "-c"):
            if self.failure_stage is WheelFunctionalValidationStage.IMPORT_SMOKE:
                return subprocess.CompletedProcess(
                    command, 1, "", "installed import failed"
                )
            assert self.environment_root is not None
            module_path = (
                self.project_root / "src" / "familyos_cli" / "main.py"
                if self.resolve_import_from_checkout
                else self.environment_root
                / "lib"
                / "python3.13"
                / "site-packages"
                / "familyos_cli"
                / "main.py"
            )
            return subprocess.CompletedProcess(
                command,
                0,
                json.dumps({"module_path": str(module_path)}),
                "",
            )
        if self.failure_stage is WheelFunctionalValidationStage.CLI_SMOKE:
            return subprocess.CompletedProcess(command, 1, "", "entry point failed")
        return subprocess.CompletedProcess(command, 0, "FamilyOS CLI\n", "")


@pytest.fixture
def functional_validation_inputs(
    tmp_path: Path,
) -> tuple[Path, Path, DiscoveredArtifact]:
    project_root = tmp_path / "project"
    project_root.mkdir()
    requirements_lock = project_root / "requirements.txt"
    requirements_lock.write_text("typer==0.26.8\n", encoding="utf-8")
    wheel = project_root / "dist" / "familyos_cli-0.1.0-py3-none-any.whl"
    wheel.parent.mkdir()
    wheel.touch()
    return (
        project_root,
        requirements_lock,
        DiscoveredArtifact(wheel, ArtifactClass.PYTHON_WHEEL),
    )


def _validator(
    project_root: Path,
    requirements_lock: Path,
) -> PythonWheelFunctionalValidator:
    return PythonWheelFunctionalValidator(
        project_root=project_root,
        requirements_lock=requirements_lock,
        python_executable="/controlled/python",
    )


def test_validates_with_isolated_commands_and_cleans_temporary_environment(
    functional_validation_inputs: tuple[Path, Path, DiscoveredArtifact],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project_root, requirements_lock, candidate = functional_validation_inputs
    monkeypatch.setenv("PYTHONPATH", str(project_root / "src"))
    runner = _CommandRunner(project_root)
    monkeypatch.setattr(
        "familyos_cli.infrastructure.build.python_wheel_functional_validator."
        "subprocess.run",
        runner,
    )

    result = _validator(project_root, requirements_lock).validate(candidate)

    assert result.status is PackageFunctionalValidationStatus.VALID
    assert result.diagnostic is None
    assert result.environment_root is not None
    assert result.imported_module_path is not None
    assert result.imported_module_path.is_relative_to(result.environment_root)
    assert not result.imported_module_path.is_relative_to(project_root / "src")
    assert not result.environment_root.exists()
    assert len(runner.calls) == 4
    for _, cwd, environment in runner.calls:
        assert not cwd.is_relative_to(project_root)
        assert "PYTHONPATH" not in environment
        assert environment["PYTHONNOUSERSITE"] == "1"
    creation_command = runner.calls[0][0]
    assert creation_command == (
        "/controlled/python",
        "-m",
        "venv",
        str(result.environment_root),
    )
    assert "--system-site-packages" not in creation_command
    installation_command = runner.calls[1][0]
    assert "--isolated" in installation_command
    assert "--require-virtualenv" in installation_command
    assert "--only-binary=:all:" in installation_command
    assert str(requirements_lock.resolve()) in installation_command
    assert str(candidate.path.resolve()) in installation_command
    assert "--requirement" not in installation_command
    assert "-r" not in installation_command
    assert "pytest" not in installation_command
    assert runner.calls[2][0][1:3] == ("-I", "-c")
    assert runner.calls[3][0][-1] == "--help"


@pytest.mark.parametrize(
    ("stage", "expected_diagnostic", "expected_call_count"),
    [
        (
            WheelFunctionalValidationStage.INSTALLATION,
            "dependency installation failed",
            2,
        ),
        (WheelFunctionalValidationStage.IMPORT_SMOKE, "installed import failed", 3),
        (WheelFunctionalValidationStage.CLI_SMOKE, "entry point failed", 4),
    ],
)
def test_stage_failure_is_invalid_and_stops_later_execution(
    functional_validation_inputs: tuple[Path, Path, DiscoveredArtifact],
    monkeypatch: pytest.MonkeyPatch,
    stage: WheelFunctionalValidationStage,
    expected_diagnostic: str,
    expected_call_count: int,
) -> None:
    project_root, requirements_lock, candidate = functional_validation_inputs
    runner = _CommandRunner(project_root, failure_stage=stage)
    monkeypatch.setattr(
        "familyos_cli.infrastructure.build.python_wheel_functional_validator."
        "subprocess.run",
        runner,
    )

    result = _validator(project_root, requirements_lock).validate(candidate)

    assert result.status is PackageFunctionalValidationStatus.INVALID
    assert result.findings[0].stage is stage
    assert expected_diagnostic in result.findings[0].diagnostic
    assert len(runner.calls) == expected_call_count
    assert result.environment_root is not None
    assert not result.environment_root.exists()


def test_checkout_import_resolution_is_rejected(
    functional_validation_inputs: tuple[Path, Path, DiscoveredArtifact],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project_root, requirements_lock, candidate = functional_validation_inputs
    runner = _CommandRunner(project_root, resolve_import_from_checkout=True)
    monkeypatch.setattr(
        "familyos_cli.infrastructure.build.python_wheel_functional_validator."
        "subprocess.run",
        runner,
    )

    result = _validator(project_root, requirements_lock).validate(candidate)

    assert result.status is PackageFunctionalValidationStatus.INVALID
    assert result.findings[0].stage is WheelFunctionalValidationStage.IMPORT_SMOKE
    assert result.findings[0].diagnostic == (
        "FamilyOS resolved outside the clean temporary environment"
    )
    assert len(runner.calls) == 3


def test_missing_wheel_fails_installation_without_spawning_process(
    functional_validation_inputs: tuple[Path, Path, DiscoveredArtifact],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project_root, requirements_lock, candidate = functional_validation_inputs
    candidate.path.unlink()
    runner = _CommandRunner(project_root)
    monkeypatch.setattr(
        "familyos_cli.infrastructure.build.python_wheel_functional_validator."
        "subprocess.run",
        runner,
    )

    result = _validator(project_root, requirements_lock).validate(candidate)

    assert result.status is PackageFunctionalValidationStatus.INVALID
    assert result.findings[0].stage is WheelFunctionalValidationStage.INSTALLATION
    assert result.findings[0].diagnostic == (
        "wheel candidate does not exist as a regular file"
    )
    assert runner.calls == []
