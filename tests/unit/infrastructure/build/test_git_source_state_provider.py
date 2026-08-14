"""Behavioral tests for Git-backed source-state observation."""

from __future__ import annotations

import subprocess
from pathlib import Path

from familyos_cli.application.build import SourceState
from familyos_cli.infrastructure.build import GitSourceStateProvider


def _git(repository: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ("git", *arguments),
        cwd=repository,
        capture_output=True,
        check=True,
        text=True,
    )
    return completed.stdout.strip()


def _initialize_repository(repository: Path) -> None:
    repository.mkdir(parents=True)
    _git(repository, "init", "-q")
    _git(repository, "config", "user.email", "familyos@example.invalid")
    _git(repository, "config", "user.name", "FamilyOS Tests")


def _commit_file(repository: Path, relative_path: str = "tracked.txt") -> str:
    path = repository / relative_path
    path.write_text("initial\n", encoding="utf-8")
    _git(repository, "add", relative_path)
    _git(repository, "commit", "-q", "-m", "initial")
    return _git(repository, "rev-parse", "HEAD")


def test_observe_clean_repository_returns_exact_revision_and_clean_state(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    _initialize_repository(repository)
    revision = _commit_file(repository)

    result = GitSourceStateProvider().observe(project_root=repository)

    assert result == SourceState(
        revision=revision,
        dirty=False,
    )


def test_observe_unstaged_tracked_modification_is_dirty(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    _initialize_repository(repository)
    revision = _commit_file(repository)

    (repository / "tracked.txt").write_text("modified\n", encoding="utf-8")

    result = GitSourceStateProvider().observe(project_root=repository)

    assert result == SourceState(
        revision=revision,
        dirty=True,
    )


def test_observe_staged_modification_is_dirty(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    _initialize_repository(repository)
    revision = _commit_file(repository)

    (repository / "tracked.txt").write_text("modified\n", encoding="utf-8")
    _git(repository, "add", "tracked.txt")

    result = GitSourceStateProvider().observe(project_root=repository)

    assert result == SourceState(
        revision=revision,
        dirty=True,
    )


def test_observe_tracked_deletion_is_dirty(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    _initialize_repository(repository)
    revision = _commit_file(repository)

    (repository / "tracked.txt").unlink()

    result = GitSourceStateProvider().observe(project_root=repository)

    assert result == SourceState(
        revision=revision,
        dirty=True,
    )


def test_observe_untracked_file_is_dirty(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    _initialize_repository(repository)
    revision = _commit_file(repository)

    (repository / "untracked.txt").write_text("untracked\n", encoding="utf-8")

    result = GitSourceStateProvider().observe(project_root=repository)

    assert result == SourceState(
        revision=revision,
        dirty=True,
    )


def test_observe_ignored_generated_output_remains_clean(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    _initialize_repository(repository)

    (repository / ".gitignore").write_text(
        "dist/\n"
        "*.egg-info/\n"
        "__pycache__/\n"
        "*.pyc\n",
        encoding="utf-8",
    )
    (repository / "tracked.txt").write_text("initial\n", encoding="utf-8")
    _git(repository, "add", ".gitignore", "tracked.txt")
    _git(repository, "commit", "-q", "-m", "initial")
    revision = _git(repository, "rev-parse", "HEAD")

    dist = repository / "dist"
    dist.mkdir()
    (dist / "package.whl").write_text("generated\n", encoding="utf-8")

    egg_info = repository / "familyos.egg-info"
    egg_info.mkdir()
    (egg_info / "PKG-INFO").write_text("generated\n", encoding="utf-8")

    cache = repository / "__pycache__"
    cache.mkdir()
    (cache / "module.cpython-313.pyc").write_bytes(b"generated")

    result = GitSourceStateProvider().observe(project_root=repository)

    assert result == SourceState(
        revision=revision,
        dirty=False,
    )


def test_observe_detached_head_returns_same_commit(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    _initialize_repository(repository)
    revision = _commit_file(repository)

    _git(repository, "checkout", "-q", "--detach", revision)

    result = GitSourceStateProvider().observe(project_root=repository)

    assert result == SourceState(
        revision=revision,
        dirty=False,
    )


def test_observe_tagged_checkout_returns_same_commit(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    _initialize_repository(repository)
    revision = _commit_file(repository)

    _git(repository, "tag", "v-test")
    _git(repository, "checkout", "-q", "v-test")

    result = GitSourceStateProvider().observe(project_root=repository)

    assert result == SourceState(
        revision=revision,
        dirty=False,
    )


def test_observe_shallow_repository_captures_head_without_history(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    _initialize_repository(source)
    revision = _commit_file(source)

    clone = tmp_path / "clone"
    subprocess.run(
        (
            "git",
            "clone",
            "-q",
            "--depth",
            "1",
            source.as_uri(),
            str(clone),
        ),
        capture_output=True,
        check=True,
        text=True,
    )

    result = GitSourceStateProvider().observe(project_root=clone)

    assert result == SourceState(
        revision=revision,
        dirty=False,
    )


def test_observe_repository_without_initial_commit_preserves_dirty_state(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    _initialize_repository(repository)

    (repository / "untracked.txt").write_text("untracked\n", encoding="utf-8")

    result = GitSourceStateProvider().observe(project_root=repository)

    assert result == SourceState(
        revision=None,
        dirty=True,
    )


def test_observe_non_git_directory_returns_unknown_state(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    result = GitSourceStateProvider().observe(project_root=project_root)

    assert result == SourceState(
        revision=None,
        dirty=None,
    )


def test_observe_unavailable_git_executable_returns_unknown_state(
    tmp_path: Path,
) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()

    result = GitSourceStateProvider(
        git_executable="familyos-git-executable-does-not-exist",
    ).observe(project_root=project_root)

    assert result == SourceState(
        revision=None,
        dirty=None,
    )


def test_observe_nested_project_rejects_ancestor_repository(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    _initialize_repository(repository)
    _commit_file(repository)

    project_root = repository / "nested-project"
    project_root.mkdir()

    result = GitSourceStateProvider().observe(project_root=project_root)

    assert result == SourceState(
        revision=None,
        dirty=None,
    )
