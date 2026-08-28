"""Canonical Family Membership lifecycle states."""

from enum import StrEnum


class MembershipState(StrEnum):
    """Lifecycle state of one canonical Family Membership continuity."""

    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ENDED = "ended"
