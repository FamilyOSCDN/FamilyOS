"""Real isolated integration coverage for canonical Python packaging."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

from familyos_cli.application.build import (
    ArtifactClass,
    DiscoverPackageArtifactsUseCase,
    PackageBuildStatus,
    PackageStructuralValidationStatus,
    RunPackageBuildUseCase,
    ValidatePythonPackageArtifactsUseCase,
)
from familyos_cli.infrastructure.build import PythonPackageBuilder


def _tracked_snapshot(repository_root: Path) -> dict[str, bytes | None]:
    completed = subprocess.run(
        ("git", "ls-files", "-z"),
        cwd=repository_root,
        capture_output=True,
        check=True,
    )
    tracked_paths = completed.stdout.decode().split("\0")
    return {
        relative_path: (
            path.read_bytes()
            if (path := repository_root / relative_path).is_file()
            else None
        )
        for relative_path in tracked_paths
        if relative_path
    }


def test_real_familyos_package_build_isolated_from_checkout(tmp_path: Path) -> None:
    repository_root = Path(__file__).resolve().parents[3]
    tracked_before = _tracked_snapshot(repository_root)

    project_root = tmp_path / "familyos-project"
    package_root = project_root / "src" / "familyos_cli"
    package_root.parent.mkdir(parents=True)
    shutil.copy2(repository_root / "pyproject.toml", project_root)
    shutil.copy2(repository_root / "README.md", project_root)
    shutil.copy2(repository_root / "LICENSE", project_root)
    shutil.copytree(
        repository_root / "src" / "familyos_cli",
        package_root,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )
    assert not (project_root / ".git").exists()
    assert not (project_root / "src" / "familyos_cli.egg-info").exists()

    output_dir = tmp_path / "package-output"
    result = RunPackageBuildUseCase(
        builder=PythonPackageBuilder(sys.executable),
        discoverer=DiscoverPackageArtifactsUseCase(),
        validator=ValidatePythonPackageArtifactsUseCase(project_root),
        project_root=project_root,
    ).execute(output_dir)

    wheels = tuple(
        artifact
        for artifact in result.candidates
        if artifact.artifact_class is ArtifactClass.PYTHON_WHEEL
    )
    sdists = tuple(
        artifact
        for artifact in result.candidates
        if artifact.artifact_class is ArtifactClass.SOURCE_DISTRIBUTION
    )
    assert result.status is PackageBuildStatus.SUCCEEDED, result.diagnostic
    assert result.execution.exit_code == 0
    assert result.discovery is not None
    assert result.discovery.successful
    assert result.validation is not None
    assert result.validation.status is PackageStructuralValidationStatus.VALID
    assert result.validation.diagnostic is None
    assert len(wheels) == 1
    assert len(sdists) == 1
    assert all(artifact.path.parent == output_dir for artifact in result.candidates)
    assert all(artifact.path.is_file() for artifact in result.candidates)
    expected_package_files = {
        path.relative_to(package_root.parent).as_posix()
        for path in package_root.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix not in {".pyc", ".pyo"}
    }
    (wheel,) = wheels
    with zipfile.ZipFile(wheel.path) as wheel_archive:
        wheel_package_files = {
            name
            for name in wheel_archive.namelist()
            if name.startswith("familyos_cli/") and not name.endswith("/")
        }
    assert wheel_package_files == expected_package_files

    (sdist,) = sdists
    with tarfile.open(sdist.path, mode="r:gz") as sdist_archive:
        sdist_package_files = {
            "/".join(member.name.split("/")[2:])
            for member in sdist_archive.getmembers()
            if member.isfile() and "/src/familyos_cli/" in member.name
        }
    assert sdist_package_files == expected_package_files
    assert any(path.endswith("plugin.yaml") for path in expected_package_files)
    assert any(path.endswith(".j2") for path in expected_package_files)
    assert _tracked_snapshot(repository_root) == tracked_before

    ignored_egg_info = subprocess.run(
        (
            "git",
            "check-ignore",
            "--no-index",
            "src/familyos_cli.egg-info/PKG-INFO",
        ),
        cwd=repository_root,
        capture_output=True,
        check=False,
        text=True,
    )
    assert ignored_egg_info.returncode == 0
