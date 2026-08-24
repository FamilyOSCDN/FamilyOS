"""Tests for the Git-backed Testing Framework source-state provider."""

from __future__ import annotations

import subprocess
from pathlib import Path

from familyos_cli.infrastructure.testing.git_testing_source_state_provider import (
    GitTestingSourceStateProvider,
)

from familyos_cli.application.ports.testing import (
    TestingSourceStateProviderPort,
)


def _git(
    repository: Path,
    *arguments: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ("git", *arguments),
        cwd=repository,
        capture_output=True,
        check=True,
        text=True,
    )


def _repository(tmp_path: Path) -> Path:
    repository = tmp_path / "repository"
    repository.mkdir()

    _git(repository, "init", "-q")
    _git(repository, "config", "user.email", "familyos@example.test")
    _git(repository, "config", "user.name", "FamilyOS Tests")

    tracked = repository / "tracked.txt"
    tracked.write_text("initial\n", encoding="utf-8")

    _git(repository, "add", "tracked.txt")
    _git(repository, "commit", "-q", "-m", "initial")

    return repository


def test_provider_implements_testing_source_state_port() -> None:
    assert isinstance(
        GitTestingSourceStateProvider(),
        TestingSourceStateProviderPort,
    )


def test_provider_captures_exact_repository_revision(
    tmp_path: Path,
) -> None:
    repository = _repository(tmp_path)

    expected_revision = _git(
        repository,
        "rev-parse",
        "--verify",
        "HEAD^{commit}",
    ).stdout.strip()

    state = GitTestingSourceStateProvider().observe(
        project_root=repository,
    )

    assert state.revision == expected_revision
    assert state.dirty is False


def test_provider_detects_dirty_repository(
    tmp_path: Path,
) -> None:
    repository = _repository(tmp_path)

    (repository / "tracked.txt").write_text(
        "modified\n",
        encoding="utf-8",
    )

    state = GitTestingSourceStateProvider().observe(
        project_root=repository,
    )

    assert state.revision is not None
    assert state.dirty is True


def test_provider_rejects_nested_directory_as_repository_authority(
    tmp_path: Path,
) -> None:
    repository = _repository(tmp_path)

    nested = repository / "nested"
    nested.mkdir()

    state = GitTestingSourceStateProvider().observe(
        project_root=nested,
    )

    assert state.revision is None
    assert state.dirty is None


def test_provider_returns_unavailable_state_outside_git_repository(
    tmp_path: Path,
) -> None:
    state = GitTestingSourceStateProvider().observe(
        project_root=tmp_path,
    )

    assert state.revision is None
    assert state.dirty is None
