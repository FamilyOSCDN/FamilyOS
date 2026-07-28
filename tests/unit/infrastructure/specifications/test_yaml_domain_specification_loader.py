from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.infrastructure.specifications.yaml_domain_specification_loader import (
    YamlDomainSpecificationLoader,
)


def test_should_load_domain_specification_from_yaml(
    tmp_path: Path,
) -> None:
    specification_file = tmp_path / "person.yaml"

    specification_file.write_text(
        """
domain:
  name: Person
  description: Person domain

  responsibilities:
    - Manage person identity

  business_rules:
    - Person must have a unique identifier

entities:
  - name: Person
    description: Represents a person
    attributes:
      - first_name
      - last_name
    behaviors:
      - register

aggregates:
  - name: PersonAggregate
    description: Person aggregate
    root_entity: Person
    entities:
      - Person
    invariants:
      - Identifier must be unique

repositories:
  - name: PersonRepository
    description: Person repository
    aggregate: PersonAggregate
    operations:
      - save

services:
  - name: PersonService
    description: Person application service
    responsibilities:
      - Register person
        """,
        encoding="utf-8",
    )

    loader = YamlDomainSpecificationLoader()

    specification = loader.load(
        specification_file,
    )

    assert isinstance(
        specification,
        DomainSpecification,
    )

    assert specification.name == "Person"

    assert len(specification.entities) == 1
    assert specification.entities[0].name == "Person"

    assert len(specification.aggregates) == 1
    assert specification.aggregates[0].name == "PersonAggregate"

    assert len(specification.repositories) == 1
    assert specification.repositories[0].name == "PersonRepository"

    assert len(specification.services) == 1
    assert specification.services[0].name == "PersonService"
