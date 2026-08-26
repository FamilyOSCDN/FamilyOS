"""Canonical comparison models for build artifact reproducibility."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from familyos_cli.application.build.artifact_type import ArtifactClass


class ArtifactReproducibilityStatus(StrEnum):
    """Canonical reproducibility classification for one artifact."""

    BIT_FOR_BIT_EQUIVALENT = "bit-for-bit-equivalent"
    LOGICALLY_EQUIVALENT = "logically-equivalent"
    NON_REPRODUCIBLE = "non-reproducible"


class ArtifactVariabilityClassification(StrEnum):
    """Classification of variability observed between equivalent builds."""

    NONE = "none"
    EXPECTED = "expected"
    UNEXPLAINED = "unexplained"


@dataclass(frozen=True, slots=True)
class ArtifactReproducibilityComparison:
    """Comparison result for one canonical artifact type."""

    artifact_type: ArtifactClass
    raw_size_equal: bool
    raw_digest_equal: bool
    content_equal: bool
    variability: ArtifactVariabilityClassification
    status: ArtifactReproducibilityStatus

    def __post_init__(self) -> None:
        """Reject internally inconsistent reproducibility classifications."""

        if self.status is ArtifactReproducibilityStatus.BIT_FOR_BIT_EQUIVALENT:
            if not (
                self.raw_size_equal and self.raw_digest_equal and self.content_equal
            ):
                raise ValueError(
                    "bit-for-bit equivalent artifacts must have equal "
                    "size, digest, and semantic content"
                )

            if self.variability is not ArtifactVariabilityClassification.NONE:
                raise ValueError(
                    "bit-for-bit equivalent artifacts must have no variability"
                )

        if self.status is ArtifactReproducibilityStatus.LOGICALLY_EQUIVALENT:
            if not self.content_equal:
                raise ValueError(
                    "logically equivalent artifacts must have equal semantic content"
                )

            if self.raw_digest_equal:
                raise ValueError(
                    "logically equivalent classification requires "
                    "raw digest variability"
                )

            if self.variability is not ArtifactVariabilityClassification.EXPECTED:
                raise ValueError(
                    "logically equivalent raw variability must be expected"
                )

        if (
            self.status is ArtifactReproducibilityStatus.NON_REPRODUCIBLE
            and self.variability is ArtifactVariabilityClassification.EXPECTED
        ):
            raise ValueError(
                "non-reproducible artifacts must not classify variability as expected"
            )

        if (
            self.status is ArtifactReproducibilityStatus.NON_REPRODUCIBLE
            and self.content_equal
            and self.variability is not ArtifactVariabilityClassification.UNEXPLAINED
        ):
            raise ValueError(
                "non-reproducible artifacts with equal semantic content "
                "must have unexplained variability"
            )


@dataclass(frozen=True, slots=True)
class ReproducibilityComparison:
    """Aggregate reproducibility result for one equivalent build pair."""

    artifacts: tuple[ArtifactReproducibilityComparison, ...]

    def __post_init__(self) -> None:
        """Require deterministic unique artifact ordering."""

        artifact_types = tuple(
            comparison.artifact_type for comparison in self.artifacts
        )

        if len(artifact_types) != len(set(artifact_types)):
            raise ValueError("reproducibility comparison artifact types must be unique")

        if artifact_types != tuple(
            sorted(artifact_types, key=lambda artifact_type: artifact_type.value)
        ):
            raise ValueError(
                "reproducibility comparisons must be sorted by artifact type"
            )

    @property
    def reproducible(self) -> bool:
        """Return whether every artifact is reproducible."""

        return all(
            comparison.status is not ArtifactReproducibilityStatus.NON_REPRODUCIBLE
            for comparison in self.artifacts
        )
