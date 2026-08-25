"""Downstream consumption boundary for canonical Release handoff."""

from __future__ import annotations

from familyos_cli.application.build.release_handoff import (
    ReleaseHandoff,
)


class ReleaseHandoffConsumer:
    """Consume an established Release handoff without substitution."""

    def consume(
        self,
        handoff: ReleaseHandoff,
    ) -> ReleaseHandoff:
        """Return the exact established handoff authority."""

        return handoff
