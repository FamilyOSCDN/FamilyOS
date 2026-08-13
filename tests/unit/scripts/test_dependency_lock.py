"""Tests for deterministic dependency lock generation and verification."""

import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from scripts import check_dependency_lock, compile_dependencies


def _write_pyproject(
    path: Path,
    *,
    name: str = "familyos-cli",
    requires_python: str = ">=3.13",
    build_requires: tuple[str, ...] = ("setuptools>=75", "wheel"),
    build_backend: str = "setuptools.build_meta",
    dependencies: tuple[str, ...] = ("typer>=0.16",),
    dev_dependencies: tuple[str, ...] = ("pytest>=8.4", "pip-tools==7.6.1"),
) -> None:
    def toml_list(values: tuple[str, ...]) -> str:
        return ", ".join(f'"{value}"' for value in values)

    path.write_text(
        "\n".join(
            (
                "[build-system]",
                f"requires = [{toml_list(build_requires)}]",
                f'build-backend = "{build_backend}"',
                "",
                "[project]",
                f'name = "{name}"',
                'version = "0.1.0"',
                f'requires-python = "{requires_python}"',
                f"dependencies = [{toml_list(dependencies)}]",
                "",
                "[project.optional-dependencies]",
                f"dev = [{toml_list(dev_dependencies)}]",
                "",
            ),
        ),
        encoding="utf-8",
    )


def test_supported_python_version_is_accepted() -> None:
    compile_dependencies.require_supported_python((3, 13))


def test_unsupported_python_version_is_rejected() -> None:
    with pytest.raises(RuntimeError, match="requires Python 3.13; found 3.14"):
        compile_dependencies.require_supported_python((3, 14))


def test_dependency_input_digest_is_deterministic(tmp_path: Path) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    _write_pyproject(pyproject_path)

    first = compile_dependencies.dependency_input_digest(pyproject_path)
    second = compile_dependencies.dependency_input_digest(pyproject_path)

    assert first == second
    assert len(first) == 64


def test_irrelevant_metadata_does_not_change_digest(tmp_path: Path) -> None:
    first_path = tmp_path / "first.toml"
    second_path = tmp_path / "second.toml"
    _write_pyproject(first_path, name="first-name")
    _write_pyproject(second_path, name="second-name")

    assert compile_dependencies.dependency_input_digest(
        first_path,
    ) == compile_dependencies.dependency_input_digest(second_path)


def test_compatible_direct_constraint_change_alters_digest(tmp_path: Path) -> None:
    first_path = tmp_path / "first.toml"
    second_path = tmp_path / "second.toml"
    _write_pyproject(first_path, dependencies=("typer>=0.16",))
    _write_pyproject(second_path, dependencies=("typer>=0.20",))

    assert compile_dependencies.dependency_input_digest(
        first_path,
    ) != compile_dependencies.dependency_input_digest(second_path)


def test_dev_dependency_change_alters_digest(tmp_path: Path) -> None:
    first_path = tmp_path / "first.toml"
    second_path = tmp_path / "second.toml"
    _write_pyproject(first_path)
    _write_pyproject(
        second_path,
        dev_dependencies=("pytest>=9", "pip-tools==7.6.1"),
    )

    assert compile_dependencies.dependency_input_digest(
        first_path,
    ) != compile_dependencies.dependency_input_digest(second_path)


def test_requires_python_change_alters_digest(tmp_path: Path) -> None:
    first_path = tmp_path / "first.toml"
    second_path = tmp_path / "second.toml"
    _write_pyproject(first_path, requires_python=">=3.13")
    _write_pyproject(second_path, requires_python=">=3.13,<3.14")

    assert compile_dependencies.dependency_input_digest(
        first_path,
    ) != compile_dependencies.dependency_input_digest(second_path)


@pytest.mark.parametrize(
    ("overrides"),
    (
        {"build_requires": ("setuptools>=76", "wheel")},
        {"build_backend": "another.backend"},
    ),
)
def test_build_system_change_alters_digest(
    tmp_path: Path,
    overrides: dict[str, Any],
) -> None:
    first_path = tmp_path / "first.toml"
    second_path = tmp_path / "second.toml"
    _write_pyproject(first_path)
    _write_pyproject(second_path, **overrides)

    assert compile_dependencies.dependency_input_digest(
        first_path,
    ) != compile_dependencies.dependency_input_digest(second_path)


def test_compile_command_is_deterministic(tmp_path: Path) -> None:
    output_path = tmp_path / "requirements.txt"

    command = compile_dependencies.build_compile_command(output_path)

    assert command == (
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
        compile_dependencies.PYPROJECT_ARGUMENT,
    )


def test_matching_pip_tools_version_succeeds(tmp_path: Path) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    _write_pyproject(pyproject_path)

    compile_dependencies.require_matching_pip_tools(
        pyproject_path,
        installed_version="7.6.1",
    )


def test_mismatched_pip_tools_version_fails(tmp_path: Path) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    _write_pyproject(pyproject_path)

    with pytest.raises(RuntimeError, match="7.5.0 does not satisfy"):
        compile_dependencies.require_matching_pip_tools(
            pyproject_path,
            installed_version="7.5.0",
        )


def test_input_digest_drift_fails_before_compilation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lock_path = tmp_path / "requirements.txt"
    lock_path.write_text(
        f"{compile_dependencies.DEPENDENCY_DIGEST_PREFIX}{'0' * 64}\nresolved\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        check_dependency_lock,
        "dependency_input_digest",
        lambda: "1" * 64,
    )

    def unexpected_generation(output_path: Path) -> None:
        pytest.fail(f"unexpected generation of {output_path}")

    monkeypatch.setattr(
        check_dependency_lock,
        "compile_dependencies",
        unexpected_generation,
    )

    with pytest.raises(check_dependency_lock.DependencyInputDriftError):
        check_dependency_lock.check_dependency_lock(lock_path)


def test_tracked_lock_is_copied_before_seeded_compilation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    digest = "a" * 64
    tracked_content = (
        f"{compile_dependencies.DEPENDENCY_DIGEST_PREFIX}{digest}\nresolved\n"
    )
    lock_path = tmp_path / "requirements.txt"
    lock_path.write_text(tracked_content, encoding="utf-8")
    monkeypatch.setattr(
        check_dependency_lock,
        "dependency_input_digest",
        lambda: digest,
    )

    def verify_seed(output_path: Path) -> None:
        assert output_path.read_text(encoding="utf-8") == tracked_content

    monkeypatch.setattr(check_dependency_lock, "compile_dependencies", verify_seed)

    check_dependency_lock.check_dependency_lock(lock_path)


def test_resolved_dependency_drift_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    digest = "b" * 64
    lock_path = tmp_path / "requirements.txt"
    lock_path.write_text(
        f"{compile_dependencies.DEPENDENCY_DIGEST_PREFIX}{digest}\ntracked\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        check_dependency_lock,
        "dependency_input_digest",
        lambda: digest,
    )

    def generate(output_path: Path) -> None:
        output_path.write_text("generated\n", encoding="utf-8")

    monkeypatch.setattr(check_dependency_lock, "compile_dependencies", generate)

    with pytest.raises(check_dependency_lock.ResolvedLockDriftError):
        check_dependency_lock.check_dependency_lock(lock_path)


def test_generator_subprocess_failure_propagates(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(compile_dependencies, "require_matching_pip_tools", lambda: None)

    def fail(*args: object, **kwargs: object) -> None:
        raise subprocess.CalledProcessError(1, ["piptools"])

    monkeypatch.setattr("scripts.compile_dependencies.subprocess.run", fail)

    with pytest.raises(subprocess.CalledProcessError):
        compile_dependencies.compile_dependencies(tmp_path / "requirements.txt")


def test_generated_header_contains_dependency_input_digest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_path = tmp_path / "requirements.txt"
    digest = "c" * 64
    monkeypatch.setattr(compile_dependencies, "require_matching_pip_tools", lambda: None)
    monkeypatch.setattr(compile_dependencies, "dependency_input_digest", lambda: digest)

    def generate(command: tuple[str, ...], **kwargs: object) -> None:
        del kwargs
        generated_path = Path(command[command.index("--output-file") + 1])
        generated_path.write_text("#\npackage==1.0\n", encoding="utf-8")

    monkeypatch.setattr("scripts.compile_dependencies.subprocess.run", generate)

    compile_dependencies.compile_dependencies(output_path)

    content = output_path.read_text(encoding="utf-8")
    assert compile_dependencies.GENERATED_WARNING in content
    assert f"{compile_dependencies.DEPENDENCY_DIGEST_PREFIX}{digest}\n" in content


def test_read_only_check_does_not_modify_tracked_lock(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    digest = "d" * 64
    lock_path = tmp_path / "requirements.txt"
    original_content = (
        f"{compile_dependencies.DEPENDENCY_DIGEST_PREFIX}{digest}\ntracked\n"
    ).encode()
    lock_path.write_bytes(original_content)
    monkeypatch.setattr(
        check_dependency_lock,
        "dependency_input_digest",
        lambda: digest,
    )

    def generate(output_path: Path) -> None:
        output_path.write_bytes(b"generated\n")

    monkeypatch.setattr(check_dependency_lock, "compile_dependencies", generate)

    with pytest.raises(check_dependency_lock.ResolvedLockDriftError):
        check_dependency_lock.check_dependency_lock(lock_path)
    assert lock_path.read_bytes() == original_content
