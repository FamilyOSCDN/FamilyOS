"""Port for clean-environment Python wheel functional validation."""

from __future__ import annotations

from abc import ABC, abstractmethod

from familyos_cli.application.build.artifact_discovery import DiscoveredArtifact
from familyos_cli.application.build.package_functional_validation import (
    PythonWheelFunctionalValidationResult,
)


class PythonWheelFunctionalValidatorPort(ABC):
    """Validate one exact discovered wheel through external execution."""

    @abstractmethod
    def validate(
        self,
        candidate: DiscoveredArtifact,
    ) -> PythonWheelFunctionalValidationResult:
        """Install and smoke-test the supplied wheel candidate."""

        raise NotImplementedError
