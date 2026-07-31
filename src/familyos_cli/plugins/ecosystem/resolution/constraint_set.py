"""Plugin version constraint set."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.plugins.ecosystem.resolution.plugin_version import (
    PluginVersion,
)
from familyos_cli.plugins.ecosystem.resolution.version_constraint import (
    VersionConstraint,
)


@dataclass(frozen=True, slots=True)
class ConstraintSet:
    """Represents a collection of version constraints."""

    constraints: tuple[VersionConstraint, ...] = field(
        default_factory=tuple,
    )

    @classmethod
    def parse(
        cls,
        value: str,
    ) -> ConstraintSet:
        """Parse a comma-separated constraint expression."""

        constraints = tuple(
            VersionConstraint.parse(
                item.strip(),
            )
            for item in value.split(",")
            if item.strip()
        )

        if not constraints:
            raise ValueError(
                "Constraint set cannot be empty.",
            )

        return cls(
            constraints=constraints,
        )

    def is_satisfied_by(
        self,
        version: PluginVersion,
    ) -> bool:
        """Return whether all constraints are satisfied."""

        return all(
            constraint.is_satisfied_by(
                version,
            )
            for constraint in self.constraints
        )

    def __str__(
        self,
    ) -> str:
        """Return the canonical constraint set."""

        return ",".join(
            str(constraint)
            for constraint in self.constraints
        )
