"""Canonical repository-layout validation models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RepositoryLayoutValidationResult:
    """Outcome of validating one build output against repository structure."""

    successful: bool
    diagnostic: str | None = None
