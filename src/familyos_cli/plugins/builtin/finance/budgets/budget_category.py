"""Finance budget categories."""

from enum import StrEnum


class BudgetCategory(StrEnum):
    """Supported budget categories."""

    HOUSING = "housing"
    FOOD = "food"
    TRANSPORT = "transport"
    EDUCATION = "education"
    HEALTH = "health"
    OTHER = "other"
