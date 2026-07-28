from pathlib import Path

from familyos_cli.application.specifications.domain_specification_loader_service import (
    DomainSpecificationLoaderService,
)
from familyos_cli.application.specifications.specification_service import (
    SpecificationService,
)
from familyos_cli.domain.specifications.domain_specification_registry import (
    DomainSpecificationRegistry,
)
from familyos_cli.infrastructure.specifications.yaml_domain_specification_loader import (
    YamlDomainSpecificationLoader,
)


def test_should_load_and_register_domain_specification(
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
      - first_name
      - last_name
    behaviors:
      - register

aggregates: []

repositories: []

services: []
""",
        encoding="utf-8",
    )

    registry = DomainSpecificationRegistry()

    specification_service = SpecificationService(
        registry,
    )

    service = DomainSpecificationLoaderService(
        loader=YamlDomainSpecificationLoader(),
        service=specification_service,
    )

    specification = service.load(
        specification_file,
    )

    assert specification.name == "Person"

    assert specification_service.contains(
        "Person",
    )

    registered = specification_service.get(
        "Person",
    )

    assert registered is not None
    assert registered.name == "Person"
