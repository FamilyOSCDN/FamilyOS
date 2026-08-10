"""Tests for the plugin runtime."""

import pytest

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_metadata import PluginMetadata
from familyos_cli.plugins.runtime.plugin_runtime import PluginRuntime
from familyos_cli.plugins.runtime.runtime_context import RuntimeContext
from familyos_cli.plugins.runtime.runtime_state import RuntimeState


class DummyPlugin(Plugin):
    """Dummy plugin."""

    metadata = PluginMetadata(
        name="dummy",
        version="1.0.0",
    )


def test_activate_plugin() -> None:
    """Activating a plugin should register it."""

    runtime = PluginRuntime()

    plugin = DummyPlugin()

    runtime.activate(plugin)

    assert runtime.plugins().plugins() == [plugin]


def test_activate_plugin_sets_active_state() -> None:
    """Activating a plugin should set its runtime state."""

    runtime = PluginRuntime()

    plugin = DummyPlugin()

    runtime.activate(plugin)

    assert runtime.state(plugin) == RuntimeState.ACTIVE


def test_deactivate_plugin_sets_stopped_state() -> None:
    """Deactivating a plugin should stop its runtime."""

    runtime = PluginRuntime()

    plugin = DummyPlugin()

    runtime.activate(plugin)
    runtime.deactivate(plugin)

    assert runtime.state(plugin) == RuntimeState.STOPPED
    assert runtime.plugins().plugins() == []


def test_runtime_accepts_context() -> None:
    """Runtime should accept an injected context."""

    context = RuntimeContext()

    runtime = PluginRuntime(
        context=context,
    )

    assert runtime.context() is context


def test_activate_plugin_with_canonical_plugin_id() -> None:
    """Runtime should use an explicit canonical plugin identifier."""

    runtime = PluginRuntime()

    plugin = DummyPlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.dummy",
    )

    assert (
        runtime.state_by_plugin_id(
            "familyos.dummy",
        )
        == RuntimeState.ACTIVE
    )


def test_runtime_tracks_active_plugin_by_canonical_id() -> None:
    """Runtime should associate canonical identity with active instance."""

    runtime = PluginRuntime()

    plugin = DummyPlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.dummy",
    )

    assert (
        runtime.plugin(
            "familyos.dummy",
        )
        is plugin
    )


def test_deactivate_plugin_by_canonical_plugin_id() -> None:
    """Runtime should deactivate the original active plugin instance."""

    runtime = PluginRuntime()

    plugin = DummyPlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.dummy",
    )

    runtime.deactivate_by_plugin_id(
        "familyos.dummy",
    )

    assert (
        runtime.state_by_plugin_id(
            "familyos.dummy",
        )
        == RuntimeState.STOPPED
    )

    assert runtime.plugins().all() == []


def test_explicit_plugin_id_does_not_use_display_name_for_lifecycle() -> None:
    """Canonical identity should be independent from display metadata."""

    runtime = PluginRuntime()

    plugin = DummyPlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.dummy",
    )

    assert (
        runtime.context().lifecycle.state(
            "familyos.dummy",
        )
        == RuntimeState.ACTIVE
    )


class OwnedCapabilityPlugin(Plugin):
    """Plugin exposing a capability in its canonical namespace."""

    def capabilities(
        self,
    ) -> tuple[PluginCapability, ...]:
        """Return capabilities owned by the plugin."""

        return (
            PluginCapability(
                id=PluginCapabilityId(
                    "familyos.dummy.example",
                ),
                display_name="Example",
            ),
        )


class ForeignCapabilityPlugin(Plugin):
    """Plugin exposing a capability from another plugin namespace."""

    def capabilities(
        self,
    ) -> tuple[PluginCapability, ...]:
        """Return a capability owned by another plugin."""

        return (
            PluginCapability(
                id=PluginCapabilityId(
                    "familyos.finance.account",
                ),
                display_name="Finance Account",
            ),
        )


def test_runtime_accepts_capability_owned_by_plugin() -> None:
    """Runtime should accept capabilities in the plugin namespace."""

    runtime = PluginRuntime()

    runtime.activate(
        OwnedCapabilityPlugin(),
        plugin_id="familyos.dummy",
    )

    capability_id = PluginCapabilityId(
        "familyos.dummy.example",
    )

    assert runtime.capabilities().contains(
        capability_id,
    )


def test_runtime_rejects_capability_owned_by_another_plugin() -> None:
    """Runtime should reject capabilities outside the plugin namespace."""

    runtime = PluginRuntime()

    with pytest.raises(
        ValueError,
        match="does not belong to plugin 'familyos.dummy'",
    ):
        runtime.activate(
            ForeignCapabilityPlugin(),
            plugin_id="familyos.dummy",
        )
