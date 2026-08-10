"""Plugin dependency model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.resolution.constraint_set import (
    ConstraintSet,
)
from familyos_cli.plugins.ecosystem.resolution.version_constraint import (
    VersionConstraint,
)
from familyos_cli.plugins.ecosystem.resolution.version_operator import (
    VersionOperator,
)
from familyos_cli.plugins.identity import PluginId


@dataclass(
    frozen=True,
    slots=True,
    init=False,
)
class PluginDependency:
    """Represent a plugin dependency requirement.

    ``plugin_id`` is the canonical dependency target.

    The historical ``name`` constructor argument and property remain
    available as compatibility aliases.
    """

    plugin_id: str
    constraint_set: ConstraintSet | None

    def __init__(
        self,
        name: str | None = None,
        minimum_version: str = "",
        *,
        plugin_id: str | None = None,
        constraint: VersionConstraint | None = None,
        constraint_set: ConstraintSet | None = None,
    ) -> None:
        """Initialize a plugin dependency.

        Args:
            name: Legacy alias for the required Plugin Identifier.
            minimum_version: Legacy minimum version requirement.
            plugin_id: Canonical required Plugin Identifier.
            constraint: Legacy typed atomic constraint.
            constraint_set: Typed collection of version constraints.

        Raises:
            ValueError: If identifier inputs disagree or multiple
                constraint inputs are provided.
        """

        explicit_plugin_id = plugin_id is not None

        if plugin_id is None:
            plugin_id = name

        if plugin_id is None:
            raise ValueError(
                "Plugin identifier is required.",
            )

        if (
            name is not None
            and explicit_plugin_id
            and name != plugin_id
        ):
            raise ValueError(
                "name and plugin_id must reference "
                "the same Plugin Identifier.",
            )

        if explicit_plugin_id:
            plugin_id = PluginId(
                plugin_id,
            ).value

        provided_inputs = sum(
            (
                bool(minimum_version),
                constraint is not None,
                constraint_set is not None,
            ),
        )

        if provided_inputs > 1:
            raise ValueError(
                "Specify only one of minimum_version, "
                "constraint or constraint_set.",
            )

        resolved_constraint_set = constraint_set

        if minimum_version:
            resolved_constraint_set = ConstraintSet.parse(
                f">={minimum_version}",
            )

        if constraint is not None:
            resolved_constraint_set = ConstraintSet(
                constraints=(
                    constraint,
                ),
            )

        object.__setattr__(
            self,
            "plugin_id",
            plugin_id,
        )
        object.__setattr__(
            self,
            "constraint_set",
            resolved_constraint_set,
        )

    @property
    def name(
        self,
    ) -> str:
        """Return legacy Plugin Identifier alias."""

        return self.plugin_id

    @property
    def constraint(
        self,
    ) -> VersionConstraint | None:
        """Return the legacy atomic constraint when available."""

        if self.constraint_set is None:
            return None

        if len(self.constraint_set.constraints) != 1:
            return None

        return self.constraint_set.constraints[0]

    @property
    def minimum_version(
        self,
    ) -> str:
        """Return the legacy minimum version value.

        This compatibility property is populated only when the dependency
        contains exactly one greater-than-or-equal constraint.
        """

        constraint = self.constraint

        if constraint is None:
            return ""

        if constraint.operator is not VersionOperator.GREATER_OR_EQUAL:
            return ""

        return str(
            constraint.version,
        )

    def identifier(
        self,
    ) -> str:
        """Return the dependency identifier."""

        if self.constraint_set is None:
            return self.plugin_id

        return f"{self.plugin_id}{self.constraint_set}"
