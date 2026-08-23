"""Validate observed canonical build-toolchain compatibility."""

from __future__ import annotations

from collections.abc import Mapping

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version

from familyos_cli.application.build.toolchain_state import ToolchainState
from familyos_cli.application.build.toolchain_validation import (
    ToolchainValidationFinding,
    ToolchainValidationResult,
    ToolchainValidationStatus,
)


class ToolchainValidator:
    """Validate observed runtime and critical tool versions against policy."""

    def validate(
        self,
        *,
        runtime_version: str,
        toolchain_state: ToolchainState,
        runtime_requirement: str,
        distribution_requirements: Mapping[str, str],
    ) -> ToolchainValidationResult:
        """Validate one observed toolchain against explicit requirements."""

        findings: list[ToolchainValidationFinding] = []

        runtime_finding = self._validate_version(
            component="python",
            observed_version=runtime_version,
            requirement=runtime_requirement,
        )
        if runtime_finding is not None:
            findings.append(runtime_finding)

        observed_versions = {
            component.distribution: component.version
            for component in toolchain_state.critical_versions
        }

        for distribution, requirement in distribution_requirements.items():
            observed_version = observed_versions.get(distribution)

            if observed_version is None:
                findings.append(
                    ToolchainValidationFinding(
                        component=distribution,
                        diagnostic=(
                            f"required toolchain distribution "
                            f"{distribution!r} is unavailable"
                        ),
                    )
                )
                continue

            finding = self._validate_version(
                component=distribution,
                observed_version=observed_version,
                requirement=requirement,
            )
            if finding is not None:
                findings.append(finding)

        if findings:
            return ToolchainValidationResult(
                status=ToolchainValidationStatus.FAILED,
                findings=tuple(findings),
            )

        return ToolchainValidationResult(
            status=ToolchainValidationStatus.SUCCEEDED,
        )

    @staticmethod
    def _validate_version(
        *,
        component: str,
        observed_version: str,
        requirement: str,
    ) -> ToolchainValidationFinding | None:
        try:
            version = Version(observed_version)
            specifier = SpecifierSet(requirement)
        except InvalidVersion:
            return ToolchainValidationFinding(
                component=component,
                diagnostic=(
                    f"{component} version {observed_version!r} is invalid"
                ),
            )
        except InvalidSpecifier:
            return ToolchainValidationFinding(
                component=component,
                diagnostic=(
                    f"{component} requirement {requirement!r} is invalid"
                ),
            )

        if specifier.contains(
            version,
            prereleases=True,
        ):
            return None

        return ToolchainValidationFinding(
            component=component,
            diagnostic=(
                f"{component} {version} does not satisfy {specifier}"
            ),
        )
