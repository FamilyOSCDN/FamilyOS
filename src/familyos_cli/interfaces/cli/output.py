"""CLI output helpers."""

import typer


class Output:
    """Provide consistent CLI output."""

    @staticmethod
    def success(message: str) -> None:
        """Display a success message."""

        typer.secho(
            f"✅ {message}",
            fg=typer.colors.GREEN,
        )

    @staticmethod
    def error(message: str) -> None:
        """Display an error message."""

        typer.secho(
            f"❌ {message}",
            fg=typer.colors.RED,
            err=True,
        )

    @staticmethod
    def warning(message: str) -> None:
        """Display a warning message."""

        typer.secho(
            f"⚠️ {message}",
            fg=typer.colors.YELLOW,
        )

    @staticmethod
    def info(message: str) -> None:
        """Display an information message."""

        typer.secho(
            f"ℹ️ {message}",
            fg=typer.colors.BLUE,
        )