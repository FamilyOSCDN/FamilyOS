from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import Any

import pytest

from familyos_cli.application.generation.generation_options import (
    GenerationOptions,
)


def _set_attribute(
    instance: object,
    name: str,
    value: Any,
) -> None:
    setattr(
        instance,
        name,
        value,
    )


def test_generation_options_defaults() -> None:
    options = GenerationOptions()

    assert options.overwrite is False
    assert options.encoding == "utf-8"
    assert options.create_directories is True
    assert options.dry_run is False


def test_generation_options_custom_values() -> None:
    options = GenerationOptions(
        overwrite=True,
        encoding="utf-16",
        create_directories=False,
        dry_run=True,
    )

    assert options.overwrite is True
    assert options.encoding == "utf-16"
    assert options.create_directories is False
    assert options.dry_run is True


def test_generation_options_is_immutable() -> None:
    options = GenerationOptions()

    with pytest.raises(
        FrozenInstanceError,
    ):
        _set_attribute(
            options,
            "encoding",
            "ascii",
        )
