from __future__ import annotations

from familyos_cli.plugins.hooks import HookRegistry
from familyos_cli.plugins.runtime.hook_dispatcher import HookDispatcher


def test_dispatch_calls_registered_hooks() -> None:
    registry = HookRegistry()
    dispatcher = HookDispatcher(registry)

    calls: list[str] = []

    def callback(context: object) -> None:
        calls.append("called")

    registry.register(
        "before_generate",
        callback,
    )

    dispatcher.dispatch(
        "before_generate",
        object(),
    )

    assert calls == ["called"]
