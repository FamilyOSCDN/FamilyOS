"""In-memory communication repository."""

from __future__ import annotations

from familyos_cli.plugins.builtin.communication.models import (
    Conversation,
)
from familyos_cli.plugins.builtin.communication.repositories.communication_repository import (
    CommunicationRepository,
)


class InMemoryCommunicationRepository(
    CommunicationRepository,
):
    """In-memory implementation of the communication repository."""

    def __init__(self) -> None:
        """Initialize the repository."""

        self._conversations: dict[
            str,
            Conversation,
        ] = {}

    def save(
        self,
        conversation: Conversation,
    ) -> None:
        """Persist a conversation."""

        self._conversations[
            conversation.identifier
        ] = conversation

    def get(
        self,
        identifier: str,
    ) -> Conversation | None:
        """Return a conversation."""

        return self._conversations.get(
            identifier,
        )

    def list(
        self,
    ) -> tuple[
        Conversation,
        ...,
    ]:
        """Return all conversations."""

        return tuple(
            self._conversations.values()
        )

    def delete(
        self,
        identifier: str,
    ) -> None:
        """Delete a conversation."""

        self._conversations.pop(
            identifier,
            None,
        )

    def exists(
        self,
        identifier: str,
    ) -> bool:
        """Return whether a conversation exists."""

        return (
            identifier
            in self._conversations
        )
