"""Temporary-venv adapter for Python wheel functional validation."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from familyos_cli.application.build.artifact_discovery import (
    ArtifactClass,
    DiscoveredArtifact,
)
from familyos_cli.application.build.package_functional_validation import (
    PackageFunctionalValidationStatus,
    PythonWheelFunctionalValidationResult,
    WheelFunctionalValidationFinding,
    WheelFunctionalValidationStage,
)
from familyos_cli.application.ports.build.python_wheel_functional_validator import (
    PythonWheelFunctionalValidatorPort,
)

_MAX_DIAGNOSTIC_CHARACTERS = 2000
_ENVIRONMENT_CREATION_TIMEOUT_SECONDS = 120
_INSTALLATION_TIMEOUT_SECONDS = 300
_SMOKE_TIMEOUT_SECONDS = 60
_IMPORT_TARGET = "familyos_cli.main"
_CLI_HELP_TEXT = "FamilyOS CLI"
_IMPORT_PROBE = (
    "import json\n"
    "from pathlib import Path\n"
    f"import {_IMPORT_TARGET} as target\n"
    "print(json.dumps({'module_path': str(Path(target.__file__).resolve())}))\n"
)


@dataclass(frozen=True, slots=True)
class _CommandOutcome:
    completed: subprocess.CompletedProcess[str] | None
    diagnostic: str | None = None


@dataclass(frozen=True, slots=True)
class PythonWheelFunctionalValidator(PythonWheelFunctionalValidatorPort):
    """Install one discovered wheel and smoke-test its installed interfaces."""

    project_root: Path
    requirements_lock: Path
    python_executable: str = sys.executable

    def validate(
        self,
        candidate: DiscoveredArtifact,
    ) -> PythonWheelFunctionalValidationResult:
        """Validate the exact candidate in a fresh, cleaned temporary venv."""

        if candidate.artifact_class is not ArtifactClass.PYTHON_WHEEL:
            return self._invalid(
                candidate,
                WheelFunctionalValidationStage.INSTALLATION,
                "candidate is not a Python wheel",
            )
        if not candidate.path.is_file():
            return self._invalid(
                candidate,
                WheelFunctionalValidationStage.INSTALLATION,
                "wheel candidate does not exist as a regular file",
            )
        if not self.requirements_lock.is_file():
            return self._invalid(
                candidate,
                WheelFunctionalValidationStage.INSTALLATION,
                "committed dependency constraints are unavailable",
            )

        try:
            with tempfile.TemporaryDirectory(
                prefix="familyos-wheel-functional-"
            ) as temporary_directory:
                return self._validate_in_temporary_environment(
                    candidate,
                    Path(temporary_directory).resolve(),
                )
        except OSError as error:
            return self._invalid(
                candidate,
                WheelFunctionalValidationStage.INSTALLATION,
                self._normalize_diagnostic(str(error), None, candidate),
            )

    def _validate_in_temporary_environment(
        self,
        candidate: DiscoveredArtifact,
        temporary_root: Path,
    ) -> PythonWheelFunctionalValidationResult:
        project_root = self.project_root.resolve()
        if temporary_root.is_relative_to(project_root):
            return self._invalid(
                candidate,
                WheelFunctionalValidationStage.INSTALLATION,
                "temporary environment resolved inside the repository checkout",
                environment_root=temporary_root,
            )

        environment_root = temporary_root / "venv"
        working_directory = temporary_root / "smoke-workdir"
        working_directory.mkdir()
        environment = self._sanitized_environment()

        creation = self._run_command(
            (
                self.python_executable,
                "-m",
                "venv",
                str(environment_root),
            ),
            cwd=working_directory,
            environment=environment,
            timeout_seconds=_ENVIRONMENT_CREATION_TIMEOUT_SECONDS,
            temporary_root=temporary_root,
            candidate=candidate,
        )
        creation_failure = self._command_failure(creation)
        if creation_failure is not None:
            return self._invalid(
                candidate,
                WheelFunctionalValidationStage.INSTALLATION,
                f"clean environment creation failed: {creation_failure}",
                environment_root=environment_root,
            )

        scripts_directory = environment_root / ("Scripts" if os.name == "nt" else "bin")
        environment_python = scripts_directory / (
            "python.exe" if os.name == "nt" else "python"
        )
        familyos_executable = scripts_directory / (
            "familyos.exe" if os.name == "nt" else "familyos"
        )
        installation = self._run_command(
            (
                str(environment_python),
                "-m",
                "pip",
                "--isolated",
                "--disable-pip-version-check",
                "--no-input",
                "--require-virtualenv",
                "install",
                "--only-binary=:all:",
                "--constraint",
                str(self.requirements_lock.resolve()),
                str(candidate.path.resolve()),
            ),
            cwd=working_directory,
            environment=environment,
            timeout_seconds=_INSTALLATION_TIMEOUT_SECONDS,
            temporary_root=temporary_root,
            candidate=candidate,
        )
        installation_failure = self._command_failure(installation)
        if installation_failure is not None:
            return self._invalid(
                candidate,
                WheelFunctionalValidationStage.INSTALLATION,
                installation_failure,
                environment_root=environment_root,
            )

        import_smoke = self._run_command(
            (str(environment_python), "-I", "-c", _IMPORT_PROBE),
            cwd=working_directory,
            environment=environment,
            timeout_seconds=_SMOKE_TIMEOUT_SECONDS,
            temporary_root=temporary_root,
            candidate=candidate,
        )
        import_failure = self._command_failure(import_smoke)
        if import_failure is not None:
            return self._invalid(
                candidate,
                WheelFunctionalValidationStage.IMPORT_SMOKE,
                import_failure,
                environment_root=environment_root,
            )
        imported_module_path = self._imported_module_path(import_smoke)
        if imported_module_path is None:
            return self._invalid(
                candidate,
                WheelFunctionalValidationStage.IMPORT_SMOKE,
                "import probe did not return a valid module path",
                environment_root=environment_root,
            )
        if not imported_module_path.is_relative_to(
            environment_root
        ) or imported_module_path.is_relative_to(project_root / "src"):
            return self._invalid(
                candidate,
                WheelFunctionalValidationStage.IMPORT_SMOKE,
                "FamilyOS resolved outside the clean temporary environment",
                environment_root=environment_root,
                imported_module_path=imported_module_path,
            )

        cli_smoke = self._run_command(
            (str(familyos_executable), "--help"),
            cwd=working_directory,
            environment=environment,
            timeout_seconds=_SMOKE_TIMEOUT_SECONDS,
            temporary_root=temporary_root,
            candidate=candidate,
        )
        cli_failure = self._command_failure(cli_smoke)
        if cli_failure is not None:
            return self._invalid(
                candidate,
                WheelFunctionalValidationStage.CLI_SMOKE,
                cli_failure,
                environment_root=environment_root,
                imported_module_path=imported_module_path,
            )
        assert cli_smoke.completed is not None
        if _CLI_HELP_TEXT not in cli_smoke.completed.stdout:
            return self._invalid(
                candidate,
                WheelFunctionalValidationStage.CLI_SMOKE,
                "installed familyos --help omitted the canonical CLI help text",
                environment_root=environment_root,
                imported_module_path=imported_module_path,
            )

        return PythonWheelFunctionalValidationResult(
            candidate=candidate,
            status=PackageFunctionalValidationStatus.VALID,
            environment_root=environment_root,
            imported_module_path=imported_module_path,
        )

    def _run_command(
        self,
        command: tuple[str, ...],
        *,
        cwd: Path,
        environment: dict[str, str],
        timeout_seconds: int,
        temporary_root: Path,
        candidate: DiscoveredArtifact,
    ) -> _CommandOutcome:
        try:
            completed = subprocess.run(
                command,
                cwd=cwd,
                env=environment,
                capture_output=True,
                check=False,
                text=True,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            return _CommandOutcome(
                completed=None,
                diagnostic=f"command exceeded {timeout_seconds}-second limit",
            )
        except Exception as error:  # noqa: BLE001 - infrastructure boundary
            return _CommandOutcome(
                completed=None,
                diagnostic=self._normalize_diagnostic(
                    str(error), temporary_root, candidate
                ),
            )
        if completed.returncode == 0:
            return _CommandOutcome(completed=completed)
        diagnostic = completed.stderr.strip() or completed.stdout.strip()
        return _CommandOutcome(
            completed=completed,
            diagnostic=self._normalize_diagnostic(
                diagnostic or "command failed without diagnostic output",
                temporary_root,
                candidate,
            ),
        )

    def _command_failure(self, outcome: _CommandOutcome) -> str | None:
        return outcome.diagnostic

    def _imported_module_path(self, outcome: _CommandOutcome) -> Path | None:
        if outcome.completed is None:
            return None
        try:
            payload = json.loads(outcome.completed.stdout.strip())
        except json.JSONDecodeError:
            return None
        module_path = payload.get("module_path") if isinstance(payload, dict) else None
        if not isinstance(module_path, str) or not module_path:
            return None
        return Path(module_path).resolve()

    def _sanitized_environment(self) -> dict[str, str]:
        environment = dict(os.environ)
        for name in (
            "PYTHONHOME",
            "PYTHONPATH",
            "PYTHONSTARTUP",
            "PYTHONUSERBASE",
            "VIRTUAL_ENV",
            "__PYVENV_LAUNCHER__",
        ):
            environment.pop(name, None)
        environment["PYTHONNOUSERSITE"] = "1"
        return environment

    def _normalize_diagnostic(
        self,
        diagnostic: str,
        temporary_root: Path | None,
        candidate: DiscoveredArtifact,
    ) -> str:
        normalized = diagnostic.replace(
            str(candidate.path.resolve()), candidate.path.name
        )
        normalized = normalized.replace(str(self.project_root.resolve()), ".")
        if temporary_root is not None:
            normalized = normalized.replace(
                str(temporary_root), "<temporary-environment>"
            )
        normalized = normalized.strip()
        return (normalized or "execution failed without diagnostic output")[
            -_MAX_DIAGNOSTIC_CHARACTERS:
        ]

    def _invalid(
        self,
        candidate: DiscoveredArtifact,
        stage: WheelFunctionalValidationStage,
        diagnostic: str,
        *,
        environment_root: Path | None = None,
        imported_module_path: Path | None = None,
    ) -> PythonWheelFunctionalValidationResult:
        return PythonWheelFunctionalValidationResult(
            candidate=candidate,
            status=PackageFunctionalValidationStatus.INVALID,
            findings=(WheelFunctionalValidationFinding(stage, diagnostic),),
            environment_root=environment_root,
            imported_module_path=imported_module_path,
        )
