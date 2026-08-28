from dataclasses import FrozenInstanceError, fields
from datetime import UTC, datetime
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.domain.family import FamilyCreated, FamilyId

_FAMILY_ID = FamilyId(UUID("01234567-89ab-4cde-8f01-23456789abcd"))
_OCCURRED_AT = datetime(2026, 8, 28, 9, 30, tzinfo=UTC)


def test_family_created_contains_minimal_canonical_payload() -> None:
    event = FamilyCreated(
        family_id=_FAMILY_ID,
        occurred_at=_OCCURRED_AT,
    )

    assert event.family_id == _FAMILY_ID
    assert event.occurred_at == _OCCURRED_AT
    assert [field.name for field in fields(FamilyCreated)] == [
        "family_id",
        "occurred_at",
    ]


def test_family_created_rejects_non_canonical_identity_reference() -> None:
    with pytest.raises(
        TypeError,
        match="FamilyCreated family_id must be a FamilyId",
    ):
        FamilyCreated(
            family_id=cast(FamilyId, "family-001"),
            occurred_at=_OCCURRED_AT,
        )


def test_family_created_rejects_non_datetime_occurrence_time() -> None:
    with pytest.raises(
        TypeError,
        match="FamilyCreated occurred_at must be a datetime",
    ):
        FamilyCreated(
            family_id=_FAMILY_ID,
            occurred_at=cast(datetime, "2026-08-28T09:30:00+02:00"),
        )


def test_family_created_requires_timezone_aware_occurrence_time() -> None:
    with pytest.raises(
        ValueError,
        match="FamilyCreated occurrence time must be timezone-aware",
    ):
        FamilyCreated(
            family_id=_FAMILY_ID,
            occurred_at=datetime(2026, 8, 28, 9, 30),
        )


def test_family_created_is_immutable() -> None:
    event = FamilyCreated(
        family_id=_FAMILY_ID,
        occurred_at=_OCCURRED_AT,
    )

    with pytest.raises(FrozenInstanceError):
        event.occurred_at = datetime(  # type: ignore[misc]
            2026,
            8,
            28,
            10,
            30,
            tzinfo=UTC,
        )
