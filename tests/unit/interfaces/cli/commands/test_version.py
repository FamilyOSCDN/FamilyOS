from __future__ import annotations

from unittest.mock import patch

from familyos_cli.interfaces.cli.commands.version import (
    version,
)


def test_should_display_version() -> None:
    with patch(
        "familyos_cli.interfaces.cli.commands.version.typer.echo"
    ) as mock_echo:
        version()

    mock_echo.assert_called_once_with(
        "FamilyOS CLI v0.1.0",
    )