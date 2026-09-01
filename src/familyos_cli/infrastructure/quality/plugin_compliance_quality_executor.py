from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path

from familyos_cli.application.ports.quality import QualityExecutorPort
from familyos_cli.application.quality import QualityCheckResult
from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityEvidence,
    QualityEvidenceId,
    QualityEvidenceResult,
    QualityEvidenceType,
    QualityFinding,
    QualityFindingId,
    QualityRule,
    QualityStatus,
    QualityTarget,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_engine import ComplianceEngine
from familyos_cli.plugins.ecosystem.compliance.compliance_evidence import (
    ComplianceEvidence,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_finding import (
    ComplianceFinding,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_request import (
    ComplianceRequest,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_result import ComplianceResult
from familyos_cli.plugins.ecosystem.compliance.compliance_status import ComplianceStatus
from familyos_cli.plugins.models import PluginDescriptor
from familyos_cli.plugins.plugin_loader import PluginLoader

_COMPLIANCE = QualityEvidenceType("COMPLIANCE")
_STATUS = {
    ComplianceStatus.COMPLIANT: (QualityStatus.PASS, QualityEvidenceResult.PASS),
    ComplianceStatus.NON_COMPLIANT: (QualityStatus.FAIL, QualityEvidenceResult.FAIL),
    ComplianceStatus.INCOMPLETE: (QualityStatus.WARNING, QualityEvidenceResult.WARNING),
    ComplianceStatus.ERROR: (QualityStatus.ERROR, QualityEvidenceResult.ERROR),
}


class PluginComplianceQualityExecutor(QualityExecutorPort):
    def __init__(
        self,
        *,
        engine: ComplianceEngine,
        plugin_loader: PluginLoader,
        plugins_root: Path,
        finding_id_factory: Callable[[], QualityFindingId],
        evidence_id_factory: Callable[[], QualityEvidenceId],
        monotonic_clock: Callable[[], float] | None = None,
    ) -> None:
        self._engine = engine
        self._plugin_loader = plugin_loader
        self._plugins_root = plugins_root
        self._finding_id_factory = finding_id_factory
        self._evidence_id_factory = evidence_id_factory
        self._clock = monotonic_clock or time.monotonic

    def execute(
        self, *, check_id: QualityCheckId, rule: QualityRule, target: QualityTarget
    ) -> QualityCheckResult:
        started = self._clock()
        if target.target_type != "plugin":
            return self._error(check_id, started, "target_type must be 'plugin'")
        if target.path is None:
            return self._error(check_id, started, "target.path is required")
        try:
            descriptor = self._descriptor(target)
            result = self._engine.evaluate(
                ComplianceRequest(plugin_descriptor=descriptor, profile_id="official")
            )
            return self._normalize(check_id, rule, target, result, started)
        except Exception as exc:  # noqa: BLE001
            return self._error(
                check_id,
                started,
                f"Plugin Compliance assessment could not complete: {exc}",
            )

    def _descriptor(self, target: QualityTarget) -> PluginDescriptor:
        for descriptor in self._plugin_loader.discover(self._plugins_root):
            if descriptor.id != target.identifier:
                continue
            if descriptor.path != Path(target.path or ""):
                raise ValueError("target path does not match canonical descriptor")
            if target.version is not None and descriptor.version != target.version:
                raise ValueError("target version does not match canonical descriptor")
            return descriptor
        raise ValueError(f"plugin {target.identifier!r} was not found")

    def _normalize(
        self,
        check_id: QualityCheckId,
        rule: QualityRule,
        target: QualityTarget,
        result: ComplianceResult,
        started: float,
    ) -> QualityCheckResult:
        if result.plugin_id != target.identifier:
            raise ValueError("result plugin id does not match target")
        if target.version is not None and result.plugin_version != target.version:
            raise ValueError("result plugin version does not match target")
        if result.profile_id != "official":
            raise ValueError("result profile is not official")
        status, evidence_result = _STATUS[result.status]
        pairs = tuple(
            (
                x,
                self._evidence(
                    x,
                    rule,
                    target,
                    evidence_result,
                    evaluation_id=result.evaluation_id,
                    profile_id=result.profile_id,
                ),
            )
            for x in result.evidence
        )
        evidence = tuple(x for _, x in pairs)
        id_map = {source.id: normalized.id.value for source, normalized in pairs}
        findings = tuple(
            self._finding(x, rule, target, status, id_map) for x in result.findings
        )
        diagnostics = tuple(self._finding_provenance(x) for x in result.findings)
        return QualityCheckResult(
            check_id=check_id,
            status=status,
            findings=findings,
            evidence=evidence,
            duration_seconds=self._duration(started),
            diagnostics=diagnostics,
        )

    def _evidence(
        self,
        source: ComplianceEvidence,
        rule: QualityRule,
        target: QualityTarget,
        result: QualityEvidenceResult,
        *,
        evaluation_id: str,
        profile_id: str,
    ) -> QualityEvidence:
        return QualityEvidence(
            id=self._evidence_id_factory(),
            type=_COMPLIANCE,
            source="quality.plugin_compliance",
            target=target,
            result=result,
            created_at=source.collected_at,
            revision=target.revision,
            rule_id=rule.id,
            requirement_id=rule.requirement_id,
            tool=source.producer,
            tool_version=source.producer_version,
            metadata=(
                ("compliance_evaluation_id", evaluation_id),
                ("compliance_profile_id", profile_id),
                ("source_evidence_id", source.id),
                ("source_evidence_type", source.type.value),
                ("source", source.source),
                ("producer", source.producer),
                ("producer_version", source.producer_version),
                ("plugin_id", source.plugin_id),
                ("plugin_version", source.plugin_version),
                ("scope", source.scope),
                ("trust_level", source.trust_level.value),
                ("collected_at", source.collected_at.isoformat()),
            ),
        )

    def _finding(
        self,
        source: ComplianceFinding,
        rule: QualityRule,
        target: QualityTarget,
        status: QualityStatus,
        id_map: dict[str, str],
    ) -> QualityFinding:
        try:
            refs = tuple(id_map[x] for x in source.evidence_refs)
        except KeyError as exc:
            raise ValueError(
                f"finding references unknown evidence {exc.args[0]!r}"
            ) from exc
        provenance = (
            f"[plugin_rule={source.rule_id}; plugin_domain={source.domain.value}; "
            f"plugin_severity={source.severity.value}; plugin_category={source.category.value}; "
            f"plugin_status={source.status.value}]"
        )
        return QualityFinding(
            id=self._finding_id_factory(),
            rule_id=rule.id,
            domain=rule.domain,
            severity=rule.severity,
            status=status,
            message=f"{source.message} {provenance}",
            target=target,
            location=source.location or None,
            evidence_ids=refs,
        )

    @staticmethod
    def _finding_provenance(source: ComplianceFinding) -> str:
        evidence_refs = ",".join(source.evidence_refs)
        return (
            "plugin_compliance_finding:"
            f"id={source.id};"
            f"evaluation_id={source.evaluation_id};"
            f"rule_id={source.rule_id};"
            f"domain={source.domain.value};"
            f"severity={source.severity.value};"
            f"category={source.category.value};"
            f"status={source.status.value};"
            f"title={source.title};"
            f"remediation={source.remediation};"
            f"evidence_refs={evidence_refs}"
        )

    def _error(
        self, check_id: QualityCheckId, started: float, diagnostic: str
    ) -> QualityCheckResult:
        return QualityCheckResult(
            check_id=check_id,
            status=QualityStatus.ERROR,
            duration_seconds=self._duration(started),
            diagnostics=(diagnostic,),
        )

    def _duration(self, started: float) -> float:
        return max(0.0, self._clock() - started)
