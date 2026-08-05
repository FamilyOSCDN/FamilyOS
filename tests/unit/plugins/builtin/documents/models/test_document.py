from familyos_cli.plugins.builtin.documents.models import (
    Document,
    DocumentType,
    DocumentVersion,
)


def test_document_creation() -> None:
    document = Document(
        identifier="document.family.passport",
        title="Family Passport",
        document_type=DocumentType.IDENTITY,
        owner="family-member",
        version=DocumentVersion(
            version=1,
            checksum="abc123",
        ),
    )

    assert document.identifier == "document.family.passport"
    assert document.title == "Family Passport"
    assert document.document_type == DocumentType.IDENTITY
    assert document.owner == "family-member"
    assert document.is_private() is True
