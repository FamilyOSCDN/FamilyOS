"""Communication repositories."""

from familyos_cli.plugins.builtin.communication.repositories.communication_repository import (
    CommunicationRepository,
)
from familyos_cli.plugins.builtin.communication.repositories.in_memory_communication_repository import (
    InMemoryCommunicationRepository,
)

__all__ = [
    "CommunicationRepository",
    "InMemoryCommunicationRepository",
]
