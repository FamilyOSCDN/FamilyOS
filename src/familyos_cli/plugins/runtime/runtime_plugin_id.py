"""Canonical runtime plugin identifier."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.identity import PluginId


@dataclass(
    frozen=True,
    slots=True,
)
class RuntimePluginId:
    """Represent a canonical runtime plugin identifier."""

    value: str

    def __post_init__(
        self,
    ) -> None:
        """Validate the runtime plugin identifier."""

        try:
            PluginId(
                self.value,
            )
        except ValueError as error:
            raise ValueError(
                (f"Invalid runtime plugin identifier: '{self.value}'."),
            ) from error

    def __str__(
        self,
    ) -> str:
        """Return the canonical identifier value."""

        return self.value
