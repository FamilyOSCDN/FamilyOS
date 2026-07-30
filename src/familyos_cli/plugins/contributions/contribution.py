"""Base contribution contract."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class Contribution:
    """Base class for every plugin contribution."""
