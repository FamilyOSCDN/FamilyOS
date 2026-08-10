"""Canonical runtime plugin identifier."""

from __future__ import annotations

import re
from dataclasses import dataclass

_RUNTIME_PLUGIN_ID_PATTERN = re.compile(
    r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+$",
)


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

        if not _RUNTIME_PLUGIN_ID_PATTERN.fullmatch(
            self.value,
        ):
            raise ValueError(
                (
                    "Invalid runtime plugin identifier: "
                    f"'{self.value}'."
                ),
            )

    def __str__(
        self,
    ) -> str:
        """Return the canonical identifier value."""

        return self.value
