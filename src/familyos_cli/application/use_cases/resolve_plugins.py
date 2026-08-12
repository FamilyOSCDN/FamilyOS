"""Resolve plugins use case."""

from __future__ import annotations

import re

from familyos_cli.plugins.ecosystem.pipeline import (
    PluginResolutionPipeline,
)
from familyos_cli.plugins.ecosystem.repository import (
    PluginRepository,
)
from familyos_cli.plugins.ecosystem.resolution import (
    ConstraintSet,
    PluginDependency,
    ResolutionPlan,
)
from familyos_cli.plugins.identity import PluginId

_DEPENDENCY_PATTERN = re.compile(
    r"^(?P<plugin_id>[A-Za-z0-9][A-Za-z0-9._-]*)(?P<constraint>.*)$",
)


class ResolvePluginsUseCase:
    """Resolve plugin dependencies from repository input."""

    def __init__(
        self,
        pipeline: PluginResolutionPipeline,
    ) -> None:
        """Initialize the use case."""

        self._pipeline = pipeline

    def execute(
        self,
        *,
        dependencies: list[str],
        repository_name: str,
        repository_url: str,
        repository_type: str,
    ) -> ResolutionPlan:
        """Resolve plugin dependencies."""

        repository = PluginRepository(
            name=repository_name,
            url=repository_url,
            repository_type=repository_type,
        )

        parsed_dependencies = [
            self._parse_dependency(
                dependency,
            )
            for dependency in dependencies
        ]

        return self._pipeline.resolve(
            repository=repository,
            dependencies=parsed_dependencies,
        )

    @staticmethod
    def _parse_dependency(
        value: str,
    ) -> PluginDependency:
        """Parse and validate a plugin dependency expression."""

        normalized_value = value.strip()

        match = _DEPENDENCY_PATTERN.fullmatch(
            normalized_value,
        )

        if match is None:
            raise ValueError(
                f"Invalid plugin dependency: {value!r}.",
            )

        plugin_id = PluginId(
            match.group("plugin_id"),
        ).value

        constraint_value = (
            match.group("constraint").strip()
        )

        if not constraint_value:
            return PluginDependency(
                plugin_id=plugin_id,
            )

        return PluginDependency(
            plugin_id=plugin_id,
            constraint_set=ConstraintSet.parse(
                constraint_value,
            ),
        )
