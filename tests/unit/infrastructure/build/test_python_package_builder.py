"""Tests for the subprocess-backed Python package builder."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from familyos_cli.application.build import PackageBuildStatus
from familyos_cli.infrastructure.build import PythonPackageBuilder


def test_success_invokes_standard_frontend_and_reports_package_outputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project_root = tmp_path / "project"
    output_dir = tmp_path / "packages"
    project_root.mkdir()
    output_dir.mkdir()
    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    unrelated = output_dir / "notes.txt"
    unrelated.touch()
    calls: list[tuple[tuple[str, ...], Path]] = []

    def succeed(
        command: tuple[str, ...],
        *,
        cwd: Path,
        env: dict[str, str],
        capture_output: bool,
        check: bool,
        text: bool,
    ) -> subprocess.CompletedProcess[str]:
        assert env["PYTHONNOUSERSITE"] == "1"
        assert capture_output
        assert not check
        assert text
        calls.append((command, cwd))
        wheel.touch()
        sdist.touch()
        return subprocess.CompletedProcess(command, 0, "built", "")

    monkeypatch.setattr(subprocess, "run", succeed)

    result = PythonPackageBuilder("/controlled/python").build(
        project_root=project_root,
        output_dir=output_dir,
    )

    assert calls == [
        (
            (
                "/controlled/python",
                "-m",
                "build",
                "--dependency-constraints-txt",
                str((project_root / "requirements.txt").resolve()),
                "--outdir",
                str(output_dir),
            ),
            project_root,
        ),
    ]
    assert result.status is PackageBuildStatus.SUCCEEDED
    assert result.outputs == (wheel, sdist)
    assert "publish" not in calls[0][0]
    assert "upload" not in calls[0][0]
    assert "twine" not in calls[0][0]
    assert "--wheel" not in calls[0][0]
    assert "--sdist" not in calls[0][0]


def test_build_uses_sanitized_environment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    removed_variables = (
        "PYTHONHOME",
        "PYTHONPATH",
        "PYTHONSTARTUP",
        "PYTHONUSERBASE",
        "VIRTUAL_ENV",
        "__PYVENV_LAUNCHER__",
        "TWINE_USERNAME",
        "TWINE_PASSWORD",
        "UV_PUBLISH_USERNAME",
        "UV_PUBLISH_PASSWORD",
        "UV_PUBLISH_TOKEN",
    )
    for name in removed_variables:
        monkeypatch.setenv(name, f"inherited-{name.lower()}")
    monkeypatch.setenv("PYTHONNOUSERSITE", "0")
    monkeypatch.setenv("FAMILYOS_SAFE_BUILD_VARIABLE", "preserved")
    environments: list[dict[str, str]] = []

    def succeed(
        command: tuple[str, ...],
        *,
        env: dict[str, str],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        environments.append(env)
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(subprocess, "run", succeed)

    result = PythonPackageBuilder("/controlled/python").build(
        project_root=tmp_path,
        output_dir=tmp_path / "packages",
    )

    assert result.status is PackageBuildStatus.SUCCEEDED
    assert len(environments) == 1
    environment = environments[0]
    for name in removed_variables:
        assert name not in environment
    assert environment["PYTHONNOUSERSITE"] == "1"
    assert environment["FAMILYOS_SAFE_BUILD_VARIABLE"] == "preserved"


def test_constraints_path_is_absolute_and_independent_of_caller_cwd(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    caller_cwd = tmp_path / "caller"
    caller_cwd.mkdir()
    monkeypatch.chdir(caller_cwd)
    calls: list[tuple[tuple[str, ...], Path]] = []

    def succeed(
        command: tuple[str, ...],
        *,
        cwd: Path,
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        calls.append((command, cwd))
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(subprocess, "run", succeed)

    result = PythonPackageBuilder("/controlled/python").build(
        project_root=project_root,
        output_dir=tmp_path / "packages",
    )

    assert result.status is PackageBuildStatus.SUCCEEDED
    assert len(calls) == 1
    command, subprocess_cwd = calls[0]
    constraint_index = command.index("--dependency-constraints-txt") + 1
    constraint_path = Path(command[constraint_index])
    assert constraint_path == (project_root / "requirements.txt").resolve()
    assert constraint_path.is_absolute()
    assert constraint_path.parent != caller_cwd
    assert subprocess_cwd == project_root


def test_success_does_not_report_unchanged_stale_package_outputs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = tmp_path / "packages"
    output_dir.mkdir()
    (output_dir / "stale.whl").touch()

    monkeypatch.setattr(
        subprocess,
        "run",
        lambda command, **kwargs: subprocess.CompletedProcess(command, 0, "", ""),
    )

    result = PythonPackageBuilder("/controlled/python").build(
        project_root=tmp_path,
        output_dir=output_dir,
    )

    assert result.status is PackageBuildStatus.SUCCEEDED
    assert result.outputs == ()


def test_success_reports_all_new_direct_files_including_unexpected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = tmp_path / "packages"
    output_dir.mkdir()
    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    unexpected = output_dir / "backend.log"

    def succeed(command: tuple[str, ...], **kwargs: object) -> subprocess.CompletedProcess[str]:
        wheel.touch()
        unexpected.touch()
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(subprocess, "run", succeed)

    result = PythonPackageBuilder("/controlled/python").build(
        project_root=tmp_path,
        output_dir=output_dir,
    )

    assert result.outputs == (unexpected, wheel)


def test_success_reports_changed_stale_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = tmp_path / "packages"
    output_dir.mkdir()
    stale = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    stale.write_text("old", encoding="utf-8")

    def succeed(command: tuple[str, ...], **kwargs: object) -> subprocess.CompletedProcess[str]:
        stale.write_text("replacement output", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(subprocess, "run", succeed)

    result = PythonPackageBuilder("/controlled/python").build(
        project_root=tmp_path,
        output_dir=output_dir,
    )

    assert result.outputs == (stale,)


def test_same_size_same_mtime_content_replacement_is_reported(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = tmp_path / "packages"
    output_dir.mkdir()
    replaced = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    replaced.write_bytes(b"old!")
    original_mtime_ns = replaced.stat().st_mtime_ns

    def succeed(command: tuple[str, ...], **kwargs: object) -> subprocess.CompletedProcess[str]:
        replaced.write_bytes(b"new!")
        os.utime(replaced, ns=(original_mtime_ns, original_mtime_ns))
        assert replaced.stat().st_size == 4
        assert replaced.stat().st_mtime_ns == original_mtime_ns
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(subprocess, "run", succeed)

    result = PythonPackageBuilder("/controlled/python").build(
        project_root=tmp_path,
        output_dir=output_dir,
    )

    assert replaced.read_bytes() == b"new!"
    assert result.outputs == (replaced,)



def test_nonzero_subprocess_result_is_normalized_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project_root = tmp_path / "project"
    output_dir = tmp_path / "packages"
    output_dir.mkdir()

    stale = output_dir / "stale.whl"
    stale.write_text("unchanged", encoding="utf-8")

    partial = output_dir / "familyos_cli-0.1.0.tar.gz"

    def fail(
        command: tuple[str, ...],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        partial.write_text(
            "partial package output",
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(
            command,
            7,
            "",
            f"failure in {project_root}",
        )

    monkeypatch.setattr(
        subprocess,
        "run",
        fail,
    )

    result = PythonPackageBuilder("/controlled/python").build(
        project_root=project_root,
        output_dir=output_dir,
    )

    assert result.status is PackageBuildStatus.FAILED
    assert result.exit_code == 7
    assert result.outputs == (partial,)
    assert stale not in result.outputs
    assert result.diagnostic == "failure in ."


def test_subprocess_launch_problem_is_execution_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = tmp_path / "packages"
    output_dir.mkdir()

    stale = output_dir / "stale.whl"
    stale.write_text("unchanged", encoding="utf-8")

    partial = output_dir / "backend.log"

    def fail(
        *args: object,
        **kwargs: object,
    ) -> None:
        partial.write_text(
            "partial frontend state",
            encoding="utf-8",
        )
        raise OSError("frontend unavailable")

    monkeypatch.setattr(
        subprocess,
        "run",
        fail,
    )

    result = PythonPackageBuilder("/controlled/python").build(
        project_root=tmp_path,
        output_dir=output_dir,
    )

    assert result.status is PackageBuildStatus.ERROR
    assert result.exit_code is None
    assert result.outputs == (partial,)
    assert stale not in result.outputs
    assert result.diagnostic == "frontend unavailable"


def test_build_uses_canonical_source_date_epoch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("SOURCE_DATE_EPOCH", raising=False)
    environments: list[dict[str, str]] = []

    def succeed(
        command: tuple[str, ...],
        *,
        env: dict[str, str],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        environments.append(env)
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(subprocess, "run", succeed)

    result = PythonPackageBuilder("/controlled/python").build(
        project_root=tmp_path,
        output_dir=tmp_path / "packages",
    )

    assert result.status is PackageBuildStatus.SUCCEEDED
    assert len(environments) == 1
    assert environments[0]["SOURCE_DATE_EPOCH"] == "315532800"


def test_build_overrides_inherited_source_date_epoch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1787654321")
    environments: list[dict[str, str]] = []

    def succeed(
        command: tuple[str, ...],
        *,
        env: dict[str, str],
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        environments.append(env)
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(subprocess, "run", succeed)

    result = PythonPackageBuilder("/controlled/python").build(
        project_root=tmp_path,
        output_dir=tmp_path / "packages",
    )

    assert result.status is PackageBuildStatus.SUCCEEDED
    assert len(environments) == 1
    assert environments[0]["SOURCE_DATE_EPOCH"] == "315532800"
