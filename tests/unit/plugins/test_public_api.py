from __future__ import annotations


def test_public_api() -> None:
    """Public plugin API should expose the main classes."""

    from familyos_cli.plugins import (
        Plugin,
        PluginContext,
        PluginFactory,
        PluginLoader,
        PluginManager,
        PluginMetadata,
        PluginRegistry,
    )
    from familyos_cli.plugins.runtime import (
        HookDispatcher,
        Lifecycle,
        PluginActivator,
        PluginRuntime,
    )

    assert Plugin is not None
    assert PluginContext is not None
    assert PluginMetadata is not None
    assert PluginFactory is not None
    assert PluginLoader is not None
    assert PluginManager is not None
    assert PluginRegistry is not None

    assert Lifecycle is not None
    assert HookDispatcher is not None
    assert PluginActivator is not None
    assert PluginRuntime is not None
