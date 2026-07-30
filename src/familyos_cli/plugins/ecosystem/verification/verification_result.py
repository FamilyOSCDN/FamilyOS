"""Plugin verification result model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VerificationResult:
    """Represent the outcome of a plugin package verification."""

    valid: bool
    reason: str = ""

    def is_valid(
        self,
    ) -> bool:
        """Return whether verification succeeded."""

        return self.valid

    @property
    def successful(
        self,
    ) -> bool:
        """Return whether verification succeeded."""

        return self.valid

    @property
    def failed(
        self,
    ) -> bool:
        """Return whether verification failed."""

        return not self.valid
