"""Canonical non-sensitive environment state for build execution."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EnvironmentState:
    """Relevant platform properties observed for one canonical build."""

    operating_system: str
    operating_system_release: str
    machine_architecture: str

    def __post_init__(self) -> None:
        """Reject incomplete canonical environment state."""

        if not self.operating_system:
            raise ValueError("operating system must not be empty")

        if not self.operating_system_release:
            raise ValueError("operating system release must not be empty")

        if not self.machine_architecture:
            raise ValueError("machine architecture must not be empty")
