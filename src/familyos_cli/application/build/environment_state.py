"""Canonical non-sensitive environment state for build execution."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EnvironmentState:
    """Relevant platform properties observed for one canonical build."""

    operating_system: str
    operating_system_release: str
    machine_architecture: str
    virtual_environment_active: bool = False
    temporary_directory: str = "/tmp"
    filesystem_encoding: str = "utf-8"

    def __post_init__(self) -> None:
        """Reject incomplete canonical environment state."""

        if not self.operating_system:
            raise ValueError("operating system must not be empty")

        if not self.operating_system_release:
            raise ValueError("operating system release must not be empty")

        if not self.machine_architecture:
            raise ValueError("machine architecture must not be empty")

        if not isinstance(self.virtual_environment_active, bool):
            raise ValueError(
                "virtual environment state must be a boolean",
            )

        if not self.temporary_directory.strip():
            raise ValueError(
                "temporary directory must not be empty",
            )

        if not self.filesystem_encoding.strip():
            raise ValueError(
                "filesystem encoding must not be empty",
            )
