"""Education profile resolver."""

from __future__ import annotations

from familyos_cli.plugins.builtin.education.domain.education_level import (
    EducationLevel,
)
from familyos_cli.plugins.builtin.education.profiles.education_profile import (
    EducationProfile,
)


class EducationProfileResolver:
    """Resolve education profiles."""

    def resolve(
        self,
        profile: EducationProfile,
    ) -> EducationLevel:
        """Resolve profile level."""

        return EducationLevel(
            profile.level.lower(),
        )
