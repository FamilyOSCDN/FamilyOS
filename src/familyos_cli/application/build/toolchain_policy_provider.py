"""Resolve canonical build-toolchain policy from project configuration."""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any

from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.utils import canonicalize_name
from packaging.version import InvalidVersion, Version

from familyos_cli.application.build.toolchain_policy import (
    ToolchainDistributionRequirement,
    ToolchainPolicy,
)

_CRITICAL_DISTRIBUTIONS = (
    "build",
    "pip-tools",
    "setuptools",
    "wheel",
)


class ToolchainPolicyProvider:
    """Resolve critical build-tool requirements from canonical metadata."""

    def resolve(
        self,
        *,
        project_root: Path,
    ) -> ToolchainPolicy:
        """Resolve one canonical toolchain policy from pyproject.toml."""

        pyproject_path = project_root / "pyproject.toml"

        try:
            with pyproject_path.open("rb") as pyproject_file:
                document = tomllib.load(pyproject_file)
        except (OSError, tomllib.TOMLDecodeError) as error:
            raise ValueError(
                "canonical toolchain policy requires valid pyproject.toml",
            ) from error

        runtime_requirement = self._runtime_requirement(document)

        build_requirements = self._requirements_by_name(
            self._required_string_list(
                document,
                ("build-system", "requires"),
                diagnostic=(
                    "pyproject.toml [build-system].requires "
                    "must be a non-empty string list"
                ),
            )
        )

        development_requirements = self._requirements_by_name(
            self._required_string_list(
                document,
                (
                    "project",
                    "optional-dependencies",
                    "dev",
                ),
                diagnostic=(
                    "pyproject.toml project.optional-dependencies.dev "
                    "must be a non-empty string list"
                ),
            )
        )

        requirements = (
            ToolchainDistributionRequirement(
                distribution="build",
                requirement=self._required_requirement(
                    development_requirements,
                    "build",
                ),
            ),
            ToolchainDistributionRequirement(
                distribution="pip-tools",
                requirement=self._required_requirement(
                    development_requirements,
                    "pip-tools",
                ),
            ),
            ToolchainDistributionRequirement(
                distribution="setuptools",
                requirement=self._required_requirement(
                    build_requirements,
                    "setuptools",
                ),
            ),
            ToolchainDistributionRequirement(
                distribution="wheel",
                requirement=self._required_requirement(
                    build_requirements,
                    "wheel",
                ),
            ),
        )

        assert tuple(
            item.distribution
            for item in requirements
        ) == _CRITICAL_DISTRIBUTIONS

        return ToolchainPolicy(
            runtime_requirement=runtime_requirement,
            distribution_requirements=requirements,
        )

    def _runtime_requirement(
        self,
        document: dict[str, Any],
    ) -> str:
        mypy = self._nested_value(
            document,
            ("tool", "mypy"),
        )

        if not isinstance(mypy, dict):
            raise ValueError(
                "pyproject.toml [tool.mypy] table is required "
                "for canonical build runtime policy",
            )

        configured_runtime = mypy.get("python_version")

        if (
            not isinstance(configured_runtime, str)
            or not configured_runtime.strip()
        ):
            raise ValueError(
                "pyproject.toml tool.mypy.python_version "
                "must be a non-empty string",
            )

        try:
            runtime = Version(configured_runtime)
        except InvalidVersion as error:
            raise ValueError(
                "pyproject.toml tool.mypy.python_version is invalid",
            ) from error

        if runtime.micro != 0:
            raise ValueError(
                "canonical build runtime must identify a Python minor version",
            )

        upper_minor = runtime.minor + 1
        canonical_requirement = (
            f">={runtime.major}.{runtime.minor},"
            f"<{runtime.major}.{upper_minor}"
        )

        project = self._nested_value(
            document,
            ("project",),
        )

        if not isinstance(project, dict):
            raise ValueError(
                "pyproject.toml [project] table is required "
                "for canonical toolchain policy",
            )

        declared_runtime = project.get("requires-python")
        if (
            not isinstance(declared_runtime, str)
            or not declared_runtime.strip()
        ):
            raise ValueError(
                "pyproject.toml project.requires-python "
                "must be a non-empty string",
            )

        try:
            project_specifier = SpecifierSet(declared_runtime)
        except InvalidSpecifier as error:
            raise ValueError(
                "pyproject.toml project.requires-python is invalid",
            ) from error

        canonical_version = Version(
            f"{runtime.major}.{runtime.minor}.0"
        )

        if not project_specifier.contains(
            canonical_version,
            prereleases=True,
        ):
            raise ValueError(
                "canonical build runtime does not satisfy "
                "project.requires-python",
            )

        return canonical_requirement

    def _requirements_by_name(
        self,
        values: list[str],
    ) -> dict[str, Requirement]:
        requirements: dict[str, Requirement] = {}

        for value in values:
            try:
                requirement = Requirement(value)
            except InvalidRequirement as error:
                raise ValueError(
                    f"invalid canonical toolchain requirement: {value!r}",
                ) from error

            name = canonicalize_name(requirement.name)

            if name in requirements:
                raise ValueError(
                    f"duplicate canonical toolchain requirement: {name}",
                )

            requirements[name] = requirement

        return requirements

    @staticmethod
    def _required_requirement(
        requirements: dict[str, Requirement],
        distribution: str,
    ) -> str:
        canonical_name = canonicalize_name(distribution)
        requirement = requirements.get(canonical_name)

        if requirement is None:
            raise ValueError(
                f"required canonical toolchain declaration "
                f"{distribution!r} is missing",
            )

        if (
            requirement.extras
            or requirement.marker is not None
            or requirement.url is not None
        ):
            raise ValueError(
                f"canonical toolchain declaration "
                f"{distribution!r} must be unconditional",
            )

        return str(requirement.specifier)

    @classmethod
    def _required_string_list(
        cls,
        document: dict[str, Any],
        keys: tuple[str, ...],
        *,
        diagnostic: str,
    ) -> list[str]:
        value = cls._nested_value(
            document,
            keys,
        )

        if (
            not isinstance(value, list)
            or not value
            or not all(
                isinstance(item, str) and bool(item.strip())
                for item in value
            )
        ):
            raise ValueError(diagnostic)

        return value

    @staticmethod
    def _nested_value(
        document: dict[str, Any],
        keys: tuple[str, ...],
    ) -> Any:
        current: Any = document

        for key in keys:
            if not isinstance(current, dict):
                return None
            current = current.get(key)

        return current
