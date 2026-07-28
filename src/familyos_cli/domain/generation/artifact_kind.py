"""Artifact kinds."""

from __future__ import annotations

from enum import StrEnum


class ArtifactKind(StrEnum):
    """Supported artifact kinds."""

    ENTITY = "entity"
    VALUE_OBJECT = "value_object"
    AGGREGATE = "aggregate"
    REPOSITORY = "repository"
    SERVICE = "service"

    README = "readme"
    DOCUMENTATION = "documentation"

    TEST = "test"

    TEMPLATE = "template"