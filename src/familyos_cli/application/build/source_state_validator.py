"""Validate observed source state for strict build usage."""

from __future__ import annotations

from familyos_cli.application.build.source_state import SourceState
from familyos_cli.application.build.source_state_validation import (
    SourceStateValidationResult,
)


class SourceStateValidator:
    """Validate whether source revision and workspace state are trustworthy."""

    def validate(
        self,
        state: SourceState,
    ) -> SourceStateValidationResult:
        """Validate one observed source state without mutating it."""

        revision_identified = bool(state.revision)

        revision_diagnostic = (
            None
            if revision_identified
            else "source revision is unavailable"
        )

        if state.dirty is False:
            working_tree_clean = True
            working_tree_diagnostic = None
        elif state.dirty is True:
            working_tree_clean = False
            working_tree_diagnostic = "source working tree is dirty"
        else:
            working_tree_clean = False
            working_tree_diagnostic = (
                "source working tree state is unavailable"
            )

        return SourceStateValidationResult(
            revision_identified=revision_identified,
            working_tree_clean=working_tree_clean,
            revision_diagnostic=revision_diagnostic,
            working_tree_diagnostic=working_tree_diagnostic,
        )
