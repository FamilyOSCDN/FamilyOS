from familyos_cli.plugins.builtin.health.plugin import (
    HealthPlugin,
)
from familyos_cli.plugins.capabilities.plugin_capability import (
    PluginCapability,
)


def test_health_plugin_exposes_capabilities() -> None:
    plugin = HealthPlugin()

    capabilities = plugin.capabilities()

    assert len(capabilities) == 2

    assert all(
        isinstance(
            capability,
            PluginCapability,
        )
        for capability in capabilities
    )

    assert {
        str(capability.id)
        for capability in capabilities
    } == {
        "familyos.health.profile",
        "familyos.health.record",
    }
