"""Compliance rule lifecycle states."""

from __future__ import annotations

from enum import StrEnum


class RuleLifecycle(StrEnum):
    """Represent the governance lifecycle state of a compliance rule."""

    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    RETIRED = "retired"
