"""Tests for the canonical package-build use case."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build import (
    ArtifactDiscoveryResult,
    ArtifactDiscoveryStatus,
    DiscoverPackageArtifactsUseCase,
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

    result = RunPackageBuildUseCase(builder, discoverer, tmp_path).execute(
        Path("dist")
    )

    assert result.status is PackageBuildStatus.FAILED
    assert result.discovery is None
    assert result.diagnostic == "backend failed"
    assert not discoverer.called


def test_discovery_failure_makes_aggregate_build_fail(tmp_path: Path) -> None:
    execution = PackageBuildResult(status=PackageBuildStatus.SUCCEEDED, outputs=())

    result = RunPackageBuildUseCase(
        _PackageBuilder(execution),
        DiscoverPackageArtifactsUseCase(),
        tmp_path,
    ).execute(Path("dist"))

    assert result.status is PackageBuildStatus.FAILED
    assert result.discovery is not None
    assert result.discovery.status is ArtifactDiscoveryStatus.FAILED
    assert result.diagnostic == (
        "Artifact discovery failed: missing python-wheel; "
        "missing source-distribution"
    )
