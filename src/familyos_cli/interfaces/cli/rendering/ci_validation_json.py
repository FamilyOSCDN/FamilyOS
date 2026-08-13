"""Deterministic JSON renderer for canonical CI validation."""

from __future__ import annotations

import json
from typing import Any

from familyos_cli.application.validation import CiValidationResult, GateResult


class CiValidationJsonRenderer:
    """Project semantic validation results into stable machine-readable JSON."""

    def render(self, result: CiValidationResult) -> str:
        """Render the canonical result as UTF-8-compatible JSON text."""

        payload: dict[str, Any] = {
            "schema_version": result.schema_version,
            "profile": result.profile,
            "status": result.status.value,
            "gates": [self._gate_payload(gate) for gate in result.gates],
        }
        return f"{json.dumps(payload, indent=2, ensure_ascii=True)}\n"

    @staticmethod
    def _gate_payload(gate: GateResult) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": gate.gate_id,
            "status": gate.status.value,
            "exit_code": gate.exit_code,
            "diagnostic": gate.diagnostic,
        }
        if gate.profile_id is not None:
            payload["profile_id"] = gate.profile_id
            payload["plugins"] = [
                {
                    "plugin_id": plugin.plugin_id,
                    "plugin_version": plugin.plugin_version,
                    "status": plugin.status,
                    "diagnostic": plugin.diagnostic,
                    "rule_outcomes": [
                        {
                            "rule_id": rule.rule_id,
                            "outcome": rule.outcome,
                            "severity": rule.severity,
                        }
                        for rule in plugin.rule_outcomes
                    ],
                }
                for plugin in gate.plugins
            ]
        return payload
