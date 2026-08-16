"""Validated Python package identity."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PackageIdentity:
    """Authoritative package name and version validated for an artifact."""

    name: str
    version: str
