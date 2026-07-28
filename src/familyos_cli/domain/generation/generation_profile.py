"""Generation profiles."""

from __future__ import annotations

from enum import StrEnum


class GenerationProfile(StrEnum):
    """Supported generation profiles."""

    DOMAIN_DOCUMENTATION = "domain_documentation"

    PYTHON_IMPLEMENTATION = "python_implementation"
