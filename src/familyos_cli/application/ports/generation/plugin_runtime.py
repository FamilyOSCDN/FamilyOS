"""Plugin runtime port."""

from __future__ import annotations

from typing import Protocol

from familyos_cli.application.generation.generation_context import (
    GenerationContext,
)


class PluginRuntime(Protocol):
    """Contract for plugin runtime operations."""

    def before_generate(
        self,
        context: GenerationContext,
    ) -> None:
        """Execute before generation hooks."""
        ...

    def after_generate(
        self,
        context: GenerationContext,
    ) -> None:
        """Execute after generation hooks."""
        ...
