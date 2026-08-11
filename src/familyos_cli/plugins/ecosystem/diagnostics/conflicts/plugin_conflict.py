"""Plugin resolution conflict model."""

from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.plugins.ecosystem.diagnostics.conflicts.conflict_reason import (
    ConflictReason,
)
from familyos_cli.plugins.identity import PluginId


@dataclass(frozen=True, slots=True)
class PluginConflict:
    """Represent a technical conflict discovered during plugin resolution."""

    plugin: str
    reason: ConflictReason
    required_by: tuple[str, ...] = field(default_factory=tuple)
    requested_constraints: tuple[str, ...] = field(default_factory=tuple)
    available_versions: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """Validate plugin identifiers."""

        canonical_plugin = PluginId(self.plugin).value

        canonical_required_by = tuple(
            PluginId(plugin_id).value for plugin_id in self.required_by
        )

        object.__setattr__(
            self,
            "plugin",
            canonical_plugin,
        )
        object.__setattr__(
            self,
            "required_by",
            canonical_required_by,
        )

    def concerns(self, plugin_id: str) -> bool:
        """Return whether this conflict concerns the given plugin."""

        canonical_plugin_id = PluginId(plugin_id).value

        return self.plugin == canonical_plugin_id

    def is_required_by(self, plugin_id: str) -> bool:
        """Return whether the given plugin introduced this requirement."""

        canonical_plugin_id = PluginId(plugin_id).value

        return canonical_plugin_id in self.required_by

    def has_available_versions(self) -> bool:
        """Return whether versions were available for the conflicted plugin."""

        return bool(self.available_versions)

    def has_multiple_constraints(self) -> bool:
        """Return whether several constraints contributed to the conflict."""

        return len(self.requested_constraints) > 1
