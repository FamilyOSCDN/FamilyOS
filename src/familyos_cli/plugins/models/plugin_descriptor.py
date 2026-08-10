"""Plugin descriptor model."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from familyos_cli.plugins.identity import PluginId
from familyos_cli.plugins.models.plugin_metadata import PluginMetadata


@dataclass(frozen=True, slots=True, init=False)
class PluginDescriptor:
    """Describe an installed plugin."""

    id: str

    metadata: PluginMetadata

    module: str
    class_name: str

    path: Path

    enabled: bool = True

    def __init__(
        self,
        id: str,
        name: str | None = None,
        version: str | None = None,
        author: str = "",
        description: str = "",
        module: str = "",
        class_name: str = "",
        path: Path = Path("."),
        enabled: bool = True,
        metadata: PluginMetadata | None = None,
    ) -> None:
        """Create a plugin descriptor.

        Supports both:
        - legacy flat fields
        - new PluginMetadata composition
        """

        if metadata is None:
            metadata = PluginMetadata(
                name=name or "",
                version=version or "",
                author=author,
                description=description,
            )

        canonical_plugin_id = PluginId(id)

        object.__setattr__(
            self,
            "id",
            canonical_plugin_id.value,
        )
        object.__setattr__(self, "metadata", metadata)
        object.__setattr__(self, "module", module)
        object.__setattr__(self, "class_name", class_name)
        object.__setattr__(self, "path", path)
        object.__setattr__(self, "enabled", enabled)

    @property
    def name(self) -> str:
        """Return plugin name."""
        return self.metadata.name

    @property
    def version(self) -> str:
        """Return plugin version."""
        return self.metadata.version

    @property
    def author(self) -> str:
        """Return plugin author."""
        return self.metadata.author

    @property
    def description(self) -> str:
        """Return plugin description."""
        return self.metadata.description
