"""Plugin dependency cycle model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.identity import PluginId


@dataclass(frozen=True, slots=True)
class DependencyCycle:
    """Represent a cycle discovered in plugin dependencies."""

    path: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate the dependency cycle path."""

        canonical_path = tuple(PluginId(plugin_id).value for plugin_id in self.path)

        object.__setattr__(
            self,
            "path",
            canonical_path,
        )

        if len(self.path) < 2:
            raise ValueError(
                "A dependency cycle must contain at least two nodes.",
            )

        if self.path[0] != self.path[-1]:
            raise ValueError(
                "A dependency cycle path must start and end with the same plugin.",
            )

    @property
    def plugin(self) -> str:
        """Return the plugin used as the cycle entry point."""

        return self.path[0]

    @property
    def length(self) -> int:
        """Return the number of dependency edges in the cycle."""

        return len(self.path) - 1

    def contains(
        self,
        plugin_id: str,
    ) -> bool:
        """Return whether the cycle contains the given plugin."""

        canonical_plugin_id = PluginId(plugin_id).value

        return canonical_plugin_id in self.path[:-1]

    def unique_plugins(self) -> tuple[str, ...]:
        """Return cycle plugins without the repeated closing node."""

        plugins: list[str] = []

        for plugin in self.path[:-1]:
            if plugin not in plugins:
                plugins.append(
                    plugin,
                )

        return tuple(plugins)

    def normalized(self) -> DependencyCycle:
        """Return a deterministic representation of this cycle."""

        plugins = self.path[:-1]
        smallest_plugin = min(
            plugins,
        )
        start_index = plugins.index(
            smallest_plugin,
        )
        normalized_plugins = plugins[start_index:] + plugins[:start_index]

        return DependencyCycle(
            path=(
                *normalized_plugins,
                normalized_plugins[0],
            ),
        )
