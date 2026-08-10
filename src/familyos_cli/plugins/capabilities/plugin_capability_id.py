"""Plugin capability identifier value object."""

import re
from dataclasses import dataclass

_CAPABILITY_ID_PATTERN = re.compile(
    r"^[a-z0-9][a-z0-9-]*"
    r"(?:\.[a-z0-9][a-z0-9-]*){2,}$",
)


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

        if _CAPABILITY_ID_PATTERN.fullmatch(
            self.value,
        ) is None:
            raise ValueError(
                f"Invalid plugin capability id: {self.value!r}.",
            )

    def __str__(
        self,
    ) -> str:
        """Return the string representation."""

        return self.value
