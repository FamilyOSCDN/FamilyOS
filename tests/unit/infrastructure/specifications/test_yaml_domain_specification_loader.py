from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.models.attribute_descriptor import (
    AttributeDescriptor,
)
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

  business_rules:
    - Person must have a unique identifier

entities:
  - name: Person
    description: Represents a person
    attributes:
      - name: first_name
        type: str
        required: true
      - name: last_name
        type: str
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

    entity = specification.entities[0]

    assert len(entity.attributes) == 2

    assert isinstance(
        entity.attributes[0],
        AttributeDescriptor,
    )

    assert entity.attributes[0].name == "first_name"

    assert entity.attributes[0].type == "str"

    assert entity.attributes[0].required is True
