"""Immutable source-state observation for canonical package builds."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SourceState:
    """Source revision and working-tree state observed before a build attempt."""

    revision: str | None
    dirty: bool | None
