"""Policy for classifying archive metadata variability."""

from __future__ import annotations

from familyos_cli.application.build.artifact_archive_metadata import (
    ArchiveMetadataField,
    ArtifactArchiveMetadataObservation,
)
from familyos_cli.application.build.artifact_reproducibility import (
    ArtifactVariabilityClassification,
)
from familyos_cli.application.build.artifact_type import ArtifactClass


class ReproducibilityVariabilityPolicy:
    """Classify canonical artifact metadata variability."""

    def classify(
        self,
        observation: ArtifactArchiveMetadataObservation,
    ) -> ArtifactVariabilityClassification:
        """Classify observed archive metadata variability."""

        if observation.metadata_equal:
            return ArtifactVariabilityClassification.NONE

        if (
            observation.artifact_type
            is ArtifactClass.SOURCE_DISTRIBUTION
            and observation.differing_fields
            == (ArchiveMetadataField.TIMESTAMP,)
        ):
            return ArtifactVariabilityClassification.EXPECTED

        return ArtifactVariabilityClassification.UNEXPLAINED
