from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError
from yaml import YAMLError

from familyos_cli.configuration.models import (
    FamilyOSConfiguration,
)


class ConfigurationError(Exception):
    """Raised when configuration loading fails."""


class ConfigurationLoader:
    """Loads FamilyOS configuration files."""

    def load(
        self,
        path: Path,
    ) -> FamilyOSConfiguration:
        """Load configuration from YAML file."""

        if not path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {path}",
            )

        try:
            content = path.read_text(
                encoding="utf-8",
            )

            data = yaml.safe_load(
                content,
            )

        except OSError as exc:
            raise ConfigurationError(
                f"Unable to read configuration file: {path}",
            ) from exc

        except YAMLError as exc:
            raise ConfigurationError(
                "Invalid YAML configuration.",
            ) from exc

        if data is None:
            raise ConfigurationError(
                "Configuration file is empty.",
            )

        try:
            return FamilyOSConfiguration.model_validate(
                data,
            )

        except ValidationError as exc:
            raise ConfigurationError(
                "Invalid FamilyOS configuration.",
            ) from exc
