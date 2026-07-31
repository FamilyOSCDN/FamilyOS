"""Plugin version constraint value object."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.resolution.plugin_version import (
    PluginVersion,
)
from familyos_cli.plugins.ecosystem.resolution.version_operator import (
    VersionOperator,
)


@dataclass(frozen=True, slots=True)
class VersionConstraint:
    """Represent an atomic plugin version constraint."""

    operator: VersionOperator
    version: PluginVersion

    @classmethod
    def parse(
        cls,
        value: str,
    ) -> VersionConstraint:
        """Parse a version constraint string.

        Args:
            value: Constraint such as ``>=1.2.0`` or ``^2.0.0``.

        Returns:
            Parsed version constraint.

        Raises:
            ValueError: If the constraint is invalid.
        """

        normalized_value = value.strip()

        for operator in sorted(
            VersionOperator,
            key=lambda item: len(item.value),
            reverse=True,
        ):
            if normalized_value.startswith(operator.value):
                version_value = normalized_value[
                    len(operator.value):
                ].strip()

                if not version_value:
                    raise ValueError(
                        f"Invalid version constraint: {value!r}. "
                        "A version is required.",
                    )

                return cls(
                    operator=operator,
                    version=PluginVersion.parse(
                        version_value,
                    ),
                )

        raise ValueError(
            f"Invalid version constraint: {value!r}. "
            "A supported operator is required.",
        )

    def is_satisfied_by(
        self,
        version: PluginVersion,
    ) -> bool:
        """Return whether a plugin version satisfies the constraint."""

        if self.operator is VersionOperator.EQUAL:
            return version == self.version

        if self.operator is VersionOperator.GREATER:
            return version > self.version

        if self.operator is VersionOperator.GREATER_OR_EQUAL:
            return version >= self.version

        if self.operator is VersionOperator.LOWER:
            return version < self.version

        if self.operator is VersionOperator.LOWER_OR_EQUAL:
            return version <= self.version

        if self.operator is VersionOperator.COMPATIBLE:
            return (
                version >= self.version
                and version < self._compatible_upper_bound()
            )

        if self.operator is VersionOperator.APPROXIMATE:
            return (
                version >= self.version
                and version < self._approximate_upper_bound()
            )

        raise ValueError(
            f"Unsupported version operator: {self.operator.value!r}.",
        )

    def _compatible_upper_bound(
        self,
    ) -> PluginVersion:
        """Return the exclusive upper bound for a caret constraint."""

        if self.version.major > 0:
            return PluginVersion(
                major=self.version.major + 1,
                minor=0,
                patch=0,
            )

        if self.version.minor > 0:
            return PluginVersion(
                major=0,
                minor=self.version.minor + 1,
                patch=0,
            )

        return PluginVersion(
            major=0,
            minor=0,
            patch=self.version.patch + 1,
        )

    def _approximate_upper_bound(
        self,
    ) -> PluginVersion:
        """Return the exclusive upper bound for a tilde constraint."""

        return PluginVersion(
            major=self.version.major,
            minor=self.version.minor + 1,
            patch=0,
        )

    def __str__(self) -> str:
        """Return the canonical constraint string."""

        return f"{self.operator.value}{self.version}"
