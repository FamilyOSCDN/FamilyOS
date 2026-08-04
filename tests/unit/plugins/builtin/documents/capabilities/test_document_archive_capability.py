from familyos_cli.plugins.builtin.documents.capabilities.document_archive_capability import (
    DocumentArchiveCapability,
)


def test_document_archive_capability_has_expected_identifier() -> None:
    capability = DocumentArchiveCapability.create()

    assert str(
        capability.id,
    ) == "familyos.documents.archive"


def test_document_archive_capability_has_expected_metadata() -> None:
    capability = DocumentArchiveCapability.create()

    assert capability.display_name == (
        "Documents Archive"
    )

    assert (
        "digital archive"
        in capability.description
    )

    assert capability.metadata["domain"] == (
        "documents"
    )

    assert capability.metadata["version"] == (
        "1.0.0"
    )
