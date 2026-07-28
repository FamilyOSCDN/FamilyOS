"""YAML implementation of the domain specification repository."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)
from familyos_cli.domain.specifications.domain_specification_repository import (
    DomainSpecificationRepository,
)
from familyos_cli.infrastructure.specifications.yaml_domain_specification_loader import (
    YamlDomainSpecificationLoader,
)


class YamlDomainSpecificationRepository(
    DomainSpecificationRepository,
):
    """Repository backed by YAML specification files."""

    def __init__(
        self,
        root: Path,
    ) -> None:
        self._root = root
        self._loader = YamlDomainSpecificationLoader()

    def load(
        self,
        name: str,
    ) -> DomainSpecification:
        """Load a specification by name."""

        return self._loader.load(
            self._root / f"{name}.yaml",
        )

    def exists(
        self,
        name: str,
    ) -> bool:
        """Return whether a specification exists."""

        return (self._root / f"{name}.yaml").exists()
