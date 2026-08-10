"""Plugin package model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.identity import PluginId


@dataclass(
    frozen=True,
    slots=True,
    init=False,
)
class PluginPackage:
    """Represents a distributable FamilyOS plugin package.

    ``plugin_id`` is the canonical logical Plugin Identifier.

    The ``name`` constructor argument and property remain available as
    compatibility aliases for the historical ecosystem contract.
    """

    plugin_id: str
    version: str
    source: str
    checksum: str = ""
    signature: str = ""

    def __init__(
        self,
        name: str | None = None,
        version: str = "",
        source: str = "",
        checksum: str = "",
        signature: str = "",
        *,
        plugin_id: str | None = None,
    ) -> None:
        """Create a plugin package.

        Args:
            name: Legacy alias for the Plugin Identifier.
            version: Plugin package version.
            source: Repository or package source.
            checksum: Optional package checksum.
            signature: Optional package signature.
            plugin_id: Canonical Plugin Identifier.

        Raises:
            ValueError: If no Plugin Identifier is provided or if
                ``name`` and ``plugin_id`` disagree.
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
            "source",
            source,
        )
        object.__setattr__(
            self,
            "checksum",
            checksum,
        )
        object.__setattr__(
            self,
            "signature",
            signature,
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
        """Return unique versioned package identifier."""

        return f"{self.plugin_id}@{self.version}"
