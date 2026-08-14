"""Tests for the subprocess-backed Python package builder."""

from __future__ import annotations

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
        capture_output: bool,
        check: bool,
        text: bool,
    ) -> subprocess.CompletedProcess[str]:
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


def test_nonzero_subprocess_result_is_normalized_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project_root = tmp_path / "project"
    output_dir = tmp_path / "packages"

    monkeypatch.setattr(
        subprocess,
        "run",
        lambda command, **kwargs: subprocess.CompletedProcess(
            command,
            7,
            "",
            f"failure in {project_root}",
        ),
    )

    result = PythonPackageBuilder("/controlled/python").build(
        project_root=project_root,
        output_dir=output_dir,
    )

    assert result.status is PackageBuildStatus.FAILED
    assert result.exit_code == 7
    assert result.outputs == ()
    assert result.diagnostic == "failure in ."


def test_subprocess_launch_problem_is_execution_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail(*args: object, **kwargs: object) -> None:
        raise OSError("frontend unavailable")

    monkeypatch.setattr(subprocess, "run", fail)

    result = PythonPackageBuilder("/controlled/python").build(
        project_root=tmp_path,
        output_dir=tmp_path / "packages",
    )

    assert result.status is PackageBuildStatus.ERROR
    assert result.exit_code is None
    assert result.outputs == ()
    assert result.diagnostic == "frontend unavailable"
