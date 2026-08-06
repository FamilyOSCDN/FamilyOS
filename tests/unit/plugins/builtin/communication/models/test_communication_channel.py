from familyos_cli.plugins.builtin.communication.models import (
    CommunicationChannel,
)


def test_communication_channel_values() -> None:
    assert CommunicationChannel.EMAIL.value == "email"
    assert CommunicationChannel.SMS.value == "sms"
    assert CommunicationChannel.CHAT.value == "chat"
    assert CommunicationChannel.PHONE.value == "phone"
    assert CommunicationChannel.VIDEO.value == "video"
    assert CommunicationChannel.SOCIAL.value == "social"
