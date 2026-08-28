"""Canonical Family Relationship lifecycle states."""

from enum import StrEnum


class RelationshipState(StrEnum):
    """Persisted states for one canonical Relationship continuity."""

    ESTABLISHED = "established"
    ENDED = "ended"
