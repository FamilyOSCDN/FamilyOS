"""Immutable models for package artifact discovery."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING

from familyos_cli.application.build.artifact_identity import ArtifactIdentity
from familyos_cli.application.build.artifact_integrity import ArtifactIntegrity
from familyos_cli.application.build.artifact_manifest import ArtifactManifest
from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.package_build import (
    PackageBuildResult,
    PackageBuildStatus,
)
from familyos_cli.application.build.source_state import SourceState

if TYPE_CHECKING:
    from familyos_cli.application.build.package_functional_validation import (
        PythonWheelFunctionalValidationResult,
    )
    from familyos_cli.application.build.package_validation import (
        PythonPackageStructuralValidationResult,
    )


class ArtifactOutputClassification(StrEnum):
    """Current Level 14 output classification."""

    CANDIDATE = "candidate"


class ArtifactDiscoveryStatus(StrEnum):
    """Outcome of comparing current outputs with the expected artifact set."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class ExpectedArtifactDefinition:
    """Required artifact class and its deterministic filename rule."""

    artifact_class: ArtifactClass
    filename_suffix: str
    required_count: int

    def accepts(self, path: Path) -> bool:
        """Return whether a regular output file matches this definition."""

        return path.is_file() and path.name.endswith(self.filename_suffix)


@dataclass(frozen=True, slots=True)
class DiscoveredArtifact:
    """A current output classified as a candidate, without trust semantics."""

    path: Path
    artifact_class: ArtifactClass
    classification: ArtifactOutputClassification = (
        ArtifactOutputClassification.CANDIDATE
    )


@dataclass(frozen=True, slots=True)
class ArtifactDiscoveryResult:
    """Deterministic comparison of expected and current package outputs."""

    status: ArtifactDiscoveryStatus
    output_dir: Path
    candidates: tuple[DiscoveredArtifact, ...] = ()
    missing_expectations: tuple[ArtifactClass, ...] = ()
    unexpected_outputs: tuple[Path, ...] = ()
    diagnostic: str | None = None

    @property
    def successful(self) -> bool:
        """Return whether the exact expected artifact set was discovered."""

        return self.status is ArtifactDiscoveryStatus.SUCCEEDED


@dataclass(frozen=True, slots=True)
class CanonicalPackageBuildResult:
    """Aggregate execution, discovery, and requested validation results."""

    status: PackageBuildStatus
    execution: PackageBuildResult
    source_state: SourceState
    build_id: BuildId = field(default_factory=BuildId.generate)
    artifact_identities: tuple[ArtifactIdentity, ...] = ()
    artifact_integrities: tuple[ArtifactIntegrity, ...] = ()
    artifact_manifest: ArtifactManifest | None = None
    discovery: ArtifactDiscoveryResult | None = None
    validation: PythonPackageStructuralValidationResult | None = None
    functional_validation: PythonWheelFunctionalValidationResult | None = None

    @property
    def successful(self) -> bool:
        """Return whether every performed canonical build stage succeeded."""

        return self.status is PackageBuildStatus.SUCCEEDED

    @property
    def candidates(self) -> tuple[DiscoveredArtifact, ...]:
        """Return classified candidates when discovery was performed."""

        return self.discovery.candidates if self.discovery else ()

    @property
    def diagnostic(self) -> str | None:
        """Return the latest applicable canonical-stage diagnostic."""

        if self.functional_validation and self.functional_validation.diagnostic:
            return self.functional_validation.diagnostic
        if self.validation and self.validation.diagnostic:
            return self.validation.diagnostic
        if self.discovery and self.discovery.diagnostic:
            return self.discovery.diagnostic
        return self.execution.diagnostic
