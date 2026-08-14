"""Real isolated integration coverage for canonical Python packaging."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

import pytest

from familyos_cli.application.build import (
    ArtifactClass,
    DiscoveredArtifact,
    DiscoverPackageArtifactsUseCase,
    PackageBuildStatus,
    PackageFunctionalValidationStatus,
    PackageStructuralValidationStatus,
    RunPackageBuildUseCase,
    ValidatePythonPackageArtifactsUseCase,
    WheelFunctionalValidationStage,
)
from familyos_cli.infrastructure.build import (
    GitSourceStateProvider,
    PythonPackageBuilder,
    PythonWheelFunctionalValidator,
)

_CONSTRAINED_BACKEND_PACKAGING_VERSION = "24.2"


def _copy_familyos_project(repository_root: Path, project_root: Path) -> Path:
    package_root = project_root / "src" / "familyos_cli"
    package_root.parent.mkdir(parents=True)
    for filename in ("pyproject.toml", "README.md", "LICENSE", "requirements.txt"):
        shutil.copy2(repository_root / filename, project_root)
    shutil.copytree(
        repository_root / "src" / "familyos_cli",
        package_root,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )
    return package_root


def _configure_backend_version_probe(project_root: Path) -> None:
    pyproject_path = project_root / "pyproject.toml"
    pyproject_content = pyproject_path.read_text(encoding="utf-8")
    build_requirements = 'requires = [\n    "setuptools>=75",'
    assert build_requirements in pyproject_content
    pyproject_path.write_text(
        pyproject_content.replace(
            build_requirements,
            'requires = [\n    "packaging>=24",\n    "setuptools>=75",',
            1,
        ),
        encoding="utf-8",
    )

    requirements_path = project_root / "requirements.txt"
    requirements_content = requirements_path.read_text(encoding="utf-8")
    packaging_pins = tuple(
        line
        for line in requirements_content.splitlines()
        if line.startswith("packaging==")
    )
    assert len(packaging_pins) == 1
    requirements_path.write_text(
        requirements_content.replace(
            f"{packaging_pins[0]}\n",
            f"packaging=={_CONSTRAINED_BACKEND_PACKAGING_VERSION}\n",
            1,
        ),
        encoding="utf-8",
    )

    (project_root / "setup.py").write_text(
        "from importlib.metadata import version\n"
        "from pathlib import Path\n"
        "from setuptools import setup\n"
        "Path('src/familyos_cli/py.typed').write_text(\n"
        "    version('packaging'), encoding='utf-8'\n"
        ")\n"
        "setup()\n",
        encoding="utf-8",
    )


def _backend_version_markers(output_dir: Path) -> tuple[str, str]:
    sdist_path = output_dir / "familyos_cli-0.1.0.tar.gz"
    wheel_path = output_dir / "familyos_cli-0.1.0-py3-none-any.whl"
    with tarfile.open(sdist_path, mode="r:gz") as sdist_archive:
        marker = sdist_archive.extractfile(
            "familyos_cli-0.1.0/src/familyos_cli/py.typed"
        )
        assert marker is not None
        sdist_version = marker.read().decode()
    with zipfile.ZipFile(wheel_path) as wheel_archive:
        wheel_version = wheel_archive.read("familyos_cli/py.typed").decode()
    return sdist_version, wheel_version


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


def _write_broken_console_entry_point_wheel(source: Path, destination: Path) -> None:
    entry_points_path: str | None = None
    with zipfile.ZipFile(source, mode="r") as source_archive:
        for name in source_archive.namelist():
            if name.endswith(".dist-info/entry_points.txt"):
                entry_points_path = name
                break
        assert entry_points_path is not None
        with zipfile.ZipFile(destination, mode="w") as destination_archive:
            for member in source_archive.infolist():
                content = source_archive.read(member)
                if member.filename == entry_points_path:
                    content = (
                        b"[console_scripts]\n"
                        b"familyos = familyos_cli.missing_entry_point:app\n"
                    )
                elif member.filename.endswith(".dist-info/RECORD"):
                    record_lines = content.decode().splitlines()
                    content = (
                        "\n".join(
                            (
                                f"{entry_points_path},,"
                                if line.startswith(f"{entry_points_path},")
                                else line
                            )
                            for line in record_lines
                        )
                        + "\n"
                    ).encode()
                destination_archive.writestr(member, content)


def test_real_familyos_package_build_isolated_from_checkout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository_root = Path(__file__).resolve().parents[3]
    tracked_before = _tracked_snapshot(repository_root)

    project_root = tmp_path / "familyos-project"
    package_root = _copy_familyos_project(repository_root, project_root)
    assert not (project_root / ".git").exists()
    assert not (project_root / "src" / "familyos_cli.egg-info").exists()
    caller_cwd = tmp_path / "external-caller"
    caller_cwd.mkdir()
    monkeypatch.chdir(caller_cwd)

    output_dir = tmp_path / "package-output"
    functional_validator = PythonWheelFunctionalValidator(
        project_root=project_root,
        requirements_lock=project_root / "requirements.txt",
        python_executable=sys.executable,
    )
    result = RunPackageBuildUseCase(
        builder=PythonPackageBuilder(sys.executable),
        discoverer=DiscoverPackageArtifactsUseCase(),
        validator=ValidatePythonPackageArtifactsUseCase(project_root),
        functional_validator=functional_validator,
        source_state_provider=GitSourceStateProvider(),
        project_root=project_root,
    ).execute(output_dir, validate_functionally=True)

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
    assert result.source_state.revision is None
    assert result.source_state.dirty is None
    assert result.execution.exit_code == 0
    assert result.discovery is not None
    assert result.discovery.successful
    assert result.validation is not None
    assert result.validation.status is PackageStructuralValidationStatus.VALID
    assert result.validation.diagnostic is None
    assert result.functional_validation is not None
    assert (
        result.functional_validation.status is PackageFunctionalValidationStatus.VALID
    )
    assert result.functional_validation.diagnostic is None
    assert result.functional_validation.environment_root is not None
    assert result.functional_validation.imported_module_path is not None
    assert result.functional_validation.imported_module_path.is_relative_to(
        result.functional_validation.environment_root
    )
    assert not result.functional_validation.imported_module_path.is_relative_to(
        project_root / "src"
    )
    assert not result.functional_validation.environment_root.exists()
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

    broken_wheel_directory = tmp_path / "broken-wheel"
    broken_wheel_directory.mkdir()
    broken_wheel_path = broken_wheel_directory / wheel.path.name
    _write_broken_console_entry_point_wheel(wheel.path, broken_wheel_path)
    broken_candidate = DiscoveredArtifact(
        broken_wheel_path,
        ArtifactClass.PYTHON_WHEEL,
    )
    broken_structural_result = ValidatePythonPackageArtifactsUseCase(
        project_root
    ).execute((broken_candidate,))
    assert broken_structural_result.status is PackageStructuralValidationStatus.VALID, (
        broken_structural_result.diagnostic
    )

    broken_functional_result = functional_validator.validate(broken_candidate)

    assert broken_functional_result.status is PackageFunctionalValidationStatus.INVALID
    assert (
        broken_functional_result.findings[0].stage
        is WheelFunctionalValidationStage.CLI_SMOKE
    )
    assert broken_functional_result.diagnostic is not None
    assert "installed CLI smoke" in broken_functional_result.diagnostic
    assert "missing_entry_point" in broken_functional_result.diagnostic
    assert broken_functional_result.environment_root is not None
    assert not broken_functional_result.environment_root.exists()
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


def test_canonical_build_depends_on_the_generated_sdist(tmp_path: Path) -> None:
    repository_root = Path(__file__).resolve().parents[3]
    direct_project = tmp_path / "direct-wheel-project"
    canonical_project = tmp_path / "canonical-project"
    for project_root in (direct_project, canonical_project):
        _copy_familyos_project(repository_root, project_root)
        (project_root / "MANIFEST.in").write_text(
            "exclude src/familyos_cli/__init__.py\n",
            encoding="utf-8",
        )
        (project_root / "setup.py").write_text(
            "from pathlib import Path\n"
            "from setuptools import setup\n"
            "if not Path('src/familyos_cli/__init__.py').is_file():\n"
            "    raise RuntimeError('sdist package marker is unavailable')\n"
            "setup()\n",
            encoding="utf-8",
        )

    direct_output = tmp_path / "direct-wheel-output"
    direct_build = subprocess.run(
        (
            sys.executable,
            "-m",
            "build",
            "--wheel",
            "--outdir",
            str(direct_output),
        ),
        cwd=direct_project,
        capture_output=True,
        check=False,
        text=True,
    )

    assert direct_build.returncode == 0, direct_build.stderr
    direct_wheel = direct_output / "familyos_cli-0.1.0-py3-none-any.whl"
    assert direct_wheel.is_file()
    with zipfile.ZipFile(direct_wheel) as direct_wheel_archive:
        assert "familyos_cli/__init__.py" in direct_wheel_archive.namelist()

    canonical_output = tmp_path / "canonical-output"
    canonical_result = PythonPackageBuilder(sys.executable).build(
        project_root=canonical_project,
        output_dir=canonical_output,
    )

    assert canonical_result.status is PackageBuildStatus.FAILED
    assert canonical_result.exit_code is not None
    assert canonical_result.exit_code != 0
    assert canonical_result.diagnostic is not None
    assert "sdist package marker is unavailable" in canonical_result.diagnostic
    assert not (canonical_output / direct_wheel.name).exists()

    sdist = canonical_output / "familyos_cli-0.1.0.tar.gz"
    assert sdist.is_file()
    with tarfile.open(sdist, mode="r:gz") as sdist_archive:
        member_names = set(sdist_archive.getnames())
    assert not any(
        name.endswith("/src/familyos_cli/__init__.py") for name in member_names
    )

    static_result = ValidatePythonPackageArtifactsUseCase(canonical_project).execute(
        (DiscoveredArtifact(sdist, ArtifactClass.SOURCE_DISTRIBUTION),)
    )
    assert static_result.status is PackageStructuralValidationStatus.INVALID
    assert static_result.diagnostic is not None
    assert "missing expected Python module 'familyos_cli/__init__.py'" in (
        static_result.diagnostic
    )


def test_backend_dependency_constraints_apply_to_both_isolated_builds(
    tmp_path: Path,
) -> None:
    repository_root = Path(__file__).resolve().parents[3]
    unconstrained_project = tmp_path / "unconstrained-project"
    constrained_project = tmp_path / "constrained-project"
    for project_root in (unconstrained_project, constrained_project):
        _copy_familyos_project(repository_root, project_root)
        _configure_backend_version_probe(project_root)

    unconstrained_output = tmp_path / "unconstrained-output"
    unconstrained_build = subprocess.run(
        (
            sys.executable,
            "-m",
            "build",
            "--outdir",
            str(unconstrained_output),
        ),
        cwd=unconstrained_project,
        capture_output=True,
        check=False,
        text=True,
    )
    assert unconstrained_build.returncode == 0, unconstrained_build.stderr
    unconstrained_sdist, unconstrained_wheel = _backend_version_markers(
        unconstrained_output
    )
    assert unconstrained_sdist != _CONSTRAINED_BACKEND_PACKAGING_VERSION
    assert unconstrained_wheel != _CONSTRAINED_BACKEND_PACKAGING_VERSION

    constrained_output = tmp_path / "constrained-output"
    constrained_result = PythonPackageBuilder(sys.executable).build(
        project_root=constrained_project,
        output_dir=constrained_output,
    )
    assert constrained_result.status is PackageBuildStatus.SUCCEEDED, (
        constrained_result.diagnostic
    )
    constrained_sdist, constrained_wheel = _backend_version_markers(
        constrained_output
    )
    assert constrained_sdist == _CONSTRAINED_BACKEND_PACKAGING_VERSION
    assert constrained_wheel == _CONSTRAINED_BACKEND_PACKAGING_VERSION
