from __future__ import annotations

from familyos_cli.plugins.hooks import HookRegistry
from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.runtime.lifecycle import Lifecycle
from familyos_cli.plugins.runtime.plugin_activator import PluginActivator


class DummyPlugin(Plugin):
    @property
    def name(self) -> str:
        return "dummy"

    def before_generate(self, context: object) -> None:
        pass


def test_activate_registers_hooks() -> None:
    registry = HookRegistry()

    activator = PluginActivator(registry)

    activator.activate(
        DummyPlugin(),
    )

    hooks = registry.get(
        Lifecycle.BEFORE_GENERATE,
    )

    assert len(hooks) == 1