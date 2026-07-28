"""CLI command context."""

from __future__ import annotations

from functools import cached_property

from familyos_cli.application.use_cases.create_artifact import (
    CreateArtifactUseCase,
)
from familyos_cli.application.use_cases.create_domain import (
    CreateDomainUseCase,
)
from familyos_cli.application.use_cases.create_project import (
    CreateProjectUseCase,
)
from familyos_cli.bootstrap import (
    ApplicationContainer,
    ApplicationFactory,
)


class CommandContext:
    """Shared context for CLI commands."""

    def __init__(
        self,
        container: ApplicationContainer | None = None,
    ) -> None:
        """Initialize CLI context."""

        self._container = (
            container if container is not None else ApplicationFactory.create()
        )

    @cached_property
    def create_project(
        self,
    ) -> CreateProjectUseCase:
        """Provide project creation use case."""

        return self._container.create_project_use_case()

    @cached_property
    def create_artifact(
        self,
    ) -> CreateArtifactUseCase:
        """Provide artifact creation use case."""

        return self._container.create_artifact_use_case()

    @cached_property
    def create_domain(
        self,
    ) -> CreateDomainUseCase:
        """Provide domain creation use case."""

        return self._container.create_domain_use_case()
