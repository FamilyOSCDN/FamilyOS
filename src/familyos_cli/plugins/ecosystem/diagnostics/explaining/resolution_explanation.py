"""Resolution explanation model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResolutionExplanation:
    """Human-oriented explanation of a plugin resolution issue."""

    title: str
    summary: str
    causes: tuple[str, ...] = ()
    suggestions: tuple[str, ...] = ()

    def has_causes(self) -> bool:
        """Return whether the explanation contains causes."""

        return bool(
            self.causes,
        )

    def has_suggestions(self) -> bool:
        """Return whether the explanation contains suggestions."""

        return bool(
            self.suggestions,
        )
