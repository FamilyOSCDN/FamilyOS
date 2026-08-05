"""Education context model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.builtin.education.domain.education_level import (
    EducationLevel,
)


@dataclass(
    frozen=True,
    slots=True,
)
class EducationContext:
    """Describe an education evaluation context."""

    domain_name: str

    subject: str

    required_level: EducationLevel
