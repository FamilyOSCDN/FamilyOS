"""Finance transaction types."""

from enum import StrEnum


class TransactionType(StrEnum):
    """Supported financial transaction types."""

    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    INVESTMENT = "investment"
