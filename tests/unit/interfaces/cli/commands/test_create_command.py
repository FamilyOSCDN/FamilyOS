from __future__ import annotations

from unittest.mock import Mock, patch

from familyos_cli.interfaces.cli.commands.create_command import (
    CreateCommand,
)


def test_should_create_artifact() -> None:
    command = CreateCommand()

    command.context.create_artifact = Mock()

    with patch(
        "familyos_cli.interfaces.cli.commands.create_command.Output.success"
    ) as mock_output:
        command.execute(
            artifact_type="domain",
            name="Person",
        )

    command.context.create_artifact.execute.assert_called_once_with(
        artifact_type="domain",
        name="Person",
    )

    mock_output.assert_called_once_with(
        'Domain "Person" created successfully.',
    )