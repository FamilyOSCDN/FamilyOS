# EPIC Index

## Overview

This document provides the canonical index of FamilyOS EPICs.

EPICs represent major engineering, architectural, documentation, platform,
governance, and implementation initiatives.

The canonical repository state of an EPIC is defined by its EPIC directory and,
when present, its `EPIC.yaml` control document.

This index provides a human-readable consolidated view of that state.

---

## Purpose

The purpose of this index is to:

- provide a central EPIC reference;
- expose the current canonical EPIC inventory;
- distinguish frameworks from implementation initiatives;
- track completed engineering work;
- preserve roadmap visibility;
- prevent legacy EPIC identifiers or titles from being treated as canonical.

---

# EPIC Model

An EPIC represents a major body of work with:

- defined objectives;
- documented scope;
- architectural or implementation responsibilities;
- validation criteria;
- lifecycle state;
- repository evidence.

Where an `EPIC.yaml` exists, it is authoritative for the current lifecycle
state of that EPIC.

---

# EPIC Naming Convention

Current FamilyOS EPIC identifiers use domain-specific prefixes.

Examples include:

```text
EPIC-ENG-001
EPIC-TST-001
EPIC-QLT-001
EPIC-PLUGIN-001
EPIC-SPL-001
```

The identifier MUST remain unique within the FamilyOS repository.

The canonical path of an EPIC is its directory under:

```text
docs/epics/
```

---

# Engineering Framework EPICs

| Identifier | Title | Status |
|---|---|---|
| EPIC-ENG-001 | Engineering Foundation | Completed |
| EPIC-TST-001 | Testing Framework | Completed |
| EPIC-QLT-001 | Quality Framework | Completed |
| EPIC-BLD-001 | Build Framework | Completed |
| EPIC-REL-001 | Release Framework | Completed |
| EPIC-OBS-001 | Observability Framework | Completed |
| EPIC-SEC-001 | Security Framework | Completed |
| EPIC-OPS-001 | Operations Framework | Completed |

These EPICs establish the broad cross-cutting engineering foundation of
FamilyOS.

EPIC-OPS-001 completes the currently planned broad engineering framework
sequence.

---

# Documentation Framework

| Identifier | Title | Status |
|---|---|---|
| EPIC-DOC-001 | Documentation Framework | Baseline / Closed |

`EPIC-DOC-001` represents the FamilyOS Documentation Framework.

It MUST NOT be interpreted as the Documents Plugin implementation EPIC.

---

# Plugin Governance and Ecosystem EPICs

| Identifier | Title | Status |
|---|---|---|
| EPIC-PLUGIN-001 | Official Plugin Implementation | Completed |
| EPIC-PLUGIN-002 | Plugin Compliance Framework | Baseline / Closed |

These EPICs define and validate the common implementation and compliance model
for official FamilyOS plugins.

---

# Official Plugin Implementation EPICs

| Identifier | Title | Status |
|---|---|---|
| EPIC-SPL-001 | Security Plugin Implementation | Completed |
| EPIC-HLT-001 | Health Plugin Implementation | Completed |
| EPIC-FIN-001 | Finance Plugin Implementation | Completed |
| EPIC-EDU-001 | Education Plugin Implementation | Completed |
| EPIC-DPL-001 | Documents Plugin Implementation | Completed |
| EPIC-COM-001 | Communication Plugin | Completed |

These identifiers represent the canonical implementation EPICs for the
official plugin set currently present in the repository.

The distinction between framework and plugin identifiers is intentional.

For example:

```text
EPIC-SEC-001
```

represents the Security Framework, while:

```text
EPIC-SPL-001
```

represents the Security Plugin Implementation.

Likewise:

```text
EPIC-DOC-001
```

represents the Documentation Framework, while:

```text
EPIC-DPL-001
```

represents the Documents Plugin Implementation.

---

# Future Initiatives

The following identifiers appeared in the historical roadmap but do not
currently have canonical EPIC directories in the repository.

| Identifier | Title | Status |
|---|---|---|
| EPIC-AI-001 | AI Intelligence Framework | Planned |
| EPIC-DATA-001 | Data Management Framework | Planned |
| EPIC-INT-001 | Integration Framework | Planned |

These entries represent roadmap intent only.

They MUST NOT be interpreted as implemented or validated EPICs until canonical
EPIC repository structures are created.

---

# Legacy Index Entries

Earlier revisions of this index referenced:

```text
EPIC-PLT-001
EPIC-PLG-001
EPIC-GEN-001
```

as completed platform EPICs.

No corresponding canonical EPIC directories are present in the current
`docs/epics/` inventory.

These identifiers are therefore not listed as active canonical EPICs by this
index.

Historical references MAY remain elsewhere where required for repository
history, but they MUST NOT be used as evidence of current canonical EPIC
state without corresponding repository authority.

---

# EPIC Lifecycle

FamilyOS EPICs may use lifecycle states appropriate to their governance model.

Common states include:

| Stage | Description |
|---|---|
| Planned | Identified future initiative |
| Draft | Initial definition exists |
| In Progress | Active implementation or documentation work |
| Baseline | Authoritative baseline established |
| Completed | Defined objectives achieved |
| Maintained | Completed capability under controlled evolution |

EPIC closure is represented by the canonical control structure of each EPIC.

In the current canonical EPIC inventory, all physical EPIC directories expose
an `EPIC.yaml` whose closure contract records:

```text
epic_closed: true
```

A lifecycle state such as `completed` or `baseline` describes the EPIC state,
while `epic_closed: true` records that its current governed work cycle is
closed.

---

# Canonical State Authority

The following precedence applies when determining current EPIC state:

```text
EPIC.yaml
    │
    ▼
EPIC control documents
    │
    ▼
Canonical numbered documents
    │
    ▼
EPIC-Index.md
    │
    ▼
Historical roadmap references
```

`EPIC-Index.md` MUST summarize canonical state.

It MUST NOT override the lifecycle state recorded by an EPIC's authoritative
control documents.

---

# Current Repository Summary

The current canonical EPIC inventory contains:

- eight completed engineering framework EPICs;
- one closed documentation framework EPIC;
- two closed plugin governance and compliance EPICs;
- six completed official plugin implementation EPICs.

The current physical EPIC inventory contains 17 canonical EPIC directories.

Each of those directories contains an `EPIC.yaml`, and the audited closure
state of each canonical EPIC records:

```text
epic_closed: true
```

Future roadmap initiatives remain separate from completed repository work.

---

# Governance

EPIC changes SHOULD be supported by the appropriate FamilyOS governance
mechanisms, including:

- RFCs;
- ADRs;
- specifications;
- engineering documentation;
- validation evidence;
- release evidence where applicable.

New EPIC identifiers MUST NOT reuse an identifier already assigned to a
canonical or historically significant FamilyOS initiative.

The index SHOULD be reviewed whenever an EPIC is created, renamed, completed,
closed, superseded, or removed from the active roadmap.

---

# Revision History

| Version | Date | Description |
|---|---|---|
| 1.0.0 | 2026-08-04 | Initial publication |
| 1.1.0 | 2026-08-12 | Reconciled index with canonical repository EPIC state, corrected framework/plugin identities, and removed obsolete lifecycle classifications |
