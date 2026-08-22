"""Canonical dependency-input freshness validation."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from hashlib import sha256
from json import dumps
from pathlib import Path
from re import MULTILINE, search
from typing import Any, Final

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.utils import canonicalize_name

DEPENDENCY_DIGEST_PREFIX: Final = "# Dependency-Input-SHA256: "


@dataclass(frozen=True, slots=True)
class DependencyInputFreshnessResult:
    """Result of comparing dependency inputs with the generated lock."""

    successful: bool
    diagnostic: str | None = None


def _canonical_requirement(requirement_text: str) -> str:
    """Return a stable representation of one PEP 508 requirement."""

    requirement = Requirement(requirement_text)
    name = canonicalize_name(requirement.name)

    extras = ""
    if requirement.extras:
        extras = f"[{','.join(sorted(requirement.extras))}]"

    constraint = str(requirement.specifier)
    url = f" @ {requirement.url}" if requirement.url else ""
    marker = f"; {requirement.marker}" if requirement.marker else ""

    return f"{name}{extras}{constraint}{url}{marker}"


def canonical_dependency_inputs(
    pyproject_path: Path,
) -> dict[str, Any]:
    """Load and normalize canonical dependency-relevant project inputs."""

    with pyproject_path.open("rb") as pyproject_file:
        project_data = tomllib.load(pyproject_file)

    project = project_data["project"]
    build_system = project_data["build-system"]
    optional_dependencies = project["optional-dependencies"]

    return {
        "build-system": {
            "build-backend": build_system["build-backend"],
            "requires": sorted(
                _canonical_requirement(item)
                for item in build_system["requires"]
            ),
        },
        "project": {
            "dependencies": sorted(
                _canonical_requirement(item)
                for item in project["dependencies"]
            ),
            "optional-dependencies": {
                "dev": sorted(
                    _canonical_requirement(item)
                    for item in optional_dependencies["dev"]
                ),
            },
            "requires-python": str(
                SpecifierSet(project["requires-python"])
            ),
        },
    }


def dependency_input_digest(
    pyproject_path: Path,
) -> str:
    """Hash normalized canonical dependency inputs."""

    canonical_json = dumps(
        canonical_dependency_inputs(pyproject_path),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )

    return sha256(
        canonical_json.encode("utf-8"),
    ).hexdigest()


def validate_dependency_input_freshness(
    *,
    pyproject_path: Path,
    requirements_path: Path,
) -> DependencyInputFreshnessResult:
    """Require generated dependency input state to match pyproject.toml."""

    try:
        tracked_content = requirements_path.read_text(
            encoding="utf-8",
        )
        current_digest = dependency_input_digest(
            pyproject_path,
        )
    except (
        OSError,
        KeyError,
        TypeError,
        ValueError,
        tomllib.TOMLDecodeError,
    ) as error:
        return DependencyInputFreshnessResult(
            successful=False,
            diagnostic=(
                "unable to validate generated dependency input freshness: "
                f"{error}"
            ),
        )

    digest_match = search(
        rf"^{DEPENDENCY_DIGEST_PREFIX}([0-9a-f]{{64}})$",
        tracked_content,
        flags=MULTILINE,
    )

    if digest_match is None:
        return DependencyInputFreshnessResult(
            successful=False,
            diagnostic=(
                "generated dependency input requirements.txt "
                "does not contain its canonical dependency digest"
            ),
        )

    if digest_match.group(1) != current_digest:
        return DependencyInputFreshnessResult(
            successful=False,
            diagnostic=(
                "generated dependency input requirements.txt is stale; "
                "regenerate requirements.txt"
            ),
        )

    return DependencyInputFreshnessResult(
        successful=True,
    )
