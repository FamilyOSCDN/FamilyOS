from __future__ import annotations

import pytest

from familyos_cli.application.build.artifact_archive_metadata import (
    ArchiveMetadataField,
    ArtifactArchiveMetadataObservation,
)
from familyos_cli.application.build.artifact_type import ArtifactClass


def test_metadata_observation_reports_equal_metadata() -> None:
    observation = ArtifactArchiveMetadataObservation(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        differing_fields=(),
    )

    assert observation.metadata_equal


def test_metadata_observation_reports_differences() -> None:
    observation = ArtifactArchiveMetadataObservation(
        artifact_type=ArtifactClass.SOURCE_DISTRIBUTION,
        differing_fields=(ArchiveMetadataField.TIMESTAMP,),
    )

    assert not observation.metadata_equal


def test_metadata_observation_rejects_duplicate_fields() -> None:
    with pytest.raises(ValueError):
        ArtifactArchiveMetadataObservation(
            artifact_type=ArtifactClass.SOURCE_DISTRIBUTION,
            differing_fields=(
                ArchiveMetadataField.TIMESTAMP,
                ArchiveMetadataField.TIMESTAMP,
            ),
        )


def test_metadata_observation_rejects_unsorted_fields() -> None:
    fields = tuple(
        sorted(
            (
                ArchiveMetadataField.TIMESTAMP,
                ArchiveMetadataField.MODE,
            ),
            key=lambda field: field.value,
            reverse=True,
        )
    )

    with pytest.raises(ValueError):
        ArtifactArchiveMetadataObservation(
            artifact_type=ArtifactClass.SOURCE_DISTRIBUTION,
            differing_fields=fields,
        )
