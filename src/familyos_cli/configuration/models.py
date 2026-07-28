from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class FamilyOSProjectConfig(BaseModel):
    """FamilyOS project configuration."""

    name: str

    version: str = "1.0"

    description: str = ""

    author: str = ""

    root_path: Path = Field(
        default_factory=Path.cwd,
    )


class FamilyOSConfiguration(BaseModel):
    """Root FamilyOS configuration."""

    project: FamilyOSProjectConfig

    plugins: list[str] = Field(
        default_factory=list,
    )
