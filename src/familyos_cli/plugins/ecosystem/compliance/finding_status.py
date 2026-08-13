"""Compliance finding workflow status."""

from __future__ import annotations

from enum import StrEnum


class FindingStatus(StrEnum):
    """Represent how a compliance finding is being handled.

    Only ``OPEN`` is produced by this implementation slice.
    Acknowledgement, suppression, exception, and resolution workflows are
    deferred to a later slice (see docs/epics/EPIC-PLUGIN-002.../
    10-Findings-and-Severity-Model.md).
    """

    OPEN = "open"
