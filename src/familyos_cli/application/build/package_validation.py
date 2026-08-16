"""Immutable results for Python package structural validation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from familyos_cli.application.build.artifact_discovery import DiscoveredArtifact
from familyos_cli.application.build.package_identity import PackageIdentity


class PackageStructuralValidationStatus(StrEnum):
    """Structural outcome for a discovered Python package candidate."""

    VALID = "valid"
    INVALID = "invalid"


@dataclass(frozen=True, slots=True)
class CandidatePackageValidationResult:
    """Structural findings for one unchanged discovered candidate."""

    candidate: DiscoveredArtifact
    status: PackageStructuralValidationStatus
    diagnostics: tuple[str, ...] = ()
    package_identity: PackageIdentity | None = None

    @property
    def successful(self) -> bool:
        """Return whether this candidate satisfied the structural contract."""

        return self.status is PackageStructuralValidationStatus.VALID


@dataclass(frozen=True, slots=True)
class PythonPackageStructuralValidationResult:
    """Aggregate structural result without integrity or trust meaning."""

    status: PackageStructuralValidationStatus
    candidate_results: tuple[CandidatePackageValidationResult, ...]

    @property
    def successful(self) -> bool:
        """Return whether every candidate satisfied the structural contract."""

        return self.status is PackageStructuralValidationStatus.VALID

    @property
    def diagnostic(self) -> str | None:
        """Render deterministic candidate-specific failure diagnostics."""

        findings = tuple(
            f"{result.candidate.artifact_class.value} "
            f"{result.candidate.path.name}: {diagnostic}"
            for result in self.candidate_results
            for diagnostic in result.diagnostics
        )
        if not findings:
            return None
        return "Python package structural validation failed: " + "; ".join(findings)
