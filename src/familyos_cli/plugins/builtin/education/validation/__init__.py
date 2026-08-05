"""Education validation."""

from familyos_cli.plugins.builtin.education.validation.course_validator import (
    CourseValidator,
)
from familyos_cli.plugins.builtin.education.validation.educational_record_validator import (
    EducationalRecordValidator,
)
from familyos_cli.plugins.builtin.education.validation.learner_validator import (
    LearnerValidator,
)

__all__ = [
    "CourseValidator",
    "EducationalRecordValidator",
    "LearnerValidator",
]
