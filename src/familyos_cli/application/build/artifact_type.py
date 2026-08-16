"""Semantic artifact types used by canonical package builds."""

from __future__ import annotations

from enum import StrEnum


class ArtifactClass(StrEnum):
    """Semantic classes supported by the current package output contract."""

    PYTHON_WHEEL = "python-wheel"
    SOURCE_DISTRIBUTION = "source-distribution"
