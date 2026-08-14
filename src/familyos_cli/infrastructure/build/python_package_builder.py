"""Subprocess-backed adapter for the standard Python build frontend."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from familyos_cli.application.build import PackageBuildResult, PackageBuildStatus
from familyos_cli.application.ports.build import PackageBuilderPort

_MAX_DIAGNOSTIC_CHARACTERS = 2000


@dataclass(frozen=True, slots=True)
class PythonPackageBuilder(PackageBuilderPort):
    """Invoke ``python -m build`` without shell interpretation."""

    python_executable: str = sys.executable

    def build(
        self,
        *,
        project_root: Path,
        output_dir: Path,
    ) -> PackageBuildResult:
        """Build wheel and sdist into the supplied directory."""

        previous_outputs = self._snapshot_outputs(output_dir)
        command = (
            self.python_executable,
            "-m",
            "build",
            "--outdir",
            str(output_dir),
        )
        try:
            completed = subprocess.run(
                command,
                cwd=project_root,
                capture_output=True,
                check=False,
                text=True,
            )
        except Exception as error:  # noqa: BLE001 - infrastructure boundary
            return PackageBuildResult(
                status=PackageBuildStatus.ERROR,
                diagnostic=self._normalize_diagnostic(str(error), project_root),
            )

        if completed.returncode != 0:
            diagnostic = completed.stderr.strip() or completed.stdout.strip()
            return PackageBuildResult(
                status=PackageBuildStatus.FAILED,
                exit_code=completed.returncode,
                diagnostic=self._normalize_diagnostic(diagnostic, project_root),
            )

        current_outputs = self._snapshot_outputs(output_dir)
        outputs = tuple(
            path
            for path, state in current_outputs.items()
            if previous_outputs.get(path) != state
        )
        return PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
            outputs=outputs,
            exit_code=0,
        )

    def _normalize_diagnostic(self, diagnostic: str, project_root: Path) -> str:
        """Remove repository-specific paths and bound diagnostic size."""

        normalized = diagnostic.replace(str(project_root), ".").strip()
        if not normalized:
            return "Package build failed without diagnostic output."
        return normalized[-_MAX_DIAGNOSTIC_CHARACTERS:]

    def _snapshot_outputs(
        self,
        output_dir: Path,
    ) -> dict[Path, tuple[int, int, bytes]]:
        """Capture package-output state in deterministic path order."""

        if not output_dir.is_dir():
            return {}
        direct_file_outputs = sorted(
            (
                path
                for path in output_dir.iterdir()
                if path.is_file()
            ),
            key=lambda path: path.name,
        )
        return {
            path: (
                path.stat().st_mtime_ns,
                path.stat().st_size,
                self._content_fingerprint(path),
            )
            for path in direct_file_outputs
        }

    def _content_fingerprint(self, path: Path) -> bytes:
        """Fingerprint raw output privately for reliable change observation."""

        with path.open("rb") as output_file:
            return hashlib.file_digest(output_file, "sha256").digest()
