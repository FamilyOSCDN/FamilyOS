"""Installed plugin model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.identity import PluginId


@dataclass(
    frozen=True,
    slots=True,
    init=False,
)
class InstalledPlugin:
    """Represents an installed FamilyOS plugin.

    ``plugin_id`` is the canonical installed Plugin Identifier.

    The historical ``name`` constructor argument and property remain
    available as compatibility aliases.
    """

    plugin_id: str
    version: str
    location: str

    def __init__(
        self,
        name: str | None = None,
        version: str = "",
        location: str = "",
        *,
        plugin_id: str | None = None,
    ) -> None:
        """Create an installed plugin representation.

        Args:
            name: Legacy alias for the Plugin Identifier.
            version: Installed plugin version.
            location: Installed plugin location.
            plugin_id: Canonical Plugin Identifier.

        Raises:
            ValueError: If no Plugin Identifier is provided, if
                identity inputs disagree, or if an explicit canonical
                Plugin Identifier is invalid.
        """

        explicit_plugin_id = plugin_id is not None

        if plugin_id is None:
            plugin_id = name

        if plugin_id is None:
            raise ValueError(
                "Plugin identifier is required.",
            )

        if name is not None and explicit_plugin_id and name != plugin_id:
            raise ValueError(
                "name and plugin_id must reference the same Plugin Identifier.",
            )

        if explicit_plugin_id:
            plugin_id = PluginId(
                plugin_id,
            ).value

        object.__setattr__(
            self,
            "plugin_id",
            plugin_id,
        )
        object.__setattr__(
            self,
            "version",
            version,
        )
        object.__setattr__(
            self,
            "location",
            location,
        )

    @property
    def name(
        self,
    ) -> str:
        """Return legacy Plugin Identifier alias."""

        return self.plugin_id

    def identifier(
        self,
    ) -> str:
        """Return installed plugin identifier."""

        return f"{self.plugin_id}@{self.version}"
