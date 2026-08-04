from familyos_cli.plugins.builtin.documents.capabilities.document_capability import (
    DocumentCapability,
)


def test_document_capability_has_expected_identifier() -> None:
    capability = DocumentCapability.create()

    assert str(
        capability.id,
    ) == "familyos.documents.document"


def test_document_capability_has_expected_metadata() -> None:
    capability = DocumentCapability.create()

    assert capability.display_name == (
        "Documents"
    )

    assert (
        "document management"
        in capability.description
    )

    assert capability.metadata["domain"] == (
        "documents"
    )

    assert capability.metadata["version"] == (
        "1.0.0"
    )
