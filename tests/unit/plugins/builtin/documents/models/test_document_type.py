from familyos_cli.plugins.builtin.documents.models import (
    DocumentType,
)


def test_document_type_values() -> None:
    assert DocumentType.IDENTITY.value == "identity"
    assert DocumentType.FINANCE.value == "finance"
    assert DocumentType.HEALTH.value == "health"
    assert DocumentType.EDUCATION.value == "education"
    assert DocumentType.LEGAL.value == "legal"
    assert DocumentType.ARCHIVE.value == "archive"
