"""Generation presets."""

from __future__ import annotations

from enum import StrEnum


class GenerationPreset(StrEnum):
    """Supported generation presets."""

    MINIMAL = "minimal"

    STANDARD = "standard"

    COMPLETE = "complete"
