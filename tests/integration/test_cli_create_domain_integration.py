from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from familyos_cli.interfaces.cli.app import app

runner = CliRunner()


def test_cli_should_create_domain_from_yaml_specification(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """CLI should load a domain specification and generate its files."""

    monkeypatch.chdir(tmp_path)

    specification = tmp_path / "person.yaml"

    specification.write_text(
        """
domain:
  name: Person
  business_rules:
    - A person must have a stable identity.

entities:
  - name: Person
    description: Person entity

aggregates:
  - name: Person
    root_entity: Person
    description: Person aggregate

repositories:
  - name: PersonRepository
    aggregate: Person
    description: Person repository

services:
  - name: PersonService
    description: Person service
""".strip(),
        encoding="utf-8",
    )

    templates = tmp_path / "templates" / "domain"
    templates.mkdir(
        parents=True,
    )

    template_names = (
        "README.md.j2",
        "Vision.md.j2",
        "Capabilities.md.j2",
        "Domain-Model.md.j2",
    )

    for template_name in template_names:
        (templates / template_name).write_text(
            "# Generated domain documentation\n",
            encoding="utf-8",
        )

    destination = tmp_path / "generated"

    result = runner.invoke(
        app,
        [
            "create",
            "domain",
            "Person",
            "--specification",
            str(specification),
            "--destination",
            str(destination),
        ],
    )

    assert result.exit_code == 0, result.output

    assert (
        'Domain "Person" created successfully.'
        in result.output
    )

    domain_directory = (
        destination
        / "docs"
        / "30-domains"
        / "person"
    )

    expected_files = (
        "README.md",
        "Vision.md",
        "Capabilities.md",
        "Domain-Model.md",
    )

    for expected_file in expected_files:
        assert (
            domain_directory / expected_file
        ).is_file()


def test_cli_should_create_domain_context_documentation(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """CLI should generate domain context documentation."""

    monkeypatch.chdir(tmp_path)

    specification = tmp_path / "person.yaml"

    specification.write_text(
        """
domain:
  name: Person
  business_rules:
    - A person must have a stable identity.

entities:
  - name: Person
    description: Person entity

aggregates:
  - name: Person
    root_entity: Person
    description: Person aggregate

repositories:
  - name: PersonRepository
    aggregate: Person
    description: Person repository

services:
  - name: PersonService
    description: Person service
""".strip(),
        encoding="utf-8",
    )

    templates = (
        tmp_path
        / "templates"
        / "domain_context"
    )

    diagrams = templates / "diagrams"

    diagrams.mkdir(
        parents=True,
    )

    template_names = (
        "Context.md.j2",
        "Responsibilities.md.j2",
        "Integrations.md.j2",
        "Business-Rules.md.j2",
    )

    for template_name in template_names:
        (templates / template_name).write_text(
            "# Generated domain context documentation\n",
            encoding="utf-8",
        )

    (diagrams / "context-map.puml.j2").write_text(
        "@startuml\n@enduml\n",
        encoding="utf-8",
    )

    destination = tmp_path / "generated"

    result = runner.invoke(
        app,
        [
            "create",
            "domain",
            "Person",
            "--specification",
            str(specification),
            "--destination",
            str(destination),
            "--recipe",
            "domain_context_documentation",
        ],
    )

    assert result.exit_code == 0, result.output

    assert (
        'Domain "Person" created successfully.'
        in result.output
    )

    domain_directory = (
        destination
        / "docs"
        / "30-domains"
        / "person"
    )

    expected_files = (
        "Context.md",
        "Responsibilities.md",
        "Integrations.md",
        "Business-Rules.md",
        "diagrams/context-map.puml",
    )

    for expected_file in expected_files:
        assert (
            domain_directory / expected_file
        ).is_file()
