"""Plugin capability identifier value object."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class PluginCapabilityId:
    """Identify a plugin capability."""

    value: str

    def __post_init__(
        self,
    ) -> None:
        """Validate the capability identifier."""

        if not self.value:
            raise ValueError(
                "Plugin capability id cannot be empty.",
            )

    def __str__(
        self,
    ) -> str:
        """Return the string representation."""

        return self.value
