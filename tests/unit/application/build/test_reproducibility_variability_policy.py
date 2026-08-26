from __future__ import annotations

from familyos_cli.application.build.artifact_archive_metadata import (
    ArchiveMetadataField,
    ArtifactArchiveMetadataObservation,
)
from familyos_cli.application.build.artifact_reproducibility import (
    ArtifactVariabilityClassification,
)
from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.reproducibility_variability_policy import (
    ReproducibilityVariabilityPolicy,
)


def test_equal_metadata_has_no_variability() -> None:
    observation = ArtifactArchiveMetadataObservation(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        differing_fields=(),
    )

    assert (
        ReproducibilityVariabilityPolicy().classify(observation)
        is ArtifactVariabilityClassification.NONE
    )


def test_sdist_timestamp_only_variability_is_expected() -> None:
    observation = ArtifactArchiveMetadataObservation(
        artifact_type=ArtifactClass.SOURCE_DISTRIBUTION,
        differing_fields=(ArchiveMetadataField.TIMESTAMP,),
    )

    assert (
        ReproducibilityVariabilityPolicy().classify(observation)
        is ArtifactVariabilityClassification.EXPECTED
    )


def test_wheel_timestamp_variability_is_unexplained() -> None:
    observation = ArtifactArchiveMetadataObservation(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        differing_fields=(ArchiveMetadataField.TIMESTAMP,),
    )

    assert (
        ReproducibilityVariabilityPolicy().classify(observation)
        is ArtifactVariabilityClassification.UNEXPLAINED
    )


def test_sdist_non_timestamp_variability_is_unexplained() -> None:
    observation = ArtifactArchiveMetadataObservation(
        artifact_type=ArtifactClass.SOURCE_DISTRIBUTION,
        differing_fields=(ArchiveMetadataField.MODE,),
    )

    assert (
        ReproducibilityVariabilityPolicy().classify(observation)
        is ArtifactVariabilityClassification.UNEXPLAINED
    )


def test_sdist_timestamp_plus_other_variability_is_unexplained() -> None:
    observation = ArtifactArchiveMetadataObservation(
        artifact_type=ArtifactClass.SOURCE_DISTRIBUTION,
        differing_fields=tuple(
            sorted(
                (
                    ArchiveMetadataField.TIMESTAMP,
                    ArchiveMetadataField.MODE,
                ),
                key=lambda field: field.value,
            )
        ),
    )

    assert (
        ReproducibilityVariabilityPolicy().classify(observation)
        is ArtifactVariabilityClassification.UNEXPLAINED
    )
