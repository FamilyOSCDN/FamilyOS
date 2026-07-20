"""Tests for InitCommand."""

from unittest.mock import Mock, patch

from familyos_cli.interfaces.cli.commands.init_command import (
    InitCommand,
)


@patch(
    "familyos_cli.interfaces.cli.commands.init_command.Output.success",
)
@patch(
    "familyos_cli.interfaces.cli.base_command.BaseCommand.__init__",
    return_value=None,
)
def test_execute_should_create_project(
    mock_base_init,
    mock_success,
) -> None:
    """Executing the command should create a project."""

    command = InitCommand()

    command.context = Mock()

    command.execute("demo")

    command.context.create_project.execute.assert_called_once_with(
        "demo",
    )

    mock_success.assert_called_once_with(
        'Project "demo" created successfully.',
    )