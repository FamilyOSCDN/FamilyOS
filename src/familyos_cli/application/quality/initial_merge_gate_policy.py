"""Explicit initial merge-readiness policy, restricted to observation."""

from familyos_cli.application.quality.default_quality_profile_registry import (
    REPOSITORY_PROFILE,
)
from familyos_cli.domain.quality.quality_assessment_state import QualityAssessmentState
from familyos_cli.domain.quality.quality_gate_id import QualityGateId
from familyos_cli.domain.quality.quality_gate_policy import QualityGatePolicy
from familyos_cli.domain.quality.quality_status import QualityStatus

INITIAL_MERGE_OBSERVATION_POLICY = QualityGatePolicy(
    gate_id=QualityGateId("QLT-GATE-MERGE-001"),
    version="1.0.0",
    authority="docs/epics/EPIC-QLT-001-quality-framework/25-Implementation-Checklist.md: Phase 15 Initial Merge Observation Contract",
    profile=REPOSITORY_PROFILE,
    accepted_check_statuses=(QualityStatus.PASS,),
    accepted_assessment_states=(
        QualityAssessmentState.PASS,
        QualityAssessmentState.PASS_WITH_WARNINGS,
    ),
)
