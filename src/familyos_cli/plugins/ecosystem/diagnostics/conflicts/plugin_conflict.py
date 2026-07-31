"""Plugin resolution conflict model."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.plugins.ecosystem.diagnostics.conflicts.conflict_reason import (
    ConflictReason,
)


@dataclass(frozen=True, slots=True)
class PluginConflict:
    """Represent a technical conflict discovered during plugin resolution."""

    plugin: str
    reason: ConflictReason
    required_by: tuple[str, ...] = field(default_factory=tuple)
    requested_constraints: tuple[str, ...] = field(default_factory=tuple)
    available_versions: tuple[str, ...] = field(default_factory=tuple)

    def concerns(self, plugin_name: str) -> bool:
        """Return whether this conflict concerns the given plugin."""

        return self.plugin == plugin_name

    def is_required_by(self, plugin_name: str) -> bool:
        """Return whether the given plugin introduced this requirement."""

        return plugin_name in self.required_by

    def has_available_versions(self) -> bool:
        """Return whether versions were available for the conflicted plugin."""

        return bool(self.available_versions)

    def has_multiple_constraints(self) -> bool:
        """Return whether several constraints contributed to the conflict."""

        return len(self.requested_constraints) > 1
