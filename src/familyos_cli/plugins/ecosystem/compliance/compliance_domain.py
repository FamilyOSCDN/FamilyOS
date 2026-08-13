"""Compliance rule domains covered by this implementation slice."""

from __future__ import annotations

from enum import StrEnum


class ComplianceDomain(StrEnum):
    """Categorize a compliance rule by its primary ownership domain.

    This slice covers a subset of the full domain baseline defined in
    docs/epics/EPIC-PLUGIN-002.../05-Compliance-Domains.md. Security,
    testing, quality, documentation, compatibility, lifecycle, governance,
    contributions, and configuration domains are deferred.
    """

    IDENTITY = "identity"
    METADATA = "metadata"
    STRUCTURE = "structure"
    ARCHITECTURE = "architecture"
    CAPABILITIES = "capabilities"
    DEPENDENCIES = "dependencies"
