import pytest

from familyos_cli.plugins.builtin.documents.models import (
    Document,
    DocumentType,
    DocumentVersion,
)


def create_version() -> DocumentVersion:
    return DocumentVersion(
        version=1,
        checksum="abc123",
    )


def test_document_creation() -> None:
    document = Document(
        identifier="document.family.passport",
        title="Family Passport",
        document_type=DocumentType.IDENTITY,
        owner="family-member",
        version=create_version(),
    )

    assert document.identifier == "document.family.passport"
    assert document.title == "Family Passport"
    assert document.document_type == DocumentType.IDENTITY
    assert document.owner == "family-member"
    assert document.is_private() is True


def test_document_rejects_empty_identifier() -> None:
    with pytest.raises(
        ValueError,
        match="Document identifier must not be empty",
    ):
        Document(
            identifier="",
            title="Family Passport",
            document_type=DocumentType.IDENTITY,
            owner="family-member",
            version=create_version(),
        )


def test_document_rejects_whitespace_identifier() -> None:
    with pytest.raises(
        ValueError,
        match="Document identifier must not be empty",
    ):
        Document(
            identifier="   ",
            title="Family Passport",
            document_type=DocumentType.IDENTITY,
            owner="family-member",
            version=create_version(),
        )


def test_document_rejects_empty_title() -> None:
    with pytest.raises(
        ValueError,
        match="Document title must not be empty",
    ):
        Document(
            identifier="document.family.passport",
            title="",
            document_type=DocumentType.IDENTITY,
            owner="family-member",
            version=create_version(),
        )


def test_document_rejects_whitespace_title() -> None:
    with pytest.raises(
        ValueError,
        match="Document title must not be empty",
    ):
        Document(
            identifier="document.family.passport",
            title="   ",
            document_type=DocumentType.IDENTITY,
            owner="family-member",
            version=create_version(),
        )


def test_document_rejects_empty_owner() -> None:
    with pytest.raises(
        ValueError,
        match="Document owner must not be empty",
    ):
        Document(
            identifier="document.family.passport",
            title="Family Passport",
            document_type=DocumentType.IDENTITY,
            owner="",
            version=create_version(),
        )


def test_document_rejects_whitespace_owner() -> None:
    with pytest.raises(
        ValueError,
        match="Document owner must not be empty",
    ):
        Document(
            identifier="document.family.passport",
            title="Family Passport",
            document_type=DocumentType.IDENTITY,
            owner="   ",
            version=create_version(),
        )
