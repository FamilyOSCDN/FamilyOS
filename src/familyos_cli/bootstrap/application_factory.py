"""Application factory."""

from __future__ import annotations

from familyos_cli.bootstrap.container import (
    ApplicationContainer,
)


class ApplicationFactory:
    """Create application containers."""

    @staticmethod
    def create() -> ApplicationContainer:
        """Create an application container."""

        return ApplicationContainer()