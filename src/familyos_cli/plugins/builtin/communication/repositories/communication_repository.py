"""Communication repository abstraction."""

from __future__ import annotations

from abc import ABC, abstractmethod

from familyos_cli.plugins.builtin.communication.models import (
    Conversation,
)


class CommunicationRepository(ABC):
    """Repository abstraction for communication conversations."""

    @abstractmethod
    def save(
        self,
        conversation: Conversation,
    ) -> None:
        """Persist a conversation."""

    @abstractmethod
    def get(
        self,
        identifier: str,
    ) -> Conversation | None:
        """Return one conversation."""

    @abstractmethod
    def list(
        self,
    ) -> tuple[Conversation, ...]:
        """Return all conversations."""

    @abstractmethod
    def delete(
        self,
        identifier: str,
    ) -> None:
        """Delete one conversation."""

    @abstractmethod
    def exists(
        self,
        identifier: str,
    ) -> bool:
        """Return whether a conversation exists."""
