"""Tests for CLI command context."""

from familyos_cli.application.use_cases.create_project import (
    CreateProjectUseCase,
)
from familyos_cli.interfaces.cli.context import CommandContext


def test_context_should_provide_create_project_use_case() -> None:
    """The command context should expose the project use case."""

    context = CommandContext()

    assert isinstance(
        context.create_project,
        CreateProjectUseCase,
    )