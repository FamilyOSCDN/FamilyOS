"""Subprocess-backed adapter for the standard Python build frontend."""

from __future__ import annotations

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

    def _snapshot_outputs(self, output_dir: Path) -> dict[Path, tuple[int, int]]:
        """Capture package-output state in deterministic path order."""

        if not output_dir.is_dir():
            return {}
        package_outputs = sorted(
            (
                path
                for path in output_dir.iterdir()
                if path.is_file()
                and (path.suffix == ".whl" or path.name.endswith(".tar.gz"))
            ),
            key=lambda path: path.name,
        )
        return {
            path: (path.stat().st_mtime_ns, path.stat().st_size)
            for path in package_outputs
        }
