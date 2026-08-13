"""Generate the pinned FamilyOS development dependency state."""

from __future__ import annotations

import os
import subprocess
import sys
import tomllib
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
from json import dumps
from pathlib import Path
from typing import Any, Final

from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.utils import canonicalize_name
from packaging.version import InvalidVersion, Version

PROJECT_ROOT: Final = Path(__file__).resolve().parent.parent
PYPROJECT_ARGUMENT: Final = "pyproject.toml"
PYPROJECT_PATH: Final = PROJECT_ROOT / PYPROJECT_ARGUMENT
LOCK_PATH: Final = PROJECT_ROOT / "requirements.txt"
SUPPORTED_PYTHON: Final = (3, 13)
DEPENDENCY_DIGEST_PREFIX: Final = "# Dependency-Input-SHA256: "
GENERATED_WARNING: Final = (
    "# DO NOT EDIT: generated from pyproject.toml by "
    "scripts/compile_dependencies.py.\n"
)


def require_supported_python(
    version_info: tuple[int, int] | None = None,
) -> None:
    """Require the Python version used by the dependency lock."""

    effective_version = version_info or sys.version_info[:2]
    if effective_version != SUPPORTED_PYTHON:
        expected = ".".join(str(part) for part in SUPPORTED_PYTHON)
        actual = ".".join(str(part) for part in effective_version)
        raise RuntimeError(
            f"Dependency generation requires Python {expected}; found {actual}.",
        )


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


def canonical_dependency_inputs(pyproject_path: Path = PYPROJECT_PATH) -> dict[str, Any]:
    """Load and normalize only canonical dependency-relevant project inputs."""

    with pyproject_path.open("rb") as pyproject_file:
        project_data = tomllib.load(pyproject_file)

    project = project_data["project"]
    build_system = project_data["build-system"]
    optional_dependencies = project["optional-dependencies"]

    return {
        "build-system": {
            "build-backend": build_system["build-backend"],
            "requires": sorted(
                _canonical_requirement(item) for item in build_system["requires"]
            ),
        },
        "project": {
            "dependencies": sorted(
                _canonical_requirement(item) for item in project["dependencies"]
            ),
            "optional-dependencies": {
                "dev": sorted(
                    _canonical_requirement(item) for item in optional_dependencies["dev"]
                ),
            },
            "requires-python": str(SpecifierSet(project["requires-python"])),
        },
    }


def dependency_input_digest(pyproject_path: Path = PYPROJECT_PATH) -> str:
    """Hash the normalized canonical dependency inputs."""

    canonical_json = dumps(
        canonical_dependency_inputs(pyproject_path),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )
    return sha256(canonical_json.encode("utf-8")).hexdigest()


def pip_tools_requirement(pyproject_path: Path = PYPROJECT_PATH) -> Requirement:
    """Return the single supported pip-tools declaration from the dev extra."""

    with pyproject_path.open("rb") as pyproject_file:
        project_data = tomllib.load(pyproject_file)

    declarations = [
        Requirement(item)
        for item in project_data["project"]["optional-dependencies"]["dev"]
        if canonicalize_name(Requirement(item).name) == "pip-tools"
    ]
    if len(declarations) != 1:
        raise RuntimeError(
            "pyproject.toml must declare pip-tools exactly once in the dev extra.",
        )

    requirement = declarations[0]
    if (
        requirement.extras
        or requirement.marker is not None
        or requirement.url is not None
        or not requirement.specifier
    ):
        raise RuntimeError(
            "The pip-tools dev declaration must use one unconditional version specifier.",
        )
    return requirement


def require_matching_pip_tools(
    pyproject_path: Path = PYPROJECT_PATH,
    installed_version: str | None = None,
) -> None:
    """Require the executing pip-tools to satisfy its canonical declaration."""

    try:
        requirement = pip_tools_requirement(pyproject_path)
        actual_text = installed_version or version("pip-tools")
        actual_version = Version(actual_text)
    except PackageNotFoundError as error:
        raise RuntimeError(
            "pip-tools is unavailable; install the generated requirements.txt first.",
        ) from error
    except (InvalidRequirement, InvalidSpecifier, InvalidVersion) as error:
        raise RuntimeError(f"Invalid pip-tools version contract: {error}") from error

    if not requirement.specifier.contains(actual_version, prereleases=True):
        raise RuntimeError(
            f"Executing pip-tools {actual_version} does not satisfy "
            f"'{requirement}'.",
        )


def build_compile_command(output_path: Path) -> tuple[str, ...]:
    """Build the deterministic pip-tools compilation command."""

    return (
        sys.executable,
        "-m",
        "piptools",
        "compile",
        "--quiet",
        "--extra",
        "dev",
        "--all-build-deps",
        "--strip-extras",
        "--allow-unsafe",
        "--resolver",
        "backtracking",
        "--annotation-style",
        "split",
        "--newline",
        "lf",
        "--no-emit-index-url",
        "--no-emit-trusted-host",
        "--output-file",
        str(output_path),
        PYPROJECT_ARGUMENT,
    )


def compile_dependencies(output_path: Path = LOCK_PATH) -> None:
    """Compile dependency declarations into an exact resolved state."""

    require_supported_python()
    require_matching_pip_tools()
    environment = os.environ.copy()
    environment["CUSTOM_COMPILE_COMMAND"] = "python scripts/compile_dependencies.py"
    subprocess.run(
        build_compile_command(output_path),
        check=True,
        cwd=PROJECT_ROOT,
        env=environment,
    )
    generated_content = output_path.read_text(encoding="utf-8")
    generated_header = (
        f"{GENERATED_WARNING}"
        f"{DEPENDENCY_DIGEST_PREFIX}{dependency_input_digest()}\n"
    )
    output_path.write_text(
        generated_content.replace("#\n", f"#\n{generated_header}", 1),
        encoding="utf-8",
    )


def main() -> int:
    """Regenerate the tracked dependency lock."""

    try:
        compile_dependencies()
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"Dependency generation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
