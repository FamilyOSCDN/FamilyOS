"""Tests for canonical Quality check identity."""

import pytest

from familyos_cli.domain.quality import QualityCheckId


@pytest.mark.parametrize(
    "value",
    (
        "QLT-CHECK-LINT",
        "QLT-CHECK-TYPE",
        "QLT-CHECK-UNIT",
        "QLT-CHECK-ARCH",
        "QLT-CHECK-DOC",
        "QLT-CHECK-TYPE-001",
    ),
)
def test_quality_check_id_accepts_canonical_identifiers(value: str) -> None:
    identifier = QualityCheckId(value)

    assert identifier.value == value
    assert str(identifier) == value


@pytest.mark.parametrize(
    "value",
    (
        "CHECK-LINT",
        "QLT-CHECK-",
        " QLT-CHECK-LINT",
        "QLT-CHECK-LINT ",
        "QLT-CHECK-L INT",
    ),
)
def test_quality_check_id_rejects_invalid_identifiers(value: str) -> None:
    with pytest.raises((TypeError, ValueError)):
        QualityCheckId(value)


def test_quality_check_id_is_immutable() -> None:
    identifier = QualityCheckId("QLT-CHECK-LINT")

    with pytest.raises(AttributeError):
        identifier.value = "QLT-CHECK-TYPE"  # type: ignore[misc]
