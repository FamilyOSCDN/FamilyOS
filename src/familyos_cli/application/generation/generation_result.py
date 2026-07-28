"""Generation result."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(
    frozen=True,
    slots=True,
)
class GenerationResult:
    """Result of a project generation."""

    success: bool

    generated_files: tuple[Path, ...]

    warnings: tuple[str, ...]

    duration: float
