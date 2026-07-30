"""Generation preset identifier value object."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class GenerationPresetId:
    """Identify a generation preset."""

    value: str

    def __post_init__(
        self,
    ) -> None:
        """Validate preset identifier."""

        if not self.value:
            raise ValueError(
                "Generation preset id cannot be empty.",
            )

    def __str__(
        self,
    ) -> str:
        """Return string representation."""

        return self.value
