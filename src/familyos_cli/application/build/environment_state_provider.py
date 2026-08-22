"""Capture canonical non-sensitive environment state for build execution."""

from __future__ import annotations

import platform
from collections.abc import Callable

from familyos_cli.application.build.environment_state import EnvironmentState


class EnvironmentStateProvider:
    """Capture relevant platform properties for one canonical build."""

    def __init__(
        self,
        *,
        system_provider: Callable[[], str] = platform.system,
        release_provider: Callable[[], str] = platform.release,
        machine_provider: Callable[[], str] = platform.machine,
    ) -> None:
        self._system_provider = system_provider
        self._release_provider = release_provider
        self._machine_provider = machine_provider

    def capture(self) -> EnvironmentState:
        """Capture canonical non-sensitive platform properties."""

        return EnvironmentState(
            operating_system=self._system_provider(),
            operating_system_release=self._release_provider(),
            machine_architecture=self._machine_provider(),
        )
