"""Tests for canonical Family Membership domain events."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from typing import cast
from uuid import UUID

import pytest

from familyos_cli.domain.family import (
    FamilyId,
    FamilyMembershipActivated,
    FamilyMembershipCreated,
    FamilyMembershipEnded,
    FamilyMembershipReactivated,
    FamilyMembershipSuspended,
)
from familyos_cli.domain.person import PersonId

EVENT_TYPES = (
    FamilyMembershipCreated,
    FamilyMembershipActivated,
    FamilyMembershipSuspended,
    FamilyMembershipReactivated,
    FamilyMembershipEnded,
)


def _family_id() -> FamilyId:
    return FamilyId(UUID("12345678-1234-4234-8234-123456789abc"))


def _person_id() -> PersonId:
    return PersonId(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_membership_event_preserves_canonical_identity_and_time(event_type: type) -> None:
    family_id = _family_id()
    person_id = _person_id()
    occurred_at = datetime(2026, 8, 28, 18, 0, tzinfo=UTC)

    event = event_type(
        family_id=family_id,
        person_id=person_id,
        occurred_at=occurred_at,
    )

    assert event.family_id == family_id
    assert event.person_id == person_id
    assert event.occurred_at == occurred_at


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_membership_event_requires_family_id(event_type: type) -> None:
    with pytest.raises(TypeError, match=r"family_id must be a FamilyId"):
        event_type(
            family_id=cast(FamilyId, "family-001"),
            person_id=_person_id(),
            occurred_at=datetime(2026, 8, 28, 18, 5, tzinfo=UTC),
        )


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_membership_event_requires_person_id(event_type: type) -> None:
    with pytest.raises(TypeError, match=r"person_id must be a PersonId"):
        event_type(
            family_id=_family_id(),
            person_id=cast(PersonId, "person-001"),
            occurred_at=datetime(2026, 8, 28, 18, 10, tzinfo=UTC),
        )


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_membership_event_requires_datetime(event_type: type) -> None:
    with pytest.raises(TypeError, match=r"occurred_at must be a datetime"):
        event_type(
            family_id=_family_id(),
            person_id=_person_id(),
            occurred_at=cast(datetime, "2026-08-28T18:15:00Z"),
        )


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_membership_event_requires_timezone_aware_occurrence_time(
    event_type: type,
) -> None:
    with pytest.raises(ValueError, match=r"occurrence time must be timezone-aware"):
        event_type(
            family_id=_family_id(),
            person_id=_person_id(),
            occurred_at=datetime(2026, 8, 28, 18, 20),
        )


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_membership_event_is_immutable(event_type: type) -> None:
    event = event_type(
        family_id=_family_id(),
        person_id=_person_id(),
        occurred_at=datetime(2026, 8, 28, 18, 25, tzinfo=UTC),
    )

    with pytest.raises(FrozenInstanceError):
        event.person_id = _person_id()  # type: ignore[misc]


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_membership_event_payload_does_not_invent_state_or_identifier(
    event_type: type,
) -> None:
    event = event_type(
        family_id=_family_id(),
        person_id=_person_id(),
        occurred_at=datetime(2026, 8, 28, 18, 30, tzinfo=UTC),
    )

    assert set(event.__dataclass_fields__) == {
        "family_id",
        "person_id",
        "occurred_at",
    }
