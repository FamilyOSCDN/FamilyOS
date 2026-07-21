from familyos_cli.plugins.hooks import HookRegistry


def callback() -> None:
    pass


def test_register_hook() -> None:
    registry = HookRegistry()

    registry.register("before_generate", callback)

    assert registry.get("before_generate") == [callback]


def test_get_unknown_hook_returns_empty_list() -> None:
    registry = HookRegistry()

    assert registry.get("unknown") == []


def test_clear_hooks() -> None:
    registry = HookRegistry()

    registry.register("before_generate", callback)
    registry.register("after_generate", callback)

    registry.clear()

    assert registry.get("before_generate") == []
    assert registry.get("after_generate") == []