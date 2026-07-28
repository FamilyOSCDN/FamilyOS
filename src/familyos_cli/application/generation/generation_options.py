"""Generation execution options."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GenerationOptions:
    """Execution options for artifact generation."""

    overwrite: bool = False

    encoding: str = "utf-8"

    create_directories: bool = True

    dry_run: bool = False
