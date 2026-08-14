"""End-to-end tests for the canonical package-build CLI surface."""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from familyos_cli.application.build import PackageBuildResult, PackageBuildStatus
from familyos_cli.interfaces.cli.app import app
from familyos_cli.interfaces.cli.commands import build as build_command

runner = CliRunner()


class _UseCase:
    def __init__(self, result: PackageBuildResult) -> None:
        self.result = result
        self.output_dirs: list[Path] = []

    def execute(self, output_dir: Path) -> PackageBuildResult:
        self.output_dirs.append(output_dir)
        return self.result


class _Context:
    def __init__(self, use_case: _UseCase) -> None:
        self.run_package_build = use_case


def _install_context(
    monkeypatch: pytest.MonkeyPatch,
    result: PackageBuildResult,
) -> _UseCase:
    use_case = _UseCase(result)
    monkeypatch.setattr(build_command, "CommandContext", lambda: _Context(use_case))
    return use_case


def test_familyos_build_is_registered() -> None:
    result = runner.invoke(app, ["--help"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "build" in result.output


def test_build_success_reports_outputs_and_returns_zero(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = tmp_path / "packages"
    wheel = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    sdist = output_dir / "familyos_cli-0.1.0.tar.gz"
    use_case = _install_context(
        monkeypatch,
        PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
            outputs=(wheel, sdist),
            exit_code=0,
        ),
    )

    result = runner.invoke(
        app,
        ["build", "--output-dir", str(output_dir)],
        catch_exceptions=False,
    )

    assert result.exit_code == 0
    assert "Canonical Package Build: SUCCEEDED" in result.output
    assert str(wheel) in result.output
    assert str(sdist) in result.output
    assert use_case.output_dirs == [output_dir]


def test_build_failure_returns_nonzero_and_diagnostic(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = tmp_path / "packages"
    _install_context(
        monkeypatch,
        PackageBuildResult(
            status=PackageBuildStatus.FAILED,
            exit_code=2,
            diagnostic="backend failed",
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


def test_build_defaults_to_conventional_dist_directory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    use_case = _install_context(
        monkeypatch,
        PackageBuildResult(status=PackageBuildStatus.SUCCEEDED, exit_code=0),
    )

    result = runner.invoke(app, ["build"], catch_exceptions=False)

    assert result.exit_code == 0
    assert use_case.output_dirs == [Path("dist")]
