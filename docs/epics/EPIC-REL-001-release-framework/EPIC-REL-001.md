# Changelog

All notable changes to **EPIC-REL-001 — Release Framework** are documented in this file.

The format follows the FamilyOS documentation and release conventions and is intended to preserve the historical evolution of the framework.

---

# Unreleased

## Added

* Final validation evidence pending.
* Final release commit pending.
* Official annotated release tag pending.
* Authoritative remote publication verification pending.

---

# 4.8.0 — Release Framework

## Added

* Established **EPIC-REL-001 — Release Framework** as the official FamilyOS release engineering foundation.
* Introduced a canonical release-specific documentation architecture replacing the previous generic Engineering Foundation-derived structure.
* Defined the complete FamilyOS release lifecycle:

```text
PLANNED
   ↓
PREPARED
   ↓
READY
   ↓
CANDIDATE
   ↓
VALIDATED
   ↓
APPROVED
   ↓
RELEASED
   ↓
PUBLISHED
   ↓
DISTRIBUTED
   ↓
COMPLETED
```

* Defined exceptional release states including:

```text
BLOCKED
FAILED
WITHDRAWN
SUPERSEDED
ROLLED_BACK
```

* Established release identity as a first-class engineering concept.

* Defined semantic versioning rules for:

  * major releases;
  * minor releases;
  * patch releases;
  * pre-releases;
  * release candidates;
  * component releases;
  * framework milestones.

* Established the distinction between:

```text
release version
```

and:

```text
Git release tag
```

* Defined FamilyOS framework release tag conventions such as:

```text
v<version>-<release-subject>
```

* Established formal Release Types including:

  * development;
  * preview;
  * feature;
  * maintenance;
  * security;
  * emergency;
  * framework;
  * plugin;
  * platform;
  * documentation.

* Established Release Channels including:

  * development;
  * preview;
  * candidate;
  * stable;
  * maintenance.

* Defined Release Planning requirements covering:

  * release intent;
  * scope;
  * version intent;
  * dependencies;
  * compatibility;
  * validation;
  * documentation;
  * governance;
  * publication;
  * risk;
  * recovery.

* Introduced the **Release Readiness Gate** before formal candidate creation.

* Defined readiness domains including:

  * repository;
  * build;
  * testing;
  * quality;
  * security;
  * compliance;
  * documentation;
  * dependencies;
  * compatibility;
  * artifacts;
  * versioning;
  * risk;
  * governance;
  * publication;
  * recovery.

* Introduced formal **Release Candidate** identity and lifecycle semantics.

* Defined release candidate numbering using forms such as:

```text
5.2.0-rc.1
5.2.0-rc.2
```

* Established rules for:

  * candidate stability;
  * candidate freeze;
  * candidate invalidation;
  * candidate iteration;
  * candidate rejection;
  * candidate promotion.

* Established the preferred release principle:

```text
build once
validate
promote
```

* Introduced a formal Release Artifact model.
* Distinguished:

```text
Build Artifact
```

from:

```text
Release Artifact
```

* Defined artifact inventory, identity, integrity, immutability, promotion, and retention requirements.
* Introduced release artifact checksum concepts and candidate-to-published artifact integrity verification.
* Established the canonical release provenance chain:

```text
Repository
   ↓
Source Revision
   ↓
Build
   ↓
Artifact
   ↓
Candidate
   ↓
Validation
   ↓
Official Release
```

* Defined future provenance maturity capabilities including:

  * release manifests;
  * dependency inventories;
  * SBOMs;
  * artifact signatures;
  * signed provenance;
  * attestations.

* Established formal **Release Validation** for the exact release candidate.

* Defined validation domains covering:

  * source;
  * repository;
  * build;
  * artifacts;
  * provenance;
  * version;
  * testing;
  * quality;
  * security;
  * compliance;
  * documentation;
  * compatibility;
  * installation;
  * upgrade;
  * migration;
  * recovery.

* Established explicit validation outcomes:

```text
PASS
FAIL
BLOCKED
EXCEPTION_REQUIRED
```

* Defined evidence freshness and validation invalidation rules.
* Established the distinction:

```text
VALIDATED
!=
APPROVED
```

* Introduced the FamilyOS **Release Automation** architecture.

* Defined automation requirements for:

  * stateful execution;
  * modular operations;
  * idempotency;
  * dry runs;
  * safe retry;
  * preflight checks;
  * evidence generation;
  * failure recovery.

* Defined the future Release Orchestrator concept.

* Established the principle:

> Automation executes release rules; it does not invent them.

* Defined CI/CD integration without coupling the framework to a specific provider.

* Distinguished:

  * CI validation;
  * continuous delivery;
  * publication;
  * deployment.

* Established CI/CD trust boundaries and separation between validation and privileged publication.

* Defined candidate artifact retention and build-once promotion through CI/CD.

* Established protected release credential handling and trusted runner expectations.

* Defined pipeline retry and concurrency requirements.

* Established separate responsibilities for **CHANGELOG.md** and release notes.

* Defined changelog categories:

```text
Added
Changed
Fixed
Deprecated
Removed
Security
```

* Defined release note requirements for:

  * release identity;
  * highlights;
  * compatibility;
  * migration;
  * known issues;
  * security;
  * upgrade guidance.

* Formalized repository state requirements for official Git-based releases.

* Defined release relationships among:

```text
working tree
HEAD
branch
remote branch
release commit
release tag
remote tag
```

* Established annotated Git tags as the preferred mechanism for significant FamilyOS framework milestones.

* Defined official tag immutability and collision behavior.

* Established remote tag verification as part of release publication.

* Defined Publishing and Distribution as distinct release concerns.

* Established publication target concepts including:

  * Git remotes;
  * package registries;
  * plugin registries;
  * artifact registries;
  * documentation systems.

* Defined multi-target publication and partial publication states.

* Established the principle:

> Trust the resulting target state, not only the command result.

* Defined distribution channel promotion and rollback.

* Established immutable version identity independently from mutable channel aliases.

* Defined Rollback and Recovery as first-class release architecture concerns.

* Established support for:

  * retry;
  * rollback;
  * withdrawal;
  * channel restoration;
  * forward recovery;
  * corrective releases.

* Established the principle that recovery begins from actual observed state rather than assumed command outcome.

* Introduced complete **Release Security** architecture covering:

  * identity;
  * authentication;
  * authorization;
  * least privilege;
  * credentials;
  * source integrity;
  * repository protection;
  * CI/CD security;
  * candidate integrity;
  * artifact integrity;
  * provenance;
  * dependency security;
  * publication security;
  * supply-chain security.

* Defined release credential protection and prohibited storage of release secrets in repository content.

* Defined future signing, SBOM, provenance, and attestation maturity.

* Established release security incident and withdrawal concepts.

* Introduced Release Observability as a lifecycle-wide capability.

* Defined release state, candidate, validation, publication, distribution, failure, and recovery observability requirements.

* Established future release lifecycle event concepts.

* Defined formal **Release Governance**.

* Established governance roles including:

  * Release Owner;
  * Technical Owner;
  * Validation Authority;
  * Approval Authority;
  * Release Authority;
  * Publication Authority;
  * Distribution Authority;
  * Risk Authority;
  * Exception Authority;
  * Security Authority;
  * Emergency Authority;
  * Withdrawal Authority;
  * Framework Authority.

* Established the principle:

```text
technical permission
!=
governed authority
```

* Defined explicit approval binding to candidate, scope, risk, and exceptions.

* Established risk acceptance and exception governance.

* Defined emergency release and break-glass governance concepts.

* Defined framework change governance and policy ownership.

* Introduced Release Compliance architecture.

* Defined release profile conformance and compliance findings.

* Established the relationship between compliance, exceptions, governance, and release qualification.

* Introduced Release Metrics architecture for evaluating:

  * release reliability;
  * candidate failure;
  * publication;
  * rollback;
  * recovery;
  * automation;
  * governance;
  * security;
  * evidence completeness.

* Introduced Release Risk Management covering:

  * identification;
  * likelihood;
  * impact;
  * mitigation;
  * residual risk;
  * risk acceptance;
  * release blocking.

* Established the Release Framework's own lifecycle:

```text
PROPOSED
   ↓
DRAFT
   ↓
VALIDATED
   ↓
APPROVED
   ↓
RELEASED
   ↓
ACTIVE
   ↓
MAINTAINED
   ↓
DEPRECATED
   ↓
RETIRED
```

* Defined framework change categories including:

```text
EDITORIAL
CLARIFICATION
COMPATIBLE
NORMATIVE
BREAKING
SECURITY
```

* Established the Release Framework bootstrap and self-application model.

* Defined framework migration, supersession, deprecation, retirement, and archival.

* Added a long-term roadmap toward:

  * automated readiness;
  * structured release candidates;
  * machine-readable release manifests;
  * policy-as-code;
  * automated publishing;
  * release evidence stores;
  * signing;
  * SBOM;
  * signed provenance;
  * release orchestration.

* Added consolidated internal and external reference architecture.

* Integrated references to:

  * FamilyOS Engineering Foundation;
  * Build Framework;
  * Testing Framework;
  * Quality Framework;
  * Documentation Framework;
  * Plugin Compliance Framework;
  * FamilyOS foundation architecture;
  * ADRs;
  * RFCs;
  * specifications;
  * Git;
  * semantic versioning concepts;
  * software supply-chain standards.

* Added a consolidated framework summary.

* Added a comprehensive implementation checklist distinguishing:

```text
framework definition
current implementation
future roadmap capability
```

* Defined final framework closure requirements covering:

  * canonical document completeness;
  * control document alignment;
  * validation;
  * governance;
  * versioning;
  * repository state;
  * official tag publication;
  * remote verification.

---

## Changed

* Replaced the inherited generic Engineering Foundation-style numbered structure with a dedicated Release Framework architecture.
* Removed the duplicate canonical `01` numbering model.
* Replaced generic engineering documents such as:

```text
01-Introduction.md
03-Engineering-Principles.md
04-Repository-Architecture.md
05-Development-Workflow.md
06-Coding-Standards.md
07-Project-Structure.md
08-Toolchain.md
09-Environment-Management.md
10-Dependency-Management.md
11-Configuration-Management.md
12-Build-Philosophy.md
13-Testing-Philosophy.md
14-Documentation-Philosophy.md
15-Quality-Philosophy.md
16-Technical-Governance.md
17-Engineering-Lifecycle.md
```

with release-specific canonical documents.

* Expanded the framework from a generic engineering documentation baseline into a dedicated release engineering capability.
* Formalized current FamilyOS framework publication practices into explicit normative release rules.
* Converted manual practices around Git status, commits, tags, pushes, and verification into a reusable release architecture.
* Clarified the distinction between current manual release implementation and future automated release capabilities.

---

## Removed

* Removed the duplicate canonical `01` document structure.
* Removed generic Engineering Foundation-derived numbered documents from the canonical Release Framework structure.
* Removed ambiguous release semantics based solely on:

  * successful build;
  * local tag creation;
  * successful push command;
  * latest artifact selection;
  * technical repository permissions.

---

## Security

* Added release credential protection requirements.
* Added least-privilege release authority requirements.
* Added protection requirements for privileged CI/CD jobs.
* Added source, candidate, artifact, provenance, and tag integrity requirements.
* Added publication target and channel protection requirements.
* Added software supply-chain security maturity concepts.
* Added release security incident, credential compromise, and release withdrawal architecture.

---

# Historical Baseline

Before the dedicated EPIC-REL-001 architecture was established, the directory inherited a generic engineering framework structure.

The previous structure included documents such as:

```text
01-Context.md
01-Introduction.md
02-Vision.md
03-Engineering-Principles.md
04-Repository-Architecture.md
05-Development-Workflow.md
...
23-Implementation-Checklist.md
```

This structure provided useful documentation content but did not represent a canonical Release Framework architecture.

The EPIC-REL-001 restructuring replaces that inherited model with the release-specific `00–31` canonical structure.

---

# Current Release Status

The **4.8.0 Release Framework milestone** is considered ready for final closure only after:

```text
canonical structure      PASS
control documents        ALIGNED
framework validation     PASS
release record           COMPLETE
final commit             CREATED
official tag             CREATED
branch publication       VERIFIED
tag publication          VERIFIED
working tree             CLEAN
```

Until those repository-level release actions are complete, the changelog entry represents the intended framework release state rather than proof of final publication.

---

# Target Official Tag

Subject to final repository validation, the intended framework release tag is:

```text
v4.8.0-release-framework
```

The tag must point to the exact final EPIC-REL-001 release commit.

---

# Release Integrity

The final release must preserve the relationship:

```text
HEAD
=
origin/<release-branch>
=
v4.8.0-release-framework
```

for the final release commit, together with a clean working tree.

---

# Final Statement

Version **4.8.0** establishes the first canonical FamilyOS Release Framework.

It transforms release engineering from a collection of manual repository operations into a formal architecture covering planning, readiness, candidates, provenance, validation, governance, security, automation, publication, distribution, observability, risk management, and recovery.

Future changes to this framework must themselves follow the lifecycle and governance rules established by EPIC-REL-001.
