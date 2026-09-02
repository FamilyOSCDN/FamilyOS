from enum import StrEnum


class QualityAssessmentState(StrEnum):
    PASS = "PASS"
    PASS_WITH_WARNINGS = "PASS_WITH_WARNINGS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"
