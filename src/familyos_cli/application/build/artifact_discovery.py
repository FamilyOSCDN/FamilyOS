"""Immutable models for package artifact discovery."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING

from familyos_cli.application.build.package_build import (
    PackageBuildResult,
    PackageBuildStatus,
)

if TYPE_CHECKING:
    from familyos_cli.application.build.package_validation import (
        PythonPackageStructuralValidationResult,
    )


class ArtifactClass(StrEnum):
    """Semantic classes supported by the current package output contract."""

    PYTHON_WHEEL = "python-wheel"
    SOURCE_DISTRIBUTION = "source-distribution"


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
    """Aggregate execution, discovery, and structural validation result."""

    status: PackageBuildStatus
    execution: PackageBuildResult
    discovery: ArtifactDiscoveryResult | None = None
    validation: PythonPackageStructuralValidationResult | None = None

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

        if self.validation and self.validation.diagnostic:
            return self.validation.diagnostic
        if self.discovery and self.discovery.diagnostic:
            return self.discovery.diagnostic
        return self.execution.diagnostic
