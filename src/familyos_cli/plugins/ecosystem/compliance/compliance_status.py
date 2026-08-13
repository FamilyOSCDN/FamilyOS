"""Overall plugin compliance status."""

from __future__ import annotations

from enum import StrEnum


class ComplianceStatus(StrEnum):
    """Represent the overall outcome of a compliance evaluation.

    Precedence, highest to lowest: ``ERROR`` > ``NON_COMPLIANT`` >
    ``INCOMPLETE`` > ``COMPLIANT``.
    """

    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    INCOMPLETE = "incomplete"
    ERROR = "error"
