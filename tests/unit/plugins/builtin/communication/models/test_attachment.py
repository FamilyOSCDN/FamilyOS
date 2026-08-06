from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.communication.models import (
    Attachment,
)


def test_attachment_creation() -> None:
    attachment = Attachment(
        identifier="att-1",
        filename="photo.jpg",
        media_type="image/jpeg",
        size=1024,
    )

    assert attachment.filename == "photo.jpg"
    assert attachment.media_type == "image/jpeg"
    assert attachment.size == 1024


def test_attachment_rejects_negative_size() -> None:
    with pytest.raises(ValueError):
        Attachment(
            identifier="att-1",
            filename="photo.jpg",
            media_type="image/jpeg",
            size=-1,
        )


def test_attachment_is_immutable() -> None:
    attachment = Attachment(
        identifier="att-1",
        filename="photo.jpg",
        media_type="image/jpeg",
        size=1024,
    )

    with pytest.raises(FrozenInstanceError):
        attachment.filename = "new.jpg"  # type: ignore[misc]
