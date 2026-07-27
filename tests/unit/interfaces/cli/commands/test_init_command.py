from __future__ import annotations

from unittest.mock import Mock, patch

from familyos_cli.interfaces.cli.commands.init_command import (
    InitCommand,
)


def test_should_initialize_project() -> None:
    command = InitCommand()

    command.context.create_project = Mock()

    with patch(
        "familyos_cli.interfaces.cli.commands.init_command.Output.success"
    ) as mock_output:
        command.execute(
            name="MyFamily",
        )

    command.context.create_project.execute.assert_called_once_with(
        "MyFamily",
    )

    mock_output.assert_called_once_with(
        'Project "MyFamily" created successfully.',
    )