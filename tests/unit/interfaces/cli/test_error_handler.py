"""Tests for CLI error handler."""

from unittest.mock import patch

import pytest
import typer

from familyos_cli.interfaces.cli.error_handler import ErrorHandler
from familyos_cli.shared.exceptions import FamilyOSError


def test_handle_should_exit() -> None:
    """Handling an error should terminate the CLI."""

    error = FamilyOSError("Boom")

    with (
        patch(
            "familyos_cli.interfaces.cli.error_handler.Output.error",
        ) as output,
        pytest.raises(typer.Exit),
    ):
        ErrorHandler.handle(error)

    output.assert_called_once_with("Boom")