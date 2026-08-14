"""Real isolated integration coverage for canonical Python packaging."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from familyos_cli.application.build import PackageBuildStatus
from familyos_cli.infrastructure.build import PythonPackageBuilder


def _snapshot(directory: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(directory)): path.read_bytes()
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


def test_real_familyos_package_build_isolated_from_checkout(tmp_path: Path) -> None:
    repository_root = Path(__file__).resolve().parents[3]
    tracked_egg_info = repository_root / "src" / "familyos_cli.egg-info"
    egg_info_before = _snapshot(tracked_egg_info)

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
    result = PythonPackageBuilder(sys.executable).build(
        project_root=project_root,
        output_dir=output_dir,
    )

    wheels = tuple(path for path in result.outputs if path.suffix == ".whl")
    sdists = tuple(path for path in result.outputs if path.name.endswith(".tar.gz"))
    assert result.status is PackageBuildStatus.SUCCEEDED, result.diagnostic
    assert result.exit_code == 0
    assert len(wheels) == 1
    assert len(sdists) == 1
    assert all(path.parent == output_dir for path in result.outputs)
    assert all(path.is_file() for path in result.outputs)
    assert _snapshot(tracked_egg_info) == egg_info_before
