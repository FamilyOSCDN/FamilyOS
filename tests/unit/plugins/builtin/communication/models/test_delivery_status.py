from familyos_cli.plugins.builtin.communication.models import (
    DeliveryStatus,
)


def test_delivery_status_values() -> None:
    assert DeliveryStatus.PENDING.value == "pending"
    assert DeliveryStatus.SENT.value == "sent"
    assert DeliveryStatus.DELIVERED.value == "delivered"
    assert DeliveryStatus.READ.value == "read"
    assert DeliveryStatus.FAILED.value == "failed"
