"""Learner domain validator."""

from __future__ import annotations

from familyos_cli.plugins.builtin.education.models.learner import (
    Learner,
)


class LearnerValidator:
    """Validate learner business rules."""

    def validate(
        self,
        learner: Learner,
    ) -> bool:
        """Validate learner."""

        return bool(
            learner.name.strip()
            and learner.education_level.strip()
        )
