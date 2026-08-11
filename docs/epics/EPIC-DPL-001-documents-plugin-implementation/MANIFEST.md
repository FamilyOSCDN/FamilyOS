# EPIC-DPL-001 — Manifest

## Purpose

This manifest defines the canonical control-document inventory for the retrospective governance record of the FamilyOS Documents Plugin implementation.

## Canonical Inventory

| Document | Role |
| --- | --- |
| `EPIC-DPL-001.md` | Epic authority and implementation record |
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

`v2.6.0-documents-plugin`

Commit: `efd8ef94f5354e8757ecbd60af718dccf8aa180c`

Implementation release:

`v3.5.0-documents-plugin`

Commit: `935865417f851f15fc617a56da8d5230c0361f41`

Historical dedicated Documents Plugin EPIC at implementation release: none.

## Identifier Contract

`EPIC-DOC-001` is owned by the Documentation Framework.

`EPIC-DPL-001` is the canonical identifier for the Documents Plugin implementation governance record.

## Completeness Requirements

The manifest is complete when:

- all seven declared files exist;
- no undeclared file exists in the canonical directory;
- no required file is empty;
- YAML metadata matches the filesystem;
- historical tags remain immutable;
- identifier separation from `EPIC-DOC-001` is preserved;
- validation evidence is recorded.

## Final Principle

The manifest describes a governance record created after implementation completion; it does not alter the historical implementation baseline.
