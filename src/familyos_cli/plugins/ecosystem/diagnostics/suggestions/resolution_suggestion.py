"""Resolution suggestion model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResolutionSuggestion:
    """Represent a possible action to resolve a diagnostic."""

    message: str

    def is_empty(self) -> bool:
        """Return whether the suggestion is empty."""

        return not self.message.strip()
