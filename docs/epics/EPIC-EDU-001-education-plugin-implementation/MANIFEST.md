# EPIC-EDU-001 — Manifest

## Purpose

This manifest defines the canonical control-document inventory for the retrospective governance record of the FamilyOS Education Plugin implementation.

## Canonical Inventory

| Document | Role |
| --- | --- |
| `EPIC-EDU-001.md` | Epic authority and implementation record |
| `EPIC.yaml` | Machine-readable metadata contract |
| `README.md` | Human-readable entry point |
| `MANIFEST.md` | Canonical inventory |
| `CHANGELOG.md` | Governance-document change record |
| `VALIDATION.md` | Validation evidence and closure gates |
| `Revision-History.md` | Revision chronology |

## Inventory Contract

```text
0 Numbered Documents
+
7 Control Documents
=
7 Canonical Files
```

## Historical Baselines

RFC release:

`v2.5.0-education-plugin`

Commit: `4179990637cd8d71451a6f9ce5995f84379bc9de`

Implementation release:

`v3.4.0-education-plugin-implementation`

Commit: `3584d9391d214d5003fc5a906c6705e62df54f51`

Historical EPIC at implementation release: none.

## Implementation Evidence

The implementation baseline contains the Education Plugin source tree and its tests. The retrospective control documents are governance additions and are not represented as historical implementation artifacts.

## Completeness Requirements

The manifest is complete when:

- all seven declared files exist;
- no undeclared file exists in the canonical directory;
- no required file is empty;
- YAML metadata matches the filesystem;
- historical tags remain immutable;
- validation evidence is recorded.

## Final Principle

The manifest describes the governance record created after implementation completion; it does not alter the historical implementation baseline.
