"""Tests for the builtin Plugin Compliance validation gate."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import cast

import pytest

from familyos_cli.application.use_cases.check_plugin_compliance import (
    CheckPluginComplianceUseCase,
)
from familyos_cli.application.validation import ValidationStatus
from familyos_cli.application.validation.builtin_plugin_compliance_gate import (
    BuiltinPluginComplianceGate,
)
from familyos_cli.plugins.ecosystem.compliance.compliance_status import (
    ComplianceStatus,
)
from familyos_cli.plugins.plugin_loader import PluginLoader


@dataclass(frozen=True)
class _Descriptor:
    id: str
    version: str = "1.0.0"


@dataclass(frozen=True)
class _Result:
    plugin_id: str
    plugin_version: str
    status: ComplianceStatus
    rule_evaluations: tuple[object, ...] = ()


@dataclass(frozen=True)
class _Report:
    result: _Result


class _Loader:
    def __init__(self, descriptors: tuple[_Descriptor, ...]) -> None:
        self.descriptors = descriptors

    def discover(self, root: Path) -> list[_Descriptor]:
        del root
        return list(self.descriptors)


class _FailingLoader:
    def discover(self, root: Path) -> list[_Descriptor]:
        del root
        raise OSError("discovery unavailable")


class _UseCase:
    def __init__(self, statuses: dict[str, ComplianceStatus]) -> None:
        self.statuses = statuses
        self.calls: list[tuple[str, str]] = []
        self.error_plugin: str | None = None

    def execute(self, *, plugin_id: str, profile_id: str = "official") -> _Report:
        self.calls.append((plugin_id, profile_id))
        if plugin_id == self.error_plugin:
            raise RuntimeError("evaluation unavailable")
        return _Report(
            _Result(plugin_id, "1.0.0", self.statuses[plugin_id]),
        )


def _gate(loader: _Loader, use_case: _UseCase) -> BuiltinPluginComplianceGate:
    return BuiltinPluginComplianceGate(
        use_case=cast(CheckPluginComplianceUseCase, use_case),
        plugin_loader=cast(PluginLoader, loader),
        plugins_root=Path("builtins"),
    )


def test_discovers_sorts_and_uses_explicit_official_profile() -> None:
    loader = _Loader((_Descriptor("familyos.zeta"), _Descriptor("familyos.alpha")))
    use_case = _UseCase(
        {
            "familyos.alpha": ComplianceStatus.COMPLIANT,
            "familyos.zeta": ComplianceStatus.COMPLIANT,
        },
    )

    result = _gate(loader, use_case).execute()

    assert result.status is ValidationStatus.PASSED
    assert result.profile_id == "official"
    assert use_case.calls == [
        ("familyos.alpha", "official"),
        ("familyos.zeta", "official"),
    ]
    assert [plugin.plugin_id for plugin in result.plugins] == [
        "familyos.alpha",
        "familyos.zeta",
    ]


@pytest.mark.parametrize(
    "compliance_status",
    (ComplianceStatus.NON_COMPLIANT, ComplianceStatus.INCOMPLETE),
)
def test_nonpassing_compliance_status_blocks(
    compliance_status: ComplianceStatus,
) -> None:
    result = _gate(
        _Loader((_Descriptor("familyos.sample"),)),
        _UseCase({"familyos.sample": compliance_status}),
    ).execute()

    assert result.status is ValidationStatus.FAILED


def test_compliance_error_status_is_execution_error() -> None:
    result = _gate(
        _Loader((_Descriptor("familyos.sample"),)),
        _UseCase({"familyos.sample": ComplianceStatus.ERROR}),
    ).execute()

    assert result.status is ValidationStatus.ERROR


def test_evaluation_exception_is_error_and_remaining_plugins_run() -> None:
    loader = _Loader((_Descriptor("familyos.alpha"), _Descriptor("familyos.zeta")))
    use_case = _UseCase(
        {
            "familyos.alpha": ComplianceStatus.COMPLIANT,
            "familyos.zeta": ComplianceStatus.COMPLIANT,
        },
    )
    use_case.error_plugin = "familyos.alpha"

    result = _gate(loader, use_case).execute()

    assert result.status is ValidationStatus.ERROR
    assert [call[0] for call in use_case.calls] == [
        "familyos.alpha",
        "familyos.zeta",
    ]
    assert result.plugins[0].status == "error"


def test_empty_discovery_never_passes() -> None:
    result = _gate(_Loader(()), _UseCase({})).execute()

    assert result.status is ValidationStatus.ERROR


def test_discovery_exception_never_passes() -> None:
    result = _gate(
        cast(_Loader, _FailingLoader()),
        _UseCase({}),
    ).execute()

    assert result.status is ValidationStatus.ERROR
    assert result.diagnostic == "Builtin plugin discovery failed: discovery unavailable"
