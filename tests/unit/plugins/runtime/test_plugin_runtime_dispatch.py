from __future__ import annotations

from familyos_cli.plugins.runtime.lifecycle import Lifecycle
from familyos_cli.plugins.runtime.plugin_runtime import PluginRuntime


def test_runtime_dispatches_hooks() -> None:
    runtime = PluginRuntime()

    calls: list[str] = []

    def callback(context: object) -> None:
        calls.append("called")

    runtime.hooks().register(
        Lifecycle.BEFORE_GENERATE,
        callback,
    )

    runtime.dispatch(
        Lifecycle.BEFORE_GENERATE,
        object(),
    )

    assert calls == ["called"]