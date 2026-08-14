"""Git-backed source-state observation for canonical package builds."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from familyos_cli.application.build.source_state import SourceState
from familyos_cli.application.ports.build.source_state_provider import (
    SourceStateProviderPort,
)


@dataclass(frozen=True, slots=True)
class GitSourceStateProvider(SourceStateProviderPort):
    """Observe Git state only when the project root is the exact repository root."""

    git_executable: str = "git"

    def observe(self, *, project_root: Path) -> SourceState:
        """Return revision and dirty state for the exact Git repository root."""

        resolved_project_root = project_root.resolve()

        repository_root = self._repository_root(resolved_project_root)
        if repository_root is None or repository_root != resolved_project_root:
            return SourceState(revision=None, dirty=None)

        revision = self._revision(resolved_project_root)
        dirty = self._dirty(resolved_project_root)

        return SourceState(
            revision=revision,
            dirty=dirty,
        )

    def _repository_root(self, project_root: Path) -> Path | None:
        completed = self._run(
            ("rev-parse", "--show-toplevel"),
            project_root=project_root,
        )
        if completed is None or completed.returncode != 0:
            return None

        repository_root = completed.stdout.strip()
        if not repository_root:
            return None

        try:
            return Path(repository_root).resolve()
        except OSError:
            return None

    def _revision(self, project_root: Path) -> str | None:
        completed = self._run(
            ("rev-parse", "--verify", "HEAD^{commit}"),
            project_root=project_root,
        )
        if completed is None or completed.returncode != 0:
            return None

        revision = completed.stdout.strip()
        return revision or None

    def _dirty(self, project_root: Path) -> bool | None:
        completed = self._run(
            ("status", "--porcelain=v1", "-z", "--untracked-files=all"),
            project_root=project_root,
        )
        if completed is None or completed.returncode != 0:
            return None

        return bool(completed.stdout)

    def _run(
        self,
        arguments: tuple[str, ...],
        *,
        project_root: Path,
    ) -> subprocess.CompletedProcess[str] | None:
        try:
            return subprocess.run(
                (self.git_executable, *arguments),
                cwd=project_root,
                capture_output=True,
                check=False,
                text=True,
            )
        except (OSError, subprocess.SubprocessError):
            return None
