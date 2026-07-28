from __future__ import annotations

from familyos_cli.interfaces.cli.context import CommandContext


def test_should_initialize_command_context() -> None:
    context = CommandContext()

    assert context.create_project is not None
    assert context.create_artifact is not None
