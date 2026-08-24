"""Tests for canonical Testing Framework execution identity."""

from __future__ import annotations

from uuid import UUID

import pytest

from familyos_cli.application.testing.test_execution_id import (
    TestExecutionId as CanonicalExecutionId,
)


def test_execution_id_wraps_uuid() -> None:
    value = UUID("01234567-89ab-cdef-0123-456789abcdef")

    execution_id = CanonicalExecutionId(value)

    assert execution_id.value == value


def test_execution_id_is_immutable() -> None:
    execution_id = CanonicalExecutionId.generate()

    with pytest.raises(AttributeError):
        execution_id.value = UUID(  # type: ignore[misc]
            "fedcba98-7654-3210-fedc-ba9876543210"
        )


def test_execution_id_generate_returns_uuid_backed_identity() -> None:
    execution_id = CanonicalExecutionId.generate()

    assert isinstance(execution_id.value, UUID)


def test_execution_id_generation_is_unique() -> None:
    first = CanonicalExecutionId.generate()
    second = CanonicalExecutionId.generate()

    assert first != second


def test_execution_id_string_is_canonical_uuid() -> None:
    value = UUID("01234567-89ab-cdef-0123-456789abcdef")

    execution_id = CanonicalExecutionId(value)

    assert str(execution_id) == str(value)
