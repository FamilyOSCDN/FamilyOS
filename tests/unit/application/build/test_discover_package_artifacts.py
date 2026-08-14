"""Tests for deterministic Python package artifact discovery."""

from __future__ import annotations

from pathlib import Path

import pytest

from familyos_cli.application.build import (
    ArtifactClass,
    ArtifactDiscoveryStatus,
    ArtifactOutputClassification,
    DiscoverPackageArtifactsUseCase,
)


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    path = tmp_path / "dist"
    path.mkdir()
    return path


def _file(output_dir: Path, name: str) -> Path:
    path = output_dir / name
    path.touch()
    return path


def test_exact_wheel_and_sdist_succeeds_in_deterministic_order(
    output_dir: Path,
) -> None:
    wheel = _file(output_dir, "familyos_cli-0.1.0-py3-none-any.whl")
    sdist = _file(output_dir, "familyos_cli-0.1.0.tar.gz")

    result = DiscoverPackageArtifactsUseCase().execute(
        output_dir=output_dir,
        current_outputs=(sdist, wheel),
    )

    assert result.status is ArtifactDiscoveryStatus.SUCCEEDED
    assert tuple(artifact.path for artifact in result.candidates) == (wheel, sdist)
    assert tuple(artifact.artifact_class for artifact in result.candidates) == (
        ArtifactClass.PYTHON_WHEEL,
        ArtifactClass.SOURCE_DISTRIBUTION,
    )
    assert all(
        artifact.classification is ArtifactOutputClassification.CANDIDATE
        for artifact in result.candidates
    )
    assert result.missing_expectations == ()
    assert result.unexpected_outputs == ()


@pytest.mark.parametrize(
    ("present_name", "missing_class"),
    [
        ("familyos_cli-0.1.0.tar.gz", ArtifactClass.PYTHON_WHEEL),
        ("familyos_cli-0.1.0-py3-none-any.whl", ArtifactClass.SOURCE_DISTRIBUTION),
    ],
)
def test_missing_required_artifact_fails(
    output_dir: Path,
    present_name: str,
    missing_class: ArtifactClass,
) -> None:
    present = _file(output_dir, present_name)

    result = DiscoverPackageArtifactsUseCase().execute(
        output_dir=output_dir,
        current_outputs=(present,),
    )

    assert result.status is ArtifactDiscoveryStatus.FAILED
    assert result.missing_expectations == (missing_class,)
    assert result.diagnostic == f"Artifact discovery failed: missing {missing_class.value}"


def test_no_outputs_reports_both_missing_expectations(output_dir: Path) -> None:
    result = DiscoverPackageArtifactsUseCase().execute(
        output_dir=output_dir,
        current_outputs=(),
    )

    assert result.status is ArtifactDiscoveryStatus.FAILED
    assert result.missing_expectations == (
        ArtifactClass.PYTHON_WHEEL,
        ArtifactClass.SOURCE_DISTRIBUTION,
    )
    assert result.diagnostic == (
        "Artifact discovery failed: missing python-wheel; "
        "missing source-distribution"
    )


@pytest.mark.parametrize(
    "duplicate_names",
    [
        (
            "familyos_cli-0.1.0-py3-none-any.whl",
            "familyos_cli-0.1.0-py3-none-macosx.whl",
        ),
        ("familyos_cli-0.1.0.tar.gz", "familyos_cli-0.1.0.post1.tar.gz"),
    ],
)
def test_duplicate_artifact_class_fails(
    output_dir: Path,
    duplicate_names: tuple[str, str],
) -> None:
    outputs = tuple(_file(output_dir, name) for name in duplicate_names)
    counterpart = _file(
        output_dir,
        "familyos_cli-0.1.0.tar.gz"
        if duplicate_names[0].endswith(".whl")
        else "familyos_cli-0.1.0-py3-none-any.whl",
    )

    result = DiscoverPackageArtifactsUseCase().execute(
        output_dir=output_dir,
        current_outputs=(*outputs, counterpart),
    )

    assert result.status is ArtifactDiscoveryStatus.FAILED
    duplicate = sorted(outputs, key=lambda path: path.name)[1]
    assert result.unexpected_outputs == (duplicate,)
    assert result.diagnostic == f"Artifact discovery failed: unexpected {duplicate.name}"


def test_unexpected_current_file_fails(output_dir: Path) -> None:
    wheel = _file(output_dir, "familyos_cli-0.1.0-py3-none-any.whl")
    sdist = _file(output_dir, "familyos_cli-0.1.0.tar.gz")
    unexpected = _file(output_dir, "build.log")

    result = DiscoverPackageArtifactsUseCase().execute(
        output_dir=output_dir,
        current_outputs=(wheel, unexpected, sdist),
    )

    assert result.status is ArtifactDiscoveryStatus.FAILED
    assert result.unexpected_outputs == (unexpected,)
    assert result.diagnostic == "Artifact discovery failed: unexpected build.log"


def test_output_outside_canonical_directory_is_unexpected(
    output_dir: Path,
    tmp_path: Path,
) -> None:
    wheel = _file(output_dir, "familyos_cli-0.1.0-py3-none-any.whl")
    sdist = _file(output_dir, "familyos_cli-0.1.0.tar.gz")
    outside = _file(tmp_path, "outside.whl")

    result = DiscoverPackageArtifactsUseCase().execute(
        output_dir=output_dir,
        current_outputs=(wheel, sdist, outside),
    )

    assert result.status is ArtifactDiscoveryStatus.FAILED
    assert result.unexpected_outputs == (outside,)


def test_discovery_model_contains_no_later_maturity_fields(output_dir: Path) -> None:
    wheel = _file(output_dir, "familyos_cli-0.1.0-py3-none-any.whl")
    sdist = _file(output_dir, "familyos_cli-0.1.0.tar.gz")

    result = DiscoverPackageArtifactsUseCase().execute(
        output_dir=output_dir,
        current_outputs=(wheel, sdist),
    )

    for field in ("validated", "trusted", "digest", "build_id", "provenance"):
        assert not hasattr(result, field)
        assert all(not hasattr(artifact, field) for artifact in result.candidates)
