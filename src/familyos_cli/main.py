import typer

app = typer.Typer(
    name="familyos",
    help="FamilyOS CLI",
    no_args_is_help=True,
)


@app.command()
def version() -> None:
    """Display the CLI version."""
    typer.echo("FamilyOS CLI v0.1.0")


@app.command()
def init(name: str) -> None:
    """Initialize a new FamilyOS project."""
    typer.echo(f"Initializing project: {name}")


if __name__ == "__main__":
    app()