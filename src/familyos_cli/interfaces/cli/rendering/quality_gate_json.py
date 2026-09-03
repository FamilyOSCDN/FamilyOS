"""Versioned transport for a non-blocking Quality gate observation."""

import json

from familyos_cli.domain.quality.quality_gate import QualityGate


def render_gate_json(gate: QualityGate) -> str:
    target = gate.target
    payload = {
        "schema_version": "1.0.0",
        "gate": {
            "id": str(gate.id),
            "target": {
                "target_type": target.target_type,
                "identifier": target.identifier,
                "revision": target.revision,
                "version": target.version,
                "path": target.path,
                "metadata": [list(pair) for pair in target.metadata],
            },
            "revision": gate.revision,
            "policy": gate.policy,
            "assessment_id": str(gate.assessment_id)
            if gate.assessment_id is not None
            else None,
            "decision": gate.decision.value,
            "mode": gate.mode,
            "prevents_progression": gate.prevents_progression,
            "blocking_conditions": [
                {
                    "code": condition.code,
                    "message": condition.message,
                    "check_id": str(condition.check_id)
                    if condition.check_id is not None
                    else None,
                    "finding_ids": [str(value) for value in condition.finding_ids],
                    "rule_ids": [str(value) for value in condition.rule_ids],
                    "evidence_ids": [str(value) for value in condition.evidence_ids],
                }
                for condition in gate.blocking_conditions
            ],
            "evaluated_at": gate.evaluated_at.isoformat(),
        },
    }
    rendered = json.dumps(payload, ensure_ascii=False, allow_nan=False, indent=2) + "\n"
    rendered.encode("utf-8")
    return rendered
