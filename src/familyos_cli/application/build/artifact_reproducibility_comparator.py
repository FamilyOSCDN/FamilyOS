"""Canonical artifact reproducibility comparison."""

from __future__ import annotations

from familyos_cli.application.build.artifact_archive_metadata import (
    ArtifactArchiveMetadataObservation,
)
from familyos_cli.application.build.artifact_content_snapshot import (
    ArtifactContentSnapshot,
)
from familyos_cli.application.build.artifact_reproducibility import (
    ArtifactReproducibilityComparison,
    ArtifactReproducibilityStatus,
)
from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.reproducibility_variability_policy import (
    ReproducibilityVariabilityPolicy,
)


class ArtifactReproducibilityComparator:
    """Compare equivalent-build artifacts using canonical observations."""

    def __init__(
        self,
        variability_policy: ReproducibilityVariabilityPolicy | None = None,
    ) -> None:
        self._variability_policy = (
            variability_policy or ReproducibilityVariabilityPolicy()
        )

    def compare(
        self,
        *,
        artifact_type: ArtifactClass,
        left_size: int,
        right_size: int,
        left_digest: str,
        right_digest: str,
        left_content: ArtifactContentSnapshot,
        right_content: ArtifactContentSnapshot,
        metadata: ArtifactArchiveMetadataObservation,
    ) -> ArtifactReproducibilityComparison:
        """Classify reproducibility for one canonical artifact."""

        self._require_matching_artifact_type(
            artifact_type,
            left_content,
            right_content,
            metadata,
        )

        raw_size_equal = left_size == right_size
        raw_digest_equal = left_digest == right_digest
        content_equal = left_content.matches(right_content)
        variability = self._variability_policy.classify(metadata)

        if raw_digest_equal:
            if not raw_size_equal or not content_equal or not metadata.metadata_equal:
                return ArtifactReproducibilityComparison(
                    artifact_type=artifact_type,
                    raw_size_equal=raw_size_equal,
                    raw_digest_equal=raw_digest_equal,
                    content_equal=content_equal,
                    variability=variability,
                    status=ArtifactReproducibilityStatus.NON_REPRODUCIBLE,
                )

            return ArtifactReproducibilityComparison(
                artifact_type=artifact_type,
                raw_size_equal=True,
                raw_digest_equal=True,
                content_equal=True,
                variability=variability,
                status=ArtifactReproducibilityStatus.BIT_FOR_BIT_EQUIVALENT,
            )

        if content_equal and variability.value == "expected":
            return ArtifactReproducibilityComparison(
                artifact_type=artifact_type,
                raw_size_equal=raw_size_equal,
                raw_digest_equal=False,
                content_equal=True,
                variability=variability,
                status=ArtifactReproducibilityStatus.LOGICALLY_EQUIVALENT,
            )

        return ArtifactReproducibilityComparison(
            artifact_type=artifact_type,
            raw_size_equal=raw_size_equal,
            raw_digest_equal=False,
            content_equal=content_equal,
            variability=variability,
            status=ArtifactReproducibilityStatus.NON_REPRODUCIBLE,
        )

    def _require_matching_artifact_type(
        self,
        artifact_type: ArtifactClass,
        left_content: ArtifactContentSnapshot,
        right_content: ArtifactContentSnapshot,
        metadata: ArtifactArchiveMetadataObservation,
    ) -> None:
        if (
            left_content.artifact_type is not artifact_type
            or right_content.artifact_type is not artifact_type
            or metadata.artifact_type is not artifact_type
        ):
            raise ValueError(
                "reproducibility comparison artifact types must match"
            )
