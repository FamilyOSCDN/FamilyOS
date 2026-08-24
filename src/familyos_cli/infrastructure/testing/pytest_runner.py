"""Subprocess-backed structured pytest runner."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from familyos_cli.application.ports.testing import PytestRunnerPort
from familyos_cli.application.testing import PytestExecutionResult

_RESULT_PLUGIN = (
    "familyos_cli.infrastructure.testing.pytest_result_plugin"
)


@dataclass(frozen=True, slots=True)
class PytestRunner(PytestRunnerPort):
    """Execute pytest in a subprocess with structured FamilyOS reporting."""

    python_executable: str = sys.executable

    def run(
        self,
        *,
        project_root: Path,
        test_paths: tuple[Path, ...],
    ) -> PytestExecutionResult:
        """Execute selected tests and return their structured pytest result."""

        resolved_root = project_root.resolve()

        resolved_paths = tuple(
            self._resolve_test_path(
                path,
                project_root=resolved_root,
            )
            for path in test_paths
        )

        with tempfile.TemporaryDirectory(
            prefix="familyos-pytest-"
        ) as temporary_directory:
            result_path = (
                Path(temporary_directory)
                / "pytest-result.json"
            )

            command = (
                self.python_executable,
                "-m",
                "pytest",
                "-q",
                "-p",
                _RESULT_PLUGIN,
                *tuple(str(path) for path in resolved_paths),
            )

            environment = {
                **dict(__import__("os").environ),
                "FAMILYOS_PYTEST_RESULT_PATH": str(result_path),
            }

            completed = subprocess.run(
                command,
                cwd=resolved_root,
                env=environment,
                capture_output=True,
                check=False,
                text=True,
            )

            if not result_path.is_file():
                return PytestExecutionResult(
                    exit_code=max(completed.returncode, 0),
                    discovered=0,
                    executed=0,
                    passed=0,
                    failed=0,
                    skipped=0,
                    errors=0,
                    duration_seconds=0.0,
                    diagnostic=self._diagnostic(completed),
                )

            payload = self._read_payload(result_path)

            return PytestExecutionResult(
                exit_code=int(payload["exit_code"]),
                discovered=int(payload["discovered"]),
                executed=int(payload["executed"]),
                passed=int(payload["passed"]),
                failed=int(payload["failed"]),
                skipped=int(payload["skipped"]),
                errors=int(payload["errors"]),
                duration_seconds=float(payload["duration_seconds"]),
                diagnostic=(
                    None
                    if completed.returncode == 0
                    else self._diagnostic(completed)
                ),
            )

    @staticmethod
    def _resolve_test_path(
        path: Path,
        *,
        project_root: Path,
    ) -> Path:
        resolved = (
            path.resolve()
            if path.is_absolute()
            else (project_root / path).resolve()
        )

        if not resolved.is_relative_to(project_root):
            raise ValueError(
                "test path must resolve inside project root"
            )

        return resolved

    @staticmethod
    def _read_payload(path: Path) -> dict[str, Any]:
        payload = json.loads(
            path.read_text(encoding="utf-8")
        )

        if not isinstance(payload, dict):
            raise ValueError(
                "pytest structured result must be an object"
            )

        return payload

    @staticmethod
    def _diagnostic(
        completed: subprocess.CompletedProcess[str],
    ) -> str | None:
        diagnostic = (
            completed.stderr.strip()
            or completed.stdout.strip()
        )

        return diagnostic or None
