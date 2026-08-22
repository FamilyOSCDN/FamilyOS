"""Resolve canonical dependency state for build execution."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from familyos_cli.application.build.dependency_state import DependencyState


class DependencyStateProvider:
    """Capture immutable identity of canonical dependency inputs."""

    def capture(self, *, project_root: Path) -> DependencyState:
        """Capture canonical dependency declaration and lock identities."""

        declaration_path = (project_root / "pyproject.toml").resolve()
        lock_path = (project_root / "requirements.txt").resolve()

        if not declaration_path.is_file():
            raise ValueError(
                "canonical dependency declaration does not exist: "
                f"{declaration_path}"
            )

        if not lock_path.is_file():
            raise ValueError(
                "canonical dependency lock does not exist: "
                f"{lock_path}"
            )

        return DependencyState(
            declaration_path=declaration_path,
            declaration_digest=self._digest(declaration_path),
            lock_path=lock_path,
            lock_digest=self._digest(lock_path),
        )

    @staticmethod
    def _digest(path: Path) -> str:
        """Return SHA-256 over the exact committed dependency-input bytes."""

        digest = sha256()

        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)

        return digest.hexdigest()
