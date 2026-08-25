"""Load canonical CI validation evidence from JSON."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any
from uuid import UUID

from familyos_cli.application.testing import (
    TestExecutionId,
    TestExecutionResult,
    TestExecutionStatus,
    TestExecutionSummary,
    TestingEvidence,
)
from familyos_cli.application.validation import (
    CI_VALIDATION_SCHEMA_VERSION,
    CiValidationResult,
    GateResult,
    ValidationStatus,
)


class CiValidationJsonLoader:
    """Reconstruct canonical CI validation authority from JSON evidence."""

    def load(self, document: str) -> CiValidationResult:
        """Load and validate one canonical CI validation JSON document."""

        try:
            payload = json.loads(document)
        except json.JSONDecodeError as error:
            raise ValueError(
                "CI validation evidence is not valid JSON"
            ) from error

        if not isinstance(payload, dict):
            raise ValueError(
                "CI validation evidence root must be an object"
            )

        schema_version = self._required_string(
            payload,
            "schema_version",
            diagnostic="CI validation schema version is required",
        )

        if schema_version != CI_VALIDATION_SCHEMA_VERSION:
            raise ValueError(
                "unsupported CI validation schema version: "
                f"{schema_version}"
            )

        profile = self._required_string(
            payload,
            "profile",
            diagnostic="CI validation profile is required",
        )

        raw_gates = payload.get("gates")

        if not isinstance(raw_gates, list):
            raise ValueError(
                "CI validation gates are required"
            )

        gates = tuple(
            self._load_gate(gate)
            for gate in raw_gates
        )

        return CiValidationResult(
            gates=gates,
            schema_version=schema_version,
            profile=profile,
        )

    def _load_gate(
        self,
        payload: Any,
    ) -> GateResult:
        if not isinstance(payload, dict):
            raise ValueError(
                "CI validation gate must be an object"
            )

        gate_id = self._required_string(
            payload,
            "id",
            diagnostic="CI validation gate id is required",
        )

        status = self._validation_status(
            self._required_string(
                payload,
                "status",
                diagnostic="CI validation gate status is required",
            )
        )

        exit_code = payload.get("exit_code")
        if exit_code is not None and (
            not isinstance(exit_code, int)
            or isinstance(exit_code, bool)
        ):
            raise ValueError(
                "CI validation gate exit_code must be an integer or null"
            )

        diagnostic = payload.get("diagnostic")
        if diagnostic is not None and not isinstance(
            diagnostic,
            str,
        ):
            raise ValueError(
                "CI validation gate diagnostic must be a string or null"
            )

        testing_evidence_payload = payload.get(
            "testing_evidence"
        )

        testing_evidence = (
            None
            if testing_evidence_payload is None
            else self._load_testing_evidence(
                testing_evidence_payload
            )
        )

        return GateResult(
            gate_id=gate_id,
            status=status,
            exit_code=exit_code,
            diagnostic=diagnostic,
            testing_evidence=testing_evidence,
        )

    def _load_testing_evidence(
        self,
        payload: Any,
    ) -> TestingEvidence:
        if not isinstance(payload, dict):
            raise ValueError(
                "testing evidence must be an object"
            )

        execution_id = self._required_string(
            payload,
            "execution_id",
            diagnostic="testing evidence execution_id is required",
        )

        source_revision = self._required_string(
            payload,
            "source_revision",
            diagnostic="testing evidence source_revision is required",
        )

        if "source_dirty" not in payload:
            raise ValueError(
                "testing evidence source_dirty is required"
            )

        source_dirty = payload["source_dirty"]

        if not isinstance(source_dirty, bool):
            raise ValueError(
                "testing evidence source_dirty must be boolean"
            )

        captured_at_value = self._required_string(
            payload,
            "captured_at",
            diagnostic="testing evidence captured_at is required",
        )

        try:
            captured_at = datetime.fromisoformat(
                captured_at_value
            )
        except ValueError as error:
            raise ValueError(
                "testing evidence captured_at is invalid"
            ) from error

        if captured_at.tzinfo is None:
            raise ValueError(
                "testing evidence captured_at must be timezone-aware"
            )

        native_exit_code = payload.get(
            "native_exit_code"
        )

        if native_exit_code is not None and (
            not isinstance(native_exit_code, int)
            or isinstance(native_exit_code, bool)
        ):
            raise ValueError(
                "testing evidence native_exit_code "
                "must be an integer or null"
            )

        result_payload = payload.get("result")

        if not isinstance(result_payload, dict):
            raise ValueError(
                "testing evidence result is required"
            )

        try:
            canonical_execution_id = TestExecutionId(
                UUID(execution_id)
            )
        except ValueError as error:
            raise ValueError(
                "testing evidence execution_id is invalid"
            ) from error

        return TestingEvidence(
            execution_id=canonical_execution_id,
            source_revision=source_revision,
            source_dirty=source_dirty,
            result=self._load_test_result(
                result_payload
            ),
            captured_at=captured_at,
            native_exit_code=native_exit_code,
        )

    def _load_test_result(
        self,
        payload: dict[str, Any],
    ) -> TestExecutionResult:
        status = self._test_execution_status(
            self._required_string(
                payload,
                "status",
                diagnostic=(
                    "testing evidence result status is required"
                ),
            )
        )

        summary_payload = payload.get("summary")

        if not isinstance(summary_payload, dict):
            raise ValueError(
                "testing evidence result summary is required"
            )

        diagnostic = payload.get("diagnostic")

        if diagnostic is not None and not isinstance(
            diagnostic,
            str,
        ):
            raise ValueError(
                "testing evidence result diagnostic "
                "must be a string or null"
            )

        return TestExecutionResult(
            status=status,
            summary=self._load_test_summary(
                summary_payload
            ),
            diagnostic=diagnostic,
        )

    def _load_test_summary(
        self,
        payload: dict[str, Any],
    ) -> TestExecutionSummary:
        return TestExecutionSummary(
            discovered=self._required_integer(
                payload,
                "discovered",
            ),
            executed=self._required_integer(
                payload,
                "executed",
            ),
            passed=self._required_integer(
                payload,
                "passed",
            ),
            failed=self._required_integer(
                payload,
                "failed",
            ),
            skipped=self._required_integer(
                payload,
                "skipped",
            ),
            errors=self._required_integer(
                payload,
                "errors",
            ),
            duration_seconds=self._required_number(
                payload,
                "duration_seconds",
            ),
        )

    @staticmethod
    def _required_string(
        payload: dict[str, Any],
        key: str,
        *,
        diagnostic: str,
    ) -> str:
        value = payload.get(key)

        if not isinstance(value, str) or not value:
            raise ValueError(diagnostic)

        return value

    @staticmethod
    def _required_integer(
        payload: dict[str, Any],
        key: str,
    ) -> int:
        value = payload.get(key)

        if (
            not isinstance(value, int)
            or isinstance(value, bool)
        ):
            raise ValueError(
                f"testing evidence summary {key} "
                "must be an integer"
            )

        return value

    @staticmethod
    def _required_number(
        payload: dict[str, Any],
        key: str,
    ) -> float:
        value = payload.get(key)

        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
        ):
            raise ValueError(
                f"testing evidence summary {key} "
                "must be numeric"
            )

        return float(value)

    @staticmethod
    def _validation_status(
        value: str,
    ) -> ValidationStatus:
        try:
            return ValidationStatus(value)
        except ValueError as error:
            raise ValueError(
                f"unsupported CI validation status: {value}"
            ) from error

    @staticmethod
    def _test_execution_status(
        value: str,
    ) -> TestExecutionStatus:
        try:
            return TestExecutionStatus(value)
        except ValueError as error:
            raise ValueError(
                f"unsupported testing evidence status: {value}"
            ) from error
