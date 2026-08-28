"""Canonical Family Relationship taxonomy."""

from enum import StrEnum


class RelationshipType(StrEnum):
    """Initial governed Family Relationship taxonomy."""

    PARENT_OF = "parent_of"
    CHILD_OF = "child_of"
    SPOUSE_OF = "spouse_of"
    SIBLING_OF = "sibling_of"
