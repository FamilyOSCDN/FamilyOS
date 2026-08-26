"""Archive metadata observations for reproducibility analysis."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from familyos_cli.application.build.artifact_type import ArtifactClass


class ArchiveMetadataField(StrEnum):
    """Canonical archive metadata fields relevant to reproducibility."""

    TIMESTAMP = "timestamp"
    MODE = "mode"
    OWNER = "owner"
    GROUP = "group"
    SIZE = "size"
    TYPE = "type"
    LINK = "link"
    COMPRESSION = "compression"
    FLAGS = "flags"


@dataclass(frozen=True, slots=True)
class ArtifactArchiveMetadataObservation:
    """Canonical metadata variability observed for one artifact."""

    artifact_type: ArtifactClass
    differing_fields: tuple[ArchiveMetadataField, ...]

    def __post_init__(self) -> None:
        """Require deterministic unique metadata-field ordering."""

        if len(self.differing_fields) != len(set(self.differing_fields)):
            raise ValueError(
                "archive metadata differing fields must be unique"
            )

        if self.differing_fields != tuple(
            sorted(self.differing_fields, key=lambda field: field.value)
        ):
            raise ValueError(
                "archive metadata differing fields must be sorted"
            )

    @property
    def metadata_equal(self) -> bool:
        """Return whether no archive metadata differences were observed."""

        return not self.differing_fields
