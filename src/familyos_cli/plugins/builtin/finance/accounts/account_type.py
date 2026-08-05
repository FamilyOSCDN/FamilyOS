"""Finance account types."""

from enum import StrEnum


class AccountType(StrEnum):
    """Supported financial account types."""

    BANK = "bank"
    SAVINGS = "savings"
    INVESTMENT = "investment"
    CASH = "cash"
