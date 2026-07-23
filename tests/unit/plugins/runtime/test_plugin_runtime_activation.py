from __future__ import annotations

from familyos_cli.plugins.plugin import Plugin
from familyos_cli.plugins.plugin_metadata import PluginMetadata
from familyos_cli.plugins.runtime.lifecycle import Lifecycle
from familyos_cli.plugins.runtime.plugin_runtime import PluginRuntime


class DummyPlugin(Plugin):
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="Dummy Plugin",
            version="1.0.0",
            author="FamilyOS Team",
            description="Dummy plugin",
        )

    def before_generate(
        self,
        context: object,
    ) -> None:
        pass


def test_register_activates_plugin() -> None:
    runtime = PluginRuntime()

    runtime.register(
        DummyPlugin(),
    )

    hooks = runtime.hooks().get(
        Lifecycle.BEFORE_GENERATE,
    )

    assert len(hooks) == 1