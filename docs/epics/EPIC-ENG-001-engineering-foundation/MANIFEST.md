# EPIC-ENG-001 — Engineering Foundation Manifest

## 1. Purpose

This manifest defines the complete documentation inventory for
EPIC-ENG-001 — Engineering Foundation.

It identifies every authoritative file delivered by the EPIC, its purpose,
and its role within the FamilyOS engineering documentation system.

The manifest is normative for the structure and completeness of this EPIC.

## 2. EPIC Metadata

| Field | Value |
|---|---|
| EPIC ID | EPIC-ENG-001 |
| Title | Engineering Foundation |
| Version | 1.0.0 |
| Status | In Progress |
| Language | English |
| Owner | FamilyOS Team |
| Category | Engineering |
| Repository | FamilyOS |

## 3. Document Inventory

### 3.1 Control Documents

| File | Purpose |
|---|---|
| `EPIC.yaml` | Machine-readable EPIC metadata, scope, dependencies, deliverables, quality gates, and acceptance criteria. |
| `EPIC-ENG-001.md` | Primary EPIC definition, rationale, scope, goals, exclusions, outcomes, and completion criteria. |
| `README.md` | Navigation entry point for the Engineering Foundation documentation set. |
| `MANIFEST.md` | Authoritative inventory of all files delivered by the EPIC. |
| `CHANGELOG.md` | Chronological record of material changes to the Engineering Foundation. |
| `VALIDATION.md` | Evidence that structural, documentary, and repository quality requirements have been satisfied. |
| `Revision-History.md` | Version and revision history for the Engineering Foundation documentation set. |

### 3.2 Foundation Chapters

| File | Purpose |
|---|---|
| `01-Introduction.md` | Introduces the Engineering Foundation, its context, intended audience, and role within FamilyOS. |
| `02-Vision.md` | Defines the long-term engineering vision and desired characteristics of the FamilyOS platform. |
| `03-Engineering-Principles.md` | Establishes the principles that guide architecture, implementation, validation, and maintenance. |
| `04-Repository-Architecture.md` | Defines repository boundaries, architectural layers, dependency direction, and ownership rules. |
| `05-Development-Workflow.md` | Describes the standard lifecycle from issue selection through implementation, review, validation, and merge. |
| `06-Coding-Standards.md` | Defines repository-wide coding, typing, formatting, naming, and maintainability standards. |
| `07-Project-Structure.md` | Specifies the expected organization of source code, tests, documentation, plugins, scripts, and configuration. |
| `08-Toolchain.md` | Defines the approved engineering tools and their responsibilities within the development lifecycle. |
| `09-Environment-Management.md` | Establishes rules for local environments, Python versions, virtual environments, reproducibility, and isolation. |
| `10-Dependency-Management.md` | Defines dependency selection, declaration, pinning, upgrades, auditing, and removal practices. |
| `11-Configuration-Management.md` | Defines configuration sources, precedence, validation, secrets handling, and environment-specific behavior. |
| `12-Build-Philosophy.md` | Establishes build principles, reproducibility expectations, artifact integrity, and build isolation. |
| `13-Testing-Philosophy.md` | Defines the role, scope, layers, determinism, and quality expectations of automated testing. |
| `14-Documentation-Philosophy.md` | Establishes documentation principles, ownership, structure, traceability, and maintenance requirements. |
| `15-Quality-Philosophy.md` | Defines the FamilyOS quality model, prevention strategy, quality gates, and continuous improvement expectations. |
| `16-Technical-Governance.md` | Defines technical decision authority, review responsibilities, exceptions, ADR usage, and policy enforcement. |
| `17-Engineering-Lifecycle.md` | Describes the complete lifecycle of engineering work from proposal through maintenance and retirement. |
| `18-Roadmap.md` | Defines the staged implementation roadmap for the Engineering Foundation and its dependent frameworks. |
| `19-References.md` | Lists normative and informative references used by the Engineering Foundation. |

## 4. File Count

The Engineering Foundation contains:

- 7 control documents
- 19 numbered foundation chapters
- 26 files in total

All files are located in:

```text
docs/epics/EPIC-ENG-001-engineering-foundation/
## 5. Normative Hierarchy

Where documents overlap, the following precedence applies:

1. Accepted Architecture Decision Records (ADRs)
2. Approved Specifications and RFCs
3. `EPIC.yaml`
4. `EPIC-ENG-001.md`
5. Numbered Engineering Foundation chapters
6. `README.md`
7. Informative examples and supporting notes

A lower-precedence document must not contradict a higher-precedence source.

---

## 6. Completeness Requirements

The EPIC is structurally complete only when:

- all 26 files exist;
- every declared deliverable is present;
- no required document is empty;
- all documentation is written in English;
- internal links and references resolve;
- document responsibilities do not conflict;
- the validation report records the final quality evidence;
- repository-wide MyPy, Ruff, and Pytest checks pass.

---

## 7. Ownership

The FamilyOS Team owns this documentation set.

Changes that materially alter engineering policy, architecture, governance,
quality gates, or lifecycle expectations must be reviewed and recorded in:

- `CHANGELOG.md`;
- `Revision-History.md`;
- an ADR when an architectural decision is involved.

---

## 8. Status

This manifest describes version **1.0.0** of the Engineering Foundation
documentation structure.

The EPIC remains **In Progress** until:

- all required documents are complete;
- all acceptance criteria declared in `EPIC.yaml` have been satisfied;
- all repository quality gates have passed successfully;
- the validation report has been completed and approved.
