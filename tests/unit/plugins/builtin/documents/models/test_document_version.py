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
