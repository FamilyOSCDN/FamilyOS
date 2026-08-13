import pytest

from familyos_cli.plugins.builtin.documents.models import (
    DocumentVersion,
)


def test_document_version_initial_state() -> None:
    version = DocumentVersion(
        version=1,
        checksum="abc123",
    )

    assert version.version == 1
    assert version.checksum == "abc123"
    assert version.is_initial() is True


def test_document_version_non_initial_state() -> None:
    version = DocumentVersion(
        version=2,
        checksum="def456",
    )

    assert version.is_initial() is False


def test_document_version_rejects_zero() -> None:
    with pytest.raises(
        ValueError,
        match="Document version must be greater than zero",
    ):
        DocumentVersion(
            version=0,
            checksum="abc123",
        )


def test_document_version_rejects_negative_value() -> None:
    with pytest.raises(
        ValueError,
        match="Document version must be greater than zero",
    ):
        DocumentVersion(
            version=-1,
            checksum="abc123",
        )


def test_document_version_rejects_empty_checksum() -> None:
    with pytest.raises(
        ValueError,
        match="Document version checksum must not be empty",
    ):
        DocumentVersion(
            version=1,
            checksum="",
        )


def test_document_version_rejects_whitespace_checksum() -> None:
    with pytest.raises(
        ValueError,
        match="Document version checksum must not be empty",
    ):
        DocumentVersion(
            version=1,
            checksum="   ",
        )
