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

    @staticmethod
    def diagnostic(
        message: str,
        *,
        styled: bool = False,
    ) -> None:
        """Display an already rendered diagnostic on stderr.

        Args:
            message: Pre-rendered multiline diagnostic.
            styled: Whether to apply optional terminal styling to the
                diagnostic heading.

        Plain-text output remains the default so callers and tests can
        preserve deterministic rendered diagnostics independently from
        terminal capabilities.
        """

        if not styled:
            typer.echo(
                message,
                err=True,
            )
            return

        heading, separator, remainder = message.partition(
            "\n",
        )

        typer.secho(
            heading,
            fg=typer.colors.RED,
            bold=True,
            err=True,
        )

        if separator:
            typer.echo(
                remainder,
                err=True,
            )
