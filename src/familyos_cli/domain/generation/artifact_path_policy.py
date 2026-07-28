"""Artifact path generation policies."""

from __future__ import annotations

import re
from typing import Protocol

from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)


class ArtifactPathPolicy(Protocol):
    """Define how artifact target paths are created."""

    def path_for(
        self,
        kind: ArtifactKind,
        name: str,
    ) -> str:
        """Return the target path for an artifact."""


class DefaultArtifactPathPolicy:
    """Build conventional target paths for generated artifacts."""

    _DIRECTORIES: dict[ArtifactKind, str] = {
        ArtifactKind.ENTITY: "models",
        ArtifactKind.VALUE_OBJECT: "value_objects",
        ArtifactKind.AGGREGATE: "aggregates",
        ArtifactKind.REPOSITORY: "repositories",
        ArtifactKind.SERVICE: "services",
        ArtifactKind.README: "",
        ArtifactKind.DOCUMENTATION: "docs",
        ArtifactKind.TEST: "tests",
        ArtifactKind.TEMPLATE: "templates",
    }

    def path_for(
        self,
        kind: ArtifactKind,
        name: str,
    ) -> str:
        """Return the target path for an artifact."""

        directory = self._DIRECTORIES[kind]
        filename = self._filename_for(
            kind=kind,
            name=name,
        )

        if not directory:
            return filename

        return f"{directory}/{filename}"

    def _filename_for(
        self,
        *,
        kind: ArtifactKind,
        name: str,
    ) -> str:
        """Return the filename for an artifact."""

        if kind is ArtifactKind.README:
            return "README.md"

        if kind is ArtifactKind.DOCUMENTATION:
            return f"{self._to_kebab_case(name)}.md"

        if kind is ArtifactKind.TEMPLATE:
            return f"{self._to_snake_case(name)}.jinja"

        return f"{self._to_snake_case(name)}.py"

    def _to_snake_case(
        self,
        value: str,
    ) -> str:
        """Convert a name to snake case."""

        normalized = re.sub(
            r"([A-Z]+)([A-Z][a-z])",
            r"\1_\2",
            value,
        )
        normalized = re.sub(
            r"([a-z0-9])([A-Z])",
            r"\1_\2",
            normalized,
        )
        normalized = re.sub(
            r"[\s\-]+",
            "_",
            normalized,
        )

        return normalized.strip("_").lower()

    def _to_kebab_case(
        self,
        value: str,
    ) -> str:
        """Convert a name to kebab case."""

        return self._to_snake_case(value).replace("_", "-")
