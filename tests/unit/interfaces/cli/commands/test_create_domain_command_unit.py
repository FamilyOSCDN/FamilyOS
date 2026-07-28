from familyos_cli.interfaces.cli.commands.create_domain import (
    create_domain,
)


def test_create_domain_command_exists() -> None:
    assert callable(create_domain)
