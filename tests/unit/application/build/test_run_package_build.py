"""Tests for the canonical package-build use case."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build import (
    PackageBuildResult,
    PackageBuildStatus,
    RunPackageBuildUseCase,
)
from familyos_cli.application.ports.build import PackageBuilderPort


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


def test_use_case_delegates_explicit_paths_to_packaging_port(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    output_dir = tmp_path / "packages"
    expected = PackageBuildResult(status=PackageBuildStatus.SUCCEEDED)
    builder = _PackageBuilder(expected)

    result = RunPackageBuildUseCase(builder, project_root).execute(output_dir)

    assert result is expected
    assert builder.calls == [(project_root, output_dir)]


def test_use_case_resolves_relative_output_from_project_root(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    expected = PackageBuildResult(status=PackageBuildStatus.SUCCEEDED)
    builder = _PackageBuilder(expected)

    RunPackageBuildUseCase(builder, project_root).execute(Path("dist"))

    assert builder.calls == [(project_root, project_root / "dist")]


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
