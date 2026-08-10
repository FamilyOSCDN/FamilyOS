"""Plugin capability registry."""

from __future__ import annotations

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)


class CapabilityRegistry:
    """Registry of plugin capabilities."""

    def __init__(
        self,
    ) -> None:
        """Initialize an empty registry."""

        self._capabilities: dict[
            PluginCapabilityId,
            PluginCapability,
        ] = {}

    def register(
        self,
        capability: PluginCapability,
    ) -> None:
        """Register a capability."""

        if capability.id in self._capabilities:
            raise ValueError(
                f"Capability '{capability.id}' already registered.",
            )

        self._capabilities[
            capability.id
        ] = capability

    def get(
        self,
        capability_id: PluginCapabilityId,
    ) -> PluginCapability:
        """Return a registered capability."""

        try:
            return self._capabilities[
                capability_id
            ]
        except KeyError as error:
            raise ValueError(
                f"Capability '{capability_id}' not found.",
            ) from error

    def contains(
        self,
        capability_id: PluginCapabilityId,
    ) -> bool:
        """Return whether a capability exists."""

        return capability_id in self._capabilities

    def list(
        self,
    ) -> tuple[PluginCapability, ...]:
        """Return all registered capabilities."""

        return tuple(
            self._capabilities.values(),
        )

    def unregister(
        self,
        capability_id: PluginCapabilityId,
    ) -> None:
        """Remove a registered capability."""

        self._capabilities.pop(
            capability_id,
            None,
        )

    def clear(
        self,
    ) -> None:
        """Remove all registered capabilities."""

        self._capabilities.clear()
