"""Tests for canonical build dependency state."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.dependency_state_provider import (
    DependencyStateProvider,
)


def _write_inputs(root: Path) -> tuple[Path, Path]:
    declaration = root / "pyproject.toml"
    lock = root / "requirements.txt"

    declaration.write_text(
        '[project]\ndependencies = ["typer>=0.26"]\n',
        encoding="utf-8",
    )
    lock.write_text(
        "typer==0.26.8\n",
        encoding="utf-8",
    )

    return declaration, lock


def test_dependency_state_is_immutable(tmp_path: Path) -> None:
    declaration, lock = _write_inputs(tmp_path)

    state = DependencyState(
        declaration_path=declaration,
        declaration_digest="a" * 64,
        lock_path=lock,
        lock_digest="b" * 64,
    )

    with pytest.raises(FrozenInstanceError):
        state.lock_digest = "c" * 64  # type: ignore[misc]


def test_dependency_state_rejects_empty_declaration_digest(
    tmp_path: Path,
) -> None:
    declaration, lock = _write_inputs(tmp_path)

    with pytest.raises(
        ValueError,
        match="dependency declaration digest must not be empty",
    ):
        DependencyState(
            declaration_path=declaration,
            declaration_digest="",
            lock_path=lock,
            lock_digest="b" * 64,
        )


def test_dependency_state_rejects_empty_lock_digest(
    tmp_path: Path,
) -> None:
    declaration, lock = _write_inputs(tmp_path)

    with pytest.raises(
        ValueError,
        match="dependency lock digest must not be empty",
    ):
        DependencyState(
            declaration_path=declaration,
            declaration_digest="a" * 64,
            lock_path=lock,
            lock_digest="",
        )


def test_provider_captures_canonical_dependency_inputs(
    tmp_path: Path,
) -> None:
    declaration, lock = _write_inputs(tmp_path)

    state = DependencyStateProvider().capture(project_root=tmp_path)

    assert state.declaration_path == declaration.resolve()
    assert state.lock_path == lock.resolve()
    assert len(state.declaration_digest) == 64
    assert len(state.lock_digest) == 64


def test_provider_is_deterministic(tmp_path: Path) -> None:
    _write_inputs(tmp_path)

    provider = DependencyStateProvider()

    first = provider.capture(project_root=tmp_path)
    second = provider.capture(project_root=tmp_path)

    assert first == second


def test_declaration_byte_change_changes_dependency_state(
    tmp_path: Path,
) -> None:
    declaration, _ = _write_inputs(tmp_path)
    provider = DependencyStateProvider()

    before = provider.capture(project_root=tmp_path)

    declaration.write_bytes(declaration.read_bytes() + b"\n")

    after = provider.capture(project_root=tmp_path)

    assert after.declaration_digest != before.declaration_digest
    assert after.lock_digest == before.lock_digest


def test_lock_byte_change_changes_dependency_state(
    tmp_path: Path,
) -> None:
    _, lock = _write_inputs(tmp_path)
    provider = DependencyStateProvider()

    before = provider.capture(project_root=tmp_path)

    lock.write_bytes(lock.read_bytes() + b"\n")

    after = provider.capture(project_root=tmp_path)

    assert after.declaration_digest == before.declaration_digest
    assert after.lock_digest != before.lock_digest


@pytest.mark.parametrize(
    "missing_name",
    ("pyproject.toml", "requirements.txt"),
)
def test_provider_rejects_missing_canonical_dependency_input(
    tmp_path: Path,
    missing_name: str,
) -> None:
    _write_inputs(tmp_path)
    (tmp_path / missing_name).unlink()

    with pytest.raises(ValueError, match="does not exist"):
        DependencyStateProvider().capture(project_root=tmp_path)
