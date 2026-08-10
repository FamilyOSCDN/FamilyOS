"""Canonical Plugin Identifier."""

from __future__ import annotations

import re
from dataclasses import dataclass

_PLUGIN_ID_PATTERN = re.compile(
    r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$",
)


@dataclass(
    frozen=True,
    slots=True,
)
class PluginId:
    """Represent a canonical Plugin Identifier."""

    value: str

    def __post_init__(
        self,
    ) -> None:
        """Validate the Plugin Identifier."""

        if not _PLUGIN_ID_PATTERN.fullmatch(
            self.value,
        ):
            raise ValueError(
                (f"Invalid Plugin Identifier: '{self.value}'."),
            )

    def __str__(
        self,
    ) -> str:
        """Return the canonical identifier value."""

        return self.value
