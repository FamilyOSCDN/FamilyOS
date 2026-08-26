from __future__ import annotations

import pytest

from familyos_cli.application.build.artifact_archive_metadata import (
    ArchiveMetadataField,
    ArtifactArchiveMetadataObservation,
)
from familyos_cli.application.build.artifact_content_snapshot import (
    ArtifactContentMember,
    ArtifactContentSnapshot,
)
from familyos_cli.application.build.artifact_integrity import (
    ArtifactDigestAlgorithm,
)
from familyos_cli.application.build.artifact_reproducibility import (
    ArtifactReproducibilityStatus,
    ArtifactVariabilityClassification,
)
from familyos_cli.application.build.artifact_reproducibility_comparator import (
    ArtifactReproducibilityComparator,
)
from familyos_cli.application.build.artifact_type import ArtifactClass

_DIGEST_A = "a" * 64
_DIGEST_B = "b" * 64


def _snapshot(
    artifact_type: ArtifactClass,
    digest: str = _DIGEST_A,
) -> ArtifactContentSnapshot:
    member = ArtifactContentMember(
        path="module.py",
        size=10,
        digest_algorithm=ArtifactDigestAlgorithm.SHA256,
        digest=digest,
    )

    return ArtifactContentSnapshot(
        artifact_type=artifact_type,
        members=(member,),
    )


def _metadata(
    artifact_type: ArtifactClass,
    differing_fields: tuple[ArchiveMetadataField, ...] = (),
) -> ArtifactArchiveMetadataObservation:
    return ArtifactArchiveMetadataObservation(
        artifact_type=artifact_type,
        differing_fields=differing_fields,
    )


def test_identical_wheel_is_bit_for_bit_equivalent() -> None:
    snapshot = _snapshot(ArtifactClass.PYTHON_WHEEL)

    result = ArtifactReproducibilityComparator().compare(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        left_size=100,
        right_size=100,
        left_digest=_DIGEST_A,
        right_digest=_DIGEST_A,
        left_content=snapshot,
        right_content=snapshot,
        metadata=_metadata(ArtifactClass.PYTHON_WHEEL),
    )

    assert (
        result.status
        is ArtifactReproducibilityStatus.BIT_FOR_BIT_EQUIVALENT
    )
    assert result.variability is ArtifactVariabilityClassification.NONE


def test_sdist_timestamp_variability_is_logically_equivalent() -> None:
    snapshot = _snapshot(ArtifactClass.SOURCE_DISTRIBUTION)

    result = ArtifactReproducibilityComparator().compare(
        artifact_type=ArtifactClass.SOURCE_DISTRIBUTION,
        left_size=100,
        right_size=101,
        left_digest=_DIGEST_A,
        right_digest=_DIGEST_B,
        left_content=snapshot,
        right_content=snapshot,
        metadata=_metadata(
            ArtifactClass.SOURCE_DISTRIBUTION,
            (ArchiveMetadataField.TIMESTAMP,),
        ),
    )

    assert (
        result.status
        is ArtifactReproducibilityStatus.LOGICALLY_EQUIVALENT
    )
    assert result.variability is ArtifactVariabilityClassification.EXPECTED


def test_changed_content_is_non_reproducible() -> None:
    result = ArtifactReproducibilityComparator().compare(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        left_size=100,
        right_size=100,
        left_digest=_DIGEST_A,
        right_digest=_DIGEST_B,
        left_content=_snapshot(
            ArtifactClass.PYTHON_WHEEL,
            _DIGEST_A,
        ),
        right_content=_snapshot(
            ArtifactClass.PYTHON_WHEEL,
            _DIGEST_B,
        ),
        metadata=_metadata(ArtifactClass.PYTHON_WHEEL),
    )

    assert (
        result.status
        is ArtifactReproducibilityStatus.NON_REPRODUCIBLE
    )


def test_unexplained_metadata_variability_is_non_reproducible() -> None:
    snapshot = _snapshot(ArtifactClass.PYTHON_WHEEL)

    result = ArtifactReproducibilityComparator().compare(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        left_size=100,
        right_size=101,
        left_digest=_DIGEST_A,
        right_digest=_DIGEST_B,
        left_content=snapshot,
        right_content=snapshot,
        metadata=_metadata(
            ArtifactClass.PYTHON_WHEEL,
            (ArchiveMetadataField.TIMESTAMP,),
        ),
    )

    assert (
        result.status
        is ArtifactReproducibilityStatus.NON_REPRODUCIBLE
    )
    assert (
        result.variability
        is ArtifactVariabilityClassification.UNEXPLAINED
    )


def test_equal_raw_digest_with_metadata_difference_is_non_reproducible() -> None:
    snapshot = _snapshot(ArtifactClass.PYTHON_WHEEL)

    result = ArtifactReproducibilityComparator().compare(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
        left_size=100,
        right_size=100,
        left_digest=_DIGEST_A,
        right_digest=_DIGEST_A,
        left_content=snapshot,
        right_content=snapshot,
        metadata=_metadata(
            ArtifactClass.PYTHON_WHEEL,
            (ArchiveMetadataField.TIMESTAMP,),
        ),
    )

    assert (
        result.status
        is ArtifactReproducibilityStatus.NON_REPRODUCIBLE
    )


def test_rejects_mismatched_content_artifact_type() -> None:
    wheel = _snapshot(ArtifactClass.PYTHON_WHEEL)
    sdist = _snapshot(ArtifactClass.SOURCE_DISTRIBUTION)

    with pytest.raises(ValueError):
        ArtifactReproducibilityComparator().compare(
            artifact_type=ArtifactClass.PYTHON_WHEEL,
            left_size=100,
            right_size=100,
            left_digest=_DIGEST_A,
            right_digest=_DIGEST_A,
            left_content=wheel,
            right_content=sdist,
            metadata=_metadata(ArtifactClass.PYTHON_WHEEL),
        )


def test_rejects_mismatched_metadata_artifact_type() -> None:
    wheel = _snapshot(ArtifactClass.PYTHON_WHEEL)

    with pytest.raises(ValueError):
        ArtifactReproducibilityComparator().compare(
            artifact_type=ArtifactClass.PYTHON_WHEEL,
            left_size=100,
            right_size=100,
            left_digest=_DIGEST_A,
            right_digest=_DIGEST_A,
            left_content=wheel,
            right_content=wheel,
            metadata=_metadata(ArtifactClass.SOURCE_DISTRIBUTION),
        )
