"""Canonical Testing Framework source-state model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TestingSourceState:
    """Source revision and working-tree state observed for test execution."""

    revision: str | None
    dirty: bool | None
