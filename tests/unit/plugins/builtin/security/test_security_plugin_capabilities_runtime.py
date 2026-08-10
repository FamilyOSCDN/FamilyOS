"""Runtime capability tests for SecurityPlugin."""

from familyos_cli.plugins.builtin.security.plugin import (
    SecurityPlugin,
)
from familyos_cli.plugins.runtime.plugin_runtime import (
    PluginRuntime,
)


def test_security_plugin_registers_capabilities_in_runtime() -> None:
    """Security capabilities are registered in the runtime."""

    runtime = PluginRuntime()

    runtime.activate(
        SecurityPlugin(),
    )

    capabilities = (
        runtime.capabilities()
        .list()
    )

    assert len(capabilities) == 2


def test_security_plugin_runtime_contains_expected_capabilities() -> None:
    """Runtime exposes the expected security capabilities."""

    runtime = PluginRuntime()

    runtime.activate(
        SecurityPlugin(),
    )

    identifiers = {
        str(capability.id)
        for capability in (
            runtime.capabilities()
            .list()
        )
    }

    assert identifiers == {
        "security.policy",
        "security.validation",
    }
