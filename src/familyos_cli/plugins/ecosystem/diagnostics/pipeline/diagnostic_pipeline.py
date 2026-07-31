"""Plugin resolution diagnostic pipeline."""

from __future__ import annotations

from collections.abc import Iterable

from familyos_cli.plugins.ecosystem.diagnostics.adapters import (
    ResolutionConflictDiagnosticAdapter,
)
from familyos_cli.plugins.ecosystem.diagnostics.diagnostic_builder import (
    DiagnosticBuilder,
)
from familyos_cli.plugins.ecosystem.diagnostics.diagnostic_report import (
    DiagnosticReport,
)
from familyos_cli.plugins.ecosystem.diagnostics.ports import (
    ResolutionDiagnosticAdapter,
)
from familyos_cli.plugins.ecosystem.resolution import ResolutionPlan


class DiagnosticPipeline:
    """Build diagnostics from a resolution plan."""

    def __init__(
        self,
        adapters: Iterable[ResolutionDiagnosticAdapter]
        | None = None,
    ) -> None:
        """Initialize the pipeline."""

        self._adapters = tuple(
            adapters
            if adapters is not None
            else (
                ResolutionConflictDiagnosticAdapter(),
            )
        )

    def build(
        self,
        plan: ResolutionPlan,
    ) -> DiagnosticReport:
        """Build a diagnostic report."""

        builder = DiagnosticBuilder()

        for adapter in self._adapters:
            diagnostics = adapter.adapt(
                plan,
            )

            builder.add_many(
                diagnostics,
            )

        return builder.build()
