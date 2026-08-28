"""Canonical Family Membership domain events."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from familyos_cli.domain.family.family_id import FamilyId
from familyos_cli.domain.person import PersonId


@dataclass(frozen=True, slots=True)
class _MembershipEvent:
    """Shared validation for canonical Membership event identity and time."""

    family_id: FamilyId
    person_id: PersonId
    occurred_at: datetime

    def __post_init__(self) -> None:
        """Validate canonical Membership event payload."""
        event_name = type(self).__name__

        if not isinstance(self.family_id, FamilyId):
            raise TypeError(f"{event_name} family_id must be a FamilyId")

        if not isinstance(self.person_id, PersonId):
            raise TypeError(f"{event_name} person_id must be a PersonId")

        if not isinstance(self.occurred_at, datetime):
            raise TypeError(f"{event_name} occurred_at must be a datetime")

        if self.occurred_at.tzinfo is None or self.occurred_at.utcoffset() is None:
            raise ValueError(
                f"{event_name} occurrence time must be timezone-aware"
            )


@dataclass(frozen=True, slots=True)
class FamilyMembershipCreated(_MembershipEvent):
    """Immutable fact that one canonical Membership was established."""


@dataclass(frozen=True, slots=True)
class FamilyMembershipActivated(_MembershipEvent):
    """Immutable fact that one PENDING Membership became ACTIVE."""


@dataclass(frozen=True, slots=True)
class FamilyMembershipSuspended(_MembershipEvent):
    """Immutable fact that one ACTIVE Membership became SUSPENDED."""


@dataclass(frozen=True, slots=True)
class FamilyMembershipReactivated(_MembershipEvent):
    """Immutable fact that one SUSPENDED Membership became ACTIVE."""


@dataclass(frozen=True, slots=True)
class FamilyMembershipEnded(_MembershipEvent):
    """Immutable fact that one Membership continuity became ENDED."""
