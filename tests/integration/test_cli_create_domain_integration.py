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


def test_cli_should_create_repository_documentation(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """CLI should generate repository documentation."""

    monkeypatch.chdir(tmp_path)

    specification = tmp_path / "person.yaml"

    specification.write_text(
        """
domain:
  name: Person

repositories:
  - name: PersonRepository
    aggregate: Person
    description: Person persistence repository
    operations:
      - save
      - find
""".strip(),
        encoding="utf-8",
    )

    templates = (
        tmp_path
        / "templates"
        / "repository"
    )

    diagrams = templates / "diagrams"

    diagrams.mkdir(
        parents=True,
    )

    template_names = (
        "README.md.j2",
        "Responsibilities.md.j2",
        "Operations.md.j2",
    )

    for template_name in template_names:
        (templates / template_name).write_text(
            "# Generated repository documentation\n",
            encoding="utf-8",
        )

    (diagrams / "persistence-flow.puml.j2").write_text(
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
            "repository_documentation",
        ],
    )

    assert result.exit_code == 0, result.output

    assert (
        'Domain "Person" created successfully.'
        in result.output
    )

    repository_directory = (
        destination
        / "docs"
        / "30-domains"
        / "person"
        / "repositories"
        / "personrepository"
    )

    expected_files = (
        "README.md",
        "Responsibilities.md",
        "Operations.md",
        "diagrams/persistence-flow.puml",
    )

    for expected_file in expected_files:
        assert (
            repository_directory / expected_file
        ).is_file()


def test_cli_should_create_service_documentation(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """CLI should generate service documentation."""

    monkeypatch.chdir(tmp_path)

    specification = tmp_path / "person.yaml"

    specification.write_text(
        """
domain:
  name: Person

services:
  - name: PersonService
    description: Person domain service
    responsibilities:
      - Manage person operations
      - Coordinate domain workflows
""".strip(),
        encoding="utf-8",
    )

    templates = (
        tmp_path
        / "templates"
        / "service"
    )

    diagrams = templates / "diagrams"

    diagrams.mkdir(
        parents=True,
    )

    template_names = (
        "README.md.j2",
        "Responsibilities.md.j2",
        "Operations.md.j2",
    )

    for template_name in template_names:
        (templates / template_name).write_text(
            "# Generated service documentation\n",
            encoding="utf-8",
        )

    (diagrams / "interaction-flow.puml.j2").write_text(
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
            "service_documentation",
        ],
    )

    assert result.exit_code == 0, result.output

    assert (
        'Domain "Person" created successfully.'
        in result.output
    )

    service_directory = (
        destination
        / "docs"
        / "30-domains"
        / "person"
        / "services"
        / "personservice"
    )

    expected_files = (
        "README.md",
        "Responsibilities.md",
        "Operations.md",
        "diagrams/interaction-flow.puml",
    )

    for expected_file in expected_files:
        assert (
            service_directory / expected_file
        ).is_file()


def test_cli_should_create_domain_using_complete_preset(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """CLI should generate a domain using complete preset."""

    monkeypatch.chdir(tmp_path)

    specification = tmp_path / "person.yaml"

    specification.write_text(
        """
domain:
  name: Person

entities:
  - name: Person
    description: Person entity
""".strip(),
        encoding="utf-8",
    )

    templates = (
        tmp_path
        / "templates"
    )

    artifacts = (
        "domain/README.md.j2",
        "domain/Vision.md.j2",
        "domain/Capabilities.md.j2",
        "domain/Domain-Model.md.j2",
    )

    for artifact in artifacts:
        template = templates / artifact
        template.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        template.write_text(
            "# Generated documentation\n",
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
            "--preset",
            "complete",
        ],
    )

    assert result.exit_code == 0, result.output

    assert (
        'Domain "Person" created successfully.'
        in result.output
    )
