"""Finance liability types."""

from enum import StrEnum


class LiabilityType(StrEnum):
    """Supported financial liability types."""

    MORTGAGE = "mortgage"
    LOAN = "loan"
    CREDIT = "credit"
