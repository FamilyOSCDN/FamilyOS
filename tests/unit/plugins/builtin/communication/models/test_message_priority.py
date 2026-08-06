from familyos_cli.plugins.builtin.communication.models import (
    MessagePriority,
)


def test_message_priority_values() -> None:
    assert MessagePriority.LOW.value == "low"
    assert MessagePriority.NORMAL.value == "normal"
    assert MessagePriority.HIGH.value == "high"
    assert MessagePriority.URGENT.value == "urgent"
