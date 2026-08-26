from __future__ import annotations

import pytest

from familyos_cli.application.build.artifact_reproducibility import (
    ArtifactReproducibilityComparison,
    ArtifactReproducibilityStatus,
    ArtifactVariabilityClassification,
    ReproducibilityComparison,
)
from familyos_cli.application.build.artifact_type import ArtifactClass


def _comparison(
    artifact_type: ArtifactClass = ArtifactClass.PYTHON_WHEEL,
    *,
    raw_size_equal: bool = True,
    raw_digest_equal: bool = True,
    content_equal: bool = True,
    variability: ArtifactVariabilityClassification = (
        ArtifactVariabilityClassification.NONE
    ),
    status: ArtifactReproducibilityStatus = (
        ArtifactReproducibilityStatus.BIT_FOR_BIT_EQUIVALENT
    ),
) -> ArtifactReproducibilityComparison:
    return ArtifactReproducibilityComparison(
        artifact_type=artifact_type,
        raw_size_equal=raw_size_equal,
        raw_digest_equal=raw_digest_equal,
        content_equal=content_equal,
        variability=variability,
        status=status,
    )


def test_bit_for_bit_equivalent_artifact_is_valid() -> None:
    comparison = _comparison()

    assert comparison.raw_size_equal
    assert comparison.raw_digest_equal
    assert comparison.content_equal
    assert comparison.variability is ArtifactVariabilityClassification.NONE
    assert comparison.status is ArtifactReproducibilityStatus.BIT_FOR_BIT_EQUIVALENT


@pytest.mark.parametrize(
    ("raw_size_equal", "raw_digest_equal", "content_equal"),
    (
        (False, True, True),
        (True, False, True),
        (True, True, False),
    ),
)
def test_bit_for_bit_equivalent_rejects_raw_or_content_difference(
    raw_size_equal: bool,
    raw_digest_equal: bool,
    content_equal: bool,
) -> None:
    with pytest.raises(ValueError):
        _comparison(
            raw_size_equal=raw_size_equal,
            raw_digest_equal=raw_digest_equal,
            content_equal=content_equal,
        )


def test_bit_for_bit_equivalent_rejects_variability() -> None:
    with pytest.raises(ValueError):
        _comparison(
            variability=ArtifactVariabilityClassification.EXPECTED,
        )


def test_logically_equivalent_artifact_is_valid() -> None:
    comparison = _comparison(
        artifact_type=ArtifactClass.SOURCE_DISTRIBUTION,
        raw_size_equal=False,
        raw_digest_equal=False,
        content_equal=True,
        variability=ArtifactVariabilityClassification.EXPECTED,
        status=ArtifactReproducibilityStatus.LOGICALLY_EQUIVALENT,
    )

    assert comparison.content_equal
    assert not comparison.raw_digest_equal
    assert comparison.status is ArtifactReproducibilityStatus.LOGICALLY_EQUIVALENT


def test_logically_equivalent_rejects_content_difference() -> None:
    with pytest.raises(ValueError):
        _comparison(
            raw_size_equal=False,
            raw_digest_equal=False,
            content_equal=False,
            variability=ArtifactVariabilityClassification.EXPECTED,
            status=ArtifactReproducibilityStatus.LOGICALLY_EQUIVALENT,
        )


def test_logically_equivalent_rejects_equal_raw_digest() -> None:
    with pytest.raises(ValueError):
        _comparison(
            raw_digest_equal=True,
            variability=ArtifactVariabilityClassification.EXPECTED,
            status=ArtifactReproducibilityStatus.LOGICALLY_EQUIVALENT,
        )


def test_logically_equivalent_rejects_unexplained_variability() -> None:
    with pytest.raises(ValueError):
        _comparison(
            raw_digest_equal=False,
            variability=ArtifactVariabilityClassification.UNEXPLAINED,
            status=ArtifactReproducibilityStatus.LOGICALLY_EQUIVALENT,
        )


def test_non_reproducible_artifact_is_valid() -> None:
    comparison = _comparison(
        raw_size_equal=False,
        raw_digest_equal=False,
        content_equal=False,
        variability=ArtifactVariabilityClassification.UNEXPLAINED,
        status=ArtifactReproducibilityStatus.NON_REPRODUCIBLE,
    )

    assert comparison.status is ArtifactReproducibilityStatus.NON_REPRODUCIBLE


def test_non_reproducible_rejects_expected_variability() -> None:
    with pytest.raises(ValueError):
        _comparison(
            raw_size_equal=False,
            raw_digest_equal=False,
            content_equal=False,
            variability=ArtifactVariabilityClassification.EXPECTED,
            status=ArtifactReproducibilityStatus.NON_REPRODUCIBLE,
        )


def test_aggregate_accepts_sorted_unique_artifacts() -> None:
    wheel = _comparison(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
    )
    sdist = _comparison(
        artifact_type=ArtifactClass.SOURCE_DISTRIBUTION,
        raw_size_equal=False,
        raw_digest_equal=False,
        variability=ArtifactVariabilityClassification.EXPECTED,
        status=ArtifactReproducibilityStatus.LOGICALLY_EQUIVALENT,
    )

    artifacts = tuple(
        sorted(
            (wheel, sdist),
            key=lambda comparison: comparison.artifact_type.value,
        )
    )

    result = ReproducibilityComparison(artifacts=artifacts)

    assert result.reproducible


def test_aggregate_rejects_duplicate_artifact_types() -> None:
    comparison = _comparison()

    with pytest.raises(ValueError):
        ReproducibilityComparison(
            artifacts=(comparison, comparison),
        )


def test_aggregate_rejects_unsorted_artifacts() -> None:
    wheel = _comparison(
        artifact_type=ArtifactClass.PYTHON_WHEEL,
    )
    sdist = _comparison(
        artifact_type=ArtifactClass.SOURCE_DISTRIBUTION,
        raw_size_equal=False,
        raw_digest_equal=False,
        variability=ArtifactVariabilityClassification.EXPECTED,
        status=ArtifactReproducibilityStatus.LOGICALLY_EQUIVALENT,
    )

    sorted_artifacts = sorted(
        (wheel, sdist),
        key=lambda comparison: comparison.artifact_type.value,
    )

    with pytest.raises(ValueError):
        ReproducibilityComparison(
            artifacts=tuple(reversed(sorted_artifacts)),
        )


def test_aggregate_reports_non_reproducible_artifact() -> None:
    comparison = _comparison(
        raw_digest_equal=False,
        content_equal=False,
        variability=ArtifactVariabilityClassification.UNEXPLAINED,
        status=ArtifactReproducibilityStatus.NON_REPRODUCIBLE,
    )

    result = ReproducibilityComparison(
        artifacts=(comparison,),
    )

    assert not result.reproducible


def test_non_reproducible_allows_changed_content_without_metadata_variability() -> None:
    comparison = _comparison(
        raw_size_equal=True,
        raw_digest_equal=False,
        content_equal=False,
        variability=ArtifactVariabilityClassification.NONE,
        status=ArtifactReproducibilityStatus.NON_REPRODUCIBLE,
    )

    assert comparison.status is ArtifactReproducibilityStatus.NON_REPRODUCIBLE
    assert comparison.variability is ArtifactVariabilityClassification.NONE
    assert not comparison.content_equal


def test_non_reproducible_equal_content_requires_unexplained_variability() -> None:
    with pytest.raises(ValueError):
        _comparison(
            raw_size_equal=False,
            raw_digest_equal=False,
            content_equal=True,
            variability=ArtifactVariabilityClassification.NONE,
            status=ArtifactReproducibilityStatus.NON_REPRODUCIBLE,
        )
