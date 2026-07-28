from familyos_cli.plugins.runtime.lifecycle import Lifecycle


def test_lifecycle_contains_standard_events() -> None:
    assert Lifecycle.INITIALIZE == "initialize"
    assert Lifecycle.SHUTDOWN == "shutdown"
    assert Lifecycle.BEFORE_GENERATE == "before_generate"
    assert Lifecycle.AFTER_GENERATE == "after_generate"
