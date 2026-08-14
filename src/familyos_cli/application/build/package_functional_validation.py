"""Immutable results for installed Python wheel functional validation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from familyos_cli.application.build.artifact_discovery import DiscoveredArtifact


class PackageFunctionalValidationStatus(StrEnum):
    """Functional outcome for an unchanged discovered wheel candidate."""

    VALID = "valid"
    INVALID = "invalid"


class WheelFunctionalValidationStage(StrEnum):
    """Mandatory clean-environment wheel validation stages."""

    INSTALLATION = "wheel installation"
    IMPORT_SMOKE = "installed import smoke"
    CLI_SMOKE = "installed CLI smoke"


@dataclass(frozen=True, slots=True)
class WheelFunctionalValidationFinding:
    """One stage-specific functional failure diagnostic."""

    stage: WheelFunctionalValidationStage
    diagnostic: str


@dataclass(frozen=True, slots=True)
class PythonWheelFunctionalValidationResult:
    """Functional result without identity, integrity, or trust meaning."""

    candidate: DiscoveredArtifact
    status: PackageFunctionalValidationStatus
    findings: tuple[WheelFunctionalValidationFinding, ...] = ()
    environment_root: Path | None = None
    imported_module_path: Path | None = None

    @property
    def successful(self) -> bool:
        """Return whether every mandatory functional stage succeeded."""

        return self.status is PackageFunctionalValidationStatus.VALID

    @property
    def diagnostic(self) -> str | None:
        """Render deterministic stage-specific failure diagnostics."""

        if not self.findings:
            return None
        findings = "; ".join(
            f"{finding.stage.value}: {finding.diagnostic}" for finding in self.findings
        )
        return (
            "Python wheel functional validation failed: "
            f"{self.candidate.artifact_class.value} "
            f"{self.candidate.path.name}: {findings}"
        )
