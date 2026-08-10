"""Tests for DocumentProfile."""

from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.plugins.builtin.documents.profiles.document_profile import (
    DocumentProfile,
)


def test_document_profile_can_be_created() -> None:
    """Document profile stores values."""

    profile = DocumentProfile(
        id="documents.profile.family",
        name="Family Documents Profile",
        version="1.0.0",
        level="STANDARD",
        description=(
            "Document profile for family environments."
        ),
    )

    assert profile.id == "documents.profile.family"
    assert profile.name == "Family Documents Profile"
    assert profile.version == "1.0.0"
    assert profile.level == "STANDARD"
    assert profile.description == (
        "Document profile for family environments."
    )


def test_document_profile_description_is_optional() -> None:
    """Description defaults to empty."""

    profile = DocumentProfile(
        id="documents.profile.basic",
        name="Basic Documents Profile",
        version="1.0.0",
        level="BASIC",
    )

    assert profile.description == ""


def test_document_profile_is_immutable() -> None:
    """Document profiles cannot be modified."""

    profile = DocumentProfile(
        id="documents.profile.basic",
        name="Basic Documents Profile",
        version="1.0.0",
        level="BASIC",
    )

    with pytest.raises(FrozenInstanceError):
        profile.level = "CRITICAL"  # type: ignore[misc]