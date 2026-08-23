"""Capture canonical non-sensitive environment state for build execution."""

from __future__ import annotations

import platform
import sys
import tempfile
from collections.abc import Callable

from familyos_cli.application.build.environment_state import EnvironmentState


def _virtual_environment_is_active() -> bool:
    """Detect Python virtual-environment isolation without shell variables."""

    return sys.prefix != sys.base_prefix


class EnvironmentStateProvider:
    """Capture relevant platform properties for one canonical build."""

    def __init__(
        self,
        *,
        system_provider: Callable[[], str] = platform.system,
        release_provider: Callable[[], str] = platform.release,
        machine_provider: Callable[[], str] = platform.machine,
        virtual_environment_provider: Callable[
            [],
            bool,
        ] = _virtual_environment_is_active,
        temporary_directory_provider: Callable[
            [],
            str,
        ] = tempfile.gettempdir,
        filesystem_encoding_provider: Callable[
            [],
            str,
        ] = sys.getfilesystemencoding,
    ) -> None:
        self._system_provider = system_provider
        self._release_provider = release_provider
        self._machine_provider = machine_provider
        self._virtual_environment_provider = virtual_environment_provider
        self._temporary_directory_provider = temporary_directory_provider
        self._filesystem_encoding_provider = filesystem_encoding_provider

    def capture(self) -> EnvironmentState:
        """Capture canonical non-sensitive platform properties."""

        return EnvironmentState(
            operating_system=self._system_provider(),
            operating_system_release=self._release_provider(),
            machine_architecture=self._machine_provider(),
            virtual_environment_active=(
                self._virtual_environment_provider()
            ),
            temporary_directory=self._temporary_directory_provider(),
            filesystem_encoding=self._filesystem_encoding_provider(),
        )
