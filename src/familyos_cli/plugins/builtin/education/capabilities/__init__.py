"""Education plugin capabilities."""

from familyos_cli.plugins.builtin.education.capabilities.education_course_capability import (
    EducationCourseCapability,
)
from familyos_cli.plugins.builtin.education.capabilities.education_learner_capability import (
    EducationLearnerCapability,
)
from familyos_cli.plugins.builtin.education.capabilities.education_record_capability import (
    EducationRecordCapability,
)

__all__ = [
    "EducationCourseCapability",
    "EducationLearnerCapability",
    "EducationRecordCapability",
]
