from dataclasses import FrozenInstanceError, fields
from datetime import UTC, datetime
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.domain.person import PersonCreated, PersonId

_PERSON_ID = PersonId(UUID("01234567-89ab-4cde-8f01-23456789abcd"))
_OCCURRED_AT = datetime(2026, 8, 27, 9, 30, tzinfo=UTC)


def test_person_created_contains_minimal_canonical_payload() -> None:
    event = PersonCreated(
        person_id=_PERSON_ID,
        occurred_at=_OCCURRED_AT,
    )

    assert event.person_id == _PERSON_ID
    assert event.occurred_at == _OCCURRED_AT
    assert [field.name for field in fields(PersonCreated)] == [
        "person_id",
        "occurred_at",
    ]


def test_person_created_rejects_non_canonical_identity_reference() -> None:
    with pytest.raises(
        TypeError,
        match="PersonCreated person_id must be a PersonId",
    ):
        PersonCreated(
            person_id=cast(PersonId, "person-001"),
            occurred_at=_OCCURRED_AT,
        )


def test_person_created_requires_timezone_aware_occurrence_time() -> None:
    with pytest.raises(
        ValueError,
        match="PersonCreated occurrence time must be timezone-aware",
    ):
        PersonCreated(
            person_id=_PERSON_ID,
            occurred_at=datetime(2026, 8, 27, 9, 30),
        )


def test_person_created_is_immutable() -> None:
    event = PersonCreated(
        person_id=_PERSON_ID,
        occurred_at=_OCCURRED_AT,
    )

    with pytest.raises(FrozenInstanceError):
        event.occurred_at = datetime(  # type: ignore[misc]
            2026,
            8,
            27,
            10,
            30,
            tzinfo=UTC,
        )
