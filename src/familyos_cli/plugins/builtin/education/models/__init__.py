"""Education domain models."""

from familyos_cli.plugins.builtin.education.models.course import (
    Course,
)
from familyos_cli.plugins.builtin.education.models.educational_record import (
    EducationalRecord,
)
from familyos_cli.plugins.builtin.education.models.learner import (
    Learner,
)

__all__ = [
    "Course",
    "EducationalRecord",
    "Learner",
]
