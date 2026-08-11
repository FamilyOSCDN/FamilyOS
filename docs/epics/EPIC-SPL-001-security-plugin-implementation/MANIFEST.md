# EPIC-SPL-001 — Security Plugin Implementation Manifest

## Canonical Model

This manifest governs the repository-control layer for the historical Security
Plugin Implementation EPIC.

## Master Document

External historical master:

`docs/epics/EPIC-SPL-001-security-plugin-implementation.md`

The master is not duplicated inside this control directory.

## Control Documents

The canonical control set is:

1. `EPIC.yaml`
2. `README.md`
3. `MANIFEST.md`
4. `CHANGELOG.md`
5. `VALIDATION.md`
6. `Revision-History.md`

Control document count:

`6`

## Historical Release

Implementation release:

- Tag: `v3.1.0-security-plugin-implementation`
- Commit: `dd713048360e77cb89fda5c05603cc14b3b886ca`

The master document existed at this release.

## Historical Reference Normalization

The current master differs from the v3.1 release only by the later architecture
reference normalization:

`ADR-0008` → `ADR-0013`

The correction was introduced by:

`e4ea9e239c9672c07808aa81432d555f9e84724c`

## Implementation Evidence

The Security Plugin repository contains implementation for:

- capabilities
- contributions
- domain
- policies
- profiles
- recipes
- rules
- templates
- validation
- runtime plugin loading

Automated tests exist for the corresponding runtime and domain behavior.

## Structural Contract

```text
External Master Documents: 1
Control Documents:         6
Numbered Documents:        0
```

The master document must remain preserved and must not be rewritten merely to
synchronize its historical metadata with current implementation status.
