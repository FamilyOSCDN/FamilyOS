# EPIC-HLT-001 — Manifest

## Purpose

This manifest defines the canonical control-document inventory for the retrospective governance record of the FamilyOS Health Plugin implementation.

## Canonical Inventory

| Document | Role |
| --- | --- |
| `EPIC-HLT-001.md` | Epic authority and implementation record |
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

`v2.3.0-health-plugin`
Commit: `0af94aada99946e1fd715c2964fae23b853757ca`

Implementation release:

`v3.2.0-health-plugin-implementation`
Commit: `661f4176f6b14cbad4f888007ecc2afcc9648c75`

Historical EPIC at implementation release: none.

## Implementation Evidence

The implementation baseline contains the Health Plugin source tree and its tests. The retrospective control documents are governance additions and are not represented as historical implementation artifacts.

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
