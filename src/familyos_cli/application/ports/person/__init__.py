"""Application ports for the canonical Person domain."""

from familyos_cli.application.ports.person.person_repository import (
    PersonConflictError,
    PersonRepository,
)

__all__ = ["PersonConflictError", "PersonRepository"]
