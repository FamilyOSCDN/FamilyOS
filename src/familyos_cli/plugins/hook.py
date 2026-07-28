from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Hook:
    """Represents a named plugin hook."""

    name: str
