"""Artifact locations."""

from __future__ import annotations

from enum import StrEnum


class ArtifactLocation(StrEnum):
    """Supported artifact locations."""

    DOMAIN = "domain"
    APPLICATION = "application"
    INFRASTRUCTURE = "infrastructure"
    INTERFACES = "interfaces"
    TESTS = "tests"
    DOCUMENTATION = "documentation"