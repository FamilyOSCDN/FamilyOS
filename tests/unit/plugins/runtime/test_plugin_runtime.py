"""Tests for plugin runtime."""

from dataclasses import dataclass

import pytest

from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)
from familyos_cli.plugins.capabilities.plugin_capability_id import (
    PluginCapabilityId,
)
from familyos_cli.plugins.contributions.contribution import (
    Contribution,
)
from familyos_cli.plugins.contributions.plugin_contribution_id import (
    PluginContributionId,
)
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)
from familyos_cli.plugins.runtime.runtime_state import (
    RuntimeState,
)


class DummyPlugin(
    Plugin,
):
    """Plugin used by runtime tests."""

    @property
    def name(
        self,
    ) -> str:
        """Return plugin display name."""

        return "Dummy Plugin"


def test_plugin_runtime_creation() -> None:
    """Runtime should initialize successfully."""

    runtime = PluginRuntime()

    assert runtime.plugins().all() == []


def test_activate_plugin() -> None:
    """Runtime should activate a plugin."""

    runtime = PluginRuntime()

    plugin = DummyPlugin()

    runtime.activate(
        plugin,
    )

    assert runtime.plugins().all() == [
        plugin,
    ]


def test_deactivate_plugin() -> None:
    """Runtime should deactivate an active plugin."""

    runtime = PluginRuntime()

    plugin = DummyPlugin()

    runtime.activate(
        plugin,
    )

    runtime.deactivate(
        plugin,
    )

    assert runtime.plugins().all() == []


def test_runtime_context() -> None:
    """Runtime should expose its context."""

    runtime = PluginRuntime()

    assert runtime.context() is not None


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

    assert runtime.plugin(
        "familyos.dummy",
    ) is plugin


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


class OwnedCapabilityPlugin(
    Plugin,
):
    """Plugin exposing a capability in its canonical namespace."""

    @property
    def name(
        self,
    ) -> str:
        """Return plugin display name."""

        return "Owned Capability Plugin"

    def capabilities(
        self,
    ) -> tuple[PluginCapability, ...]:
        """Return capabilities owned by the plugin."""

        return (
            PluginCapability(
                id=PluginCapabilityId(
                    "familyos.dummy.example",
                ),
                display_name="Dummy Example",
                description="Example capability.",
            ),
        )


class ForeignCapabilityPlugin(
    Plugin,
):
    """Plugin exposing a capability owned by another plugin."""

    @property
    def name(
        self,
    ) -> str:
        """Return plugin display name."""

        return "Foreign Capability Plugin"

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
                description="Foreign capability.",
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


@dataclass(
    frozen=True,
    slots=True,
)
class RuntimeTestContribution(
    Contribution,
):
    """Contribution used by runtime ownership tests."""

    name: str


class OwnedContributionPlugin(
    Plugin,
):
    """Plugin exposing a contribution in its canonical namespace."""

    @property
    def name(
        self,
    ) -> str:
        """Return plugin display name."""

        return "Owned Contribution Plugin"

    def contributions(
        self,
    ) -> tuple[Contribution, ...]:
        """Return a contribution owned by the plugin."""

        return (
            RuntimeTestContribution(
                id=PluginContributionId(
                    "familyos.dummy.example",
                ),
                name="example",
            ),
        )


class ForeignContributionPlugin(
    Plugin,
):
    """Plugin exposing a contribution from another namespace."""

    @property
    def name(
        self,
    ) -> str:
        """Return plugin display name."""

        return "Foreign Contribution Plugin"

    def contributions(
        self,
    ) -> tuple[Contribution, ...]:
        """Return a contribution owned by another plugin."""

        return (
            RuntimeTestContribution(
                id=PluginContributionId(
                    "familyos.finance.generation",
                ),
                name="foreign",
            ),
        )


def test_runtime_accepts_contribution_owned_by_plugin() -> None:
    """Runtime should accept contributions in the plugin namespace."""

    runtime = PluginRuntime()

    plugin = OwnedContributionPlugin()

    runtime.activate(
        plugin,
        plugin_id="familyos.dummy",
    )

    assert runtime.plugin(
        "familyos.dummy",
    ) is plugin


def test_runtime_rejects_contribution_owned_by_another_plugin() -> None:
    """Runtime should reject contributions outside the plugin namespace."""

    runtime = PluginRuntime()

    with pytest.raises(
        ValueError,
        match="does not belong to plugin 'familyos.dummy'",
    ):
        runtime.activate(
            ForeignContributionPlugin(),
            plugin_id="familyos.dummy",
        )
