"""Tests for canonical package-build input staging."""

from __future__ import annotations

from pathlib import Path

import pytest

from familyos_cli.application.build.build_input_stager import BuildInputStager
from familyos_cli.application.build.build_workspace import BuildWorkspace


def _workspace(tmp_path: Path) -> BuildWorkspace:
    root = tmp_path.resolve() / "workspace"
    staging = root / "staging"
    intermediate = root / "intermediate"
    staging.mkdir(parents=True)
    intermediate.mkdir()

    return BuildWorkspace(
        root=root,
        staging_dir=staging,
        intermediate_dir=intermediate,
    )


def _project(tmp_path: Path) -> Path:
    root = tmp_path / "authoritative"
    package = root / "src" / "familyos_cli"
    package.mkdir(parents=True)

    for filename in (
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "requirements.txt",
    ):
        (root / filename).write_text(
            f"{filename}\n",
            encoding="utf-8",
        )

    (package / "__init__.py").write_text(
        "VALUE = 1\n",
        encoding="utf-8",
    )
    (package / "py.typed").write_text("", encoding="utf-8")

    templates = package / "plugins" / "builtin" / "sample" / "templates"
    templates.mkdir(parents=True)
    (templates.parent / "plugin.yaml").write_text(
        "id: sample\n",
        encoding="utf-8",
    )
    (templates / "sample.md.j2").write_text(
        "{{ value }}\n",
        encoding="utf-8",
    )

    return root


def test_stager_materializes_canonical_package_inputs(
    tmp_path: Path,
) -> None:
    project_root = _project(tmp_path)
    workspace = _workspace(tmp_path)

    result = BuildInputStager().stage(
        project_root=project_root,
        workspace=workspace,
    )

    staged = result.project_root

    assert staged == (workspace.staging_dir / "project").resolve()

    for filename in (
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "requirements.txt",
    ):
        assert (staged / filename).read_bytes() == (
            project_root / filename
        ).read_bytes()

    assert (
        staged / "src" / "familyos_cli" / "__init__.py"
    ).read_text(encoding="utf-8") == "VALUE = 1\n"

    assert (
        staged
        / "src"
        / "familyos_cli"
        / "plugins"
        / "builtin"
        / "sample"
        / "plugin.yaml"
    ).is_file()

    assert (
        staged
        / "src"
        / "familyos_cli"
        / "plugins"
        / "builtin"
        / "sample"
        / "templates"
        / "sample.md.j2"
    ).is_file()


def test_stager_excludes_python_cache_state(
    tmp_path: Path,
) -> None:
    project_root = _project(tmp_path)
    cache = project_root / "src" / "familyos_cli" / "__pycache__"
    cache.mkdir()
    (cache / "module.cpython-313.pyc").write_bytes(b"cache")

    workspace = _workspace(tmp_path)

    result = BuildInputStager().stage(
        project_root=project_root,
        workspace=workspace,
    )

    assert not (
        result.project_root
        / "src"
        / "familyos_cli"
        / "__pycache__"
    ).exists()


def test_stager_does_not_copy_unrelated_repository_state(
    tmp_path: Path,
) -> None:
    project_root = _project(tmp_path)
    (project_root / ".git").mkdir()
    (project_root / "docs").mkdir()
    (project_root / "dist").mkdir()
    (project_root / "unrelated.txt").write_text(
        "not a build input",
        encoding="utf-8",
    )

    workspace = _workspace(tmp_path)

    result = BuildInputStager().stage(
        project_root=project_root,
        workspace=workspace,
    )

    assert not (result.project_root / ".git").exists()
    assert not (result.project_root / "docs").exists()
    assert not (result.project_root / "dist").exists()
    assert not (result.project_root / "unrelated.txt").exists()


def test_stager_rejects_existing_staged_project(
    tmp_path: Path,
) -> None:
    project_root = _project(tmp_path)
    workspace = _workspace(tmp_path)
    stager = BuildInputStager()

    stager.stage(
        project_root=project_root,
        workspace=workspace,
    )

    with pytest.raises(FileExistsError):
        stager.stage(
            project_root=project_root,
            workspace=workspace,
        )
