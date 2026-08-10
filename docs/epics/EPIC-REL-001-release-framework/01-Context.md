# Release Framework

# 01 Context

## Overview

The FamilyOS engineering platform has progressively established a set of foundational capabilities covering architecture, implementation, testing, quality, documentation, plugins, compliance, and build engineering.

These capabilities provide the mechanisms required to design, implement, validate, and produce reliable software artifacts.

However, producing a valid artifact is not equivalent to releasing that artifact.

As the FamilyOS ecosystem grows, the transition between a successful build and an official platform release becomes a distinct engineering problem requiring explicit architecture, governance, automation, traceability, and recovery mechanisms.

EPIC-REL-001 — Release Framework addresses this problem.

The framework establishes the engineering context required to transform validated FamilyOS artifacts into official, identifiable, traceable, governed, publishable, observable, and recoverable releases.

---

# Engineering Context

FamilyOS is evolving from a software project into a structured engineering platform.

The ecosystem includes increasingly independent and releasable assets such as:

* core platform components;
* command-line tooling;
* official plugins;
* documentation frameworks;
* specifications;
* architecture decisions;
* configuration assets;
* generated artifacts;
* metadata;
* future SDKs and integration components.

Each of these assets may evolve at different rates while remaining part of the same governed ecosystem.

As a result, release management can no longer rely exclusively on ad hoc Git operations or manually chosen version identifiers.

The platform requires a formal release engineering model.

---

# Current Engineering Chain

FamilyOS already establishes several stages before release.

The conceptual engineering chain is:

```text
Architecture
    ↓
Implementation
    ↓
Testing
    ↓
Quality
    ↓
Compliance
    ↓
Build
    ↓
Validated Artifacts
```

These stages answer important questions.

Architecture determines what should exist.

Implementation produces the required software behavior.

Testing verifies that behavior.

Quality evaluates broader engineering expectations.

Compliance evaluates conformance with applicable rules.

Build engineering produces controlled artifacts from a known source state.

At this point, however, several critical questions remain unresolved:

```text
Which artifacts are actually being released?

Which repository state is authoritative?

Which version should be assigned?

Is the candidate ready for publication?

Who or what may approve the release?

Which validation evidence must exist?

How are changelogs and release notes produced?

Which Git tag represents the release?

How are artifacts published?

How is publication verified?

What happens if the release fails?

How can a historical release be reconstructed?
```

These questions define the release engineering domain.

---

# Build and Release Are Different Responsibilities

One of the central architectural decisions behind EPIC-REL-001 is the explicit separation between build engineering and release engineering.

The Build Framework controls the transformation:

```text
Source State
    ↓
Build Process
    ↓
Build Artifacts
```

The Release Framework controls the transformation:

```text
Validated Build Artifacts
    ↓
Release Qualification
    ↓
Official Release
```

The distinction is important because a build may succeed while a release must still be rejected.

For example:

* mandatory tests may not have completed;
* quality gates may have failed;
* documentation may be incomplete;
* release notes may be missing;
* a security finding may remain unresolved;
* repository state may be incorrect;
* artifacts may not correspond to the intended commit;
* release metadata may be inconsistent;
* the selected version may be invalid;
* a previous release may already use the intended tag;
* a required approval may not exist.

Therefore:

> Build success is necessary for many releases, but build success alone is not sufficient for release approval.

---

# Existing Release Practices

FamilyOS already performs several release-related activities.

Examples include:

* committing completed framework work;
* verifying repository cleanliness;
* verifying branch state;
* synchronizing with the authoritative remote;
* assigning release versions;
* creating annotated Git tags;
* pushing tags to the remote repository;
* maintaining changelog information;
* validating framework completion before tagging;
* using versioned milestones to represent platform evolution.

These practices provide an important operational foundation.

However, they currently represent conventions and workflow knowledge more than a complete formal release architecture.

The Release Framework must convert those practices into explicit, reusable engineering rules.

---

# Problem Statement

Without a formal Release Framework, release operations risk becoming inconsistent as the platform expands.

Potential problems include:

* version numbers selected without uniform rules;
* different release processes for different components;
* tags created from incorrect repository states;
* artifacts published without sufficient provenance;
* release candidates modified after validation;
* missing release evidence;
* inconsistent changelog structures;
* incomplete release notes;
* unclear approval responsibility;
* manual release procedures that drift over time;
* accidental publication of incomplete artifacts;
* inability to determine exactly what was released;
* inability to reconstruct historical releases;
* weak rollback or recovery procedures;
* release credentials handled inconsistently;
* incompatible release expectations between plugins and the core platform.

These risks increase as the number of contributors, release targets, automation systems, and platform components grows.

---

# Why Release Engineering Must Be Formalized Early

Release engineering becomes more difficult to introduce after many incompatible release patterns already exist.

Establishing the framework now provides several advantages.

It creates consistent semantics before the number of FamilyOS release targets increases substantially.

It also ensures that future automation is built around explicit release architecture rather than embedding undocumented assumptions into CI/CD scripts.

This is particularly important because release automation can make incorrect processes execute faster and more consistently.

Automation is therefore only safe when the underlying release model is already well defined.

---

# Platform Growth Context

FamilyOS is designed as an extensible ecosystem rather than a single monolithic executable.

Future platform maturity may introduce:

* independently versioned plugins;
* SDK releases;
* APIs;
* libraries;
* packaged CLI releases;
* installation bundles;
* documentation releases;
* specification versions;
* generated schemas;
* deployment bundles;
* container images;
* integration packages;
* compatibility matrices.

The Release Framework must provide concepts that remain valid across these different release targets.

It should not assume that all releases are identical.

At the same time, it must preserve a common governance foundation.

---

# Release Complexity

Release complexity emerges from several interacting concerns.

## Source State

The release must originate from a known source state.

This normally includes:

* repository;
* branch or equivalent source lineage;
* commit identity;
* relevant configuration;
* dependency state;
* build inputs.

Without source identity, release reconstruction becomes unreliable.

---

## Artifact State

The exact artifacts being released must be known.

Different artifacts produced from different source or configuration states must not accidentally share the same release identity.

---

## Validation State

The framework must determine which validation evidence applies to the candidate.

Evidence may include:

* tests;
* static analysis;
* quality gates;
* compliance checks;
* security checks;
* artifact verification;
* installation verification;
* documentation validation.

---

## Version State

The intended version must be consistent with:

* previous releases;
* compatibility impact;
* release type;
* branch strategy;
* pre-release state;
* repository tags.

---

## Publication State

The framework must know whether a candidate is:

* unpublished;
* approved;
* published;
* partially published;
* withdrawn;
* superseded;
* failed.

Without explicit state semantics, release recovery becomes difficult.

---

# Repository State as Release Evidence

The Git repository is a central element of FamilyOS release traceability.

For many FamilyOS releases, a valid release requires alignment between:

```text
working tree
branch
HEAD
remote branch
version
tag
release metadata
```

A release created while these elements disagree can become ambiguous.

For example, a tag created against a local commit that has not been published to the authoritative repository may appear locally valid while failing to represent a complete shared release state.

Similarly, a release performed from a dirty working tree can create uncertainty about whether the released artifact corresponds exactly to committed source.

The Release Framework therefore treats repository state verification as a first-class release concern.

---

# Git Tags as Release Anchors

FamilyOS already uses annotated Git tags to identify significant completed engineering milestones.

Examples of the release pattern include:

```text
commit
    ↓
verify repository state
    ↓
create annotated tag
    ↓
push branch
    ↓
push tag
    ↓
verify resulting state
```

The Release Framework must formalize the semantics behind this workflow.

An official tag should represent a deliberate release anchor, not simply a convenient label.

A release tag must therefore be associated with:

* a specific commit;
* a specific version identity;
* an intentional release decision;
* appropriate validation;
* repository synchronization;
* historical stability.

---

# Version Proliferation Risk

As FamilyOS grows, multiple subsystems may introduce versions.

Without governance, this can create version ambiguity.

Potential version domains include:

```text
platform version
CLI version
plugin version
framework version
specification version
artifact version
schema version
API version
release candidate version
```

These identifiers may serve different purposes.

The Release Framework must define which version types are release identifiers, which are compatibility identifiers, and how they relate to one another.

It must also prevent unnecessary version proliferation where a shared version is sufficient.

---

# Release Candidate Problem

A release candidate must represent a stable object of validation.

If the candidate changes after tests or release validation have completed, the earlier evidence may no longer prove the correctness of the candidate being published.

The framework must therefore establish an identity relationship between:

```text
candidate
source state
artifacts
validation evidence
release version
```

This relationship is essential for trustworthy promotion.

---

# Evidence Fragmentation Problem

FamilyOS already produces evidence across several engineering systems.

Examples include:

* test results;
* Ruff results;
* MyPy results;
* quality validation;
* framework validation;
* compliance findings;
* build verification;
* documentation checks;
* Git state.

Without release-level aggregation, engineers may know that these checks occurred individually but still lack a clear answer to:

> Is this exact release candidate ready to become an official release?

The Release Framework introduces release readiness as the aggregation point for this evidence.

---

# Manual Release Risk

Manual release operations are not inherently invalid.

Some operations may intentionally remain manual because they require human authority or judgment.

The risk arises when manual processes are:

* undocumented;
* inconsistent;
* order-dependent;
* difficult to reproduce;
* difficult to audit;
* dependent on individual memory.

The framework must therefore distinguish:

```text
manual but governed
```

from:

```text
manual and undocumented
```

The first may be acceptable.

The second should be progressively eliminated.

---

# Automation Risk

Release automation also creates risks.

Poorly designed automation may:

* publish from the wrong branch;
* reuse an existing version;
* create an incorrect tag;
* publish incomplete artifacts;
* expose credentials;
* bypass required validation;
* produce partially completed releases;
* hide failed intermediate states.

The framework therefore requires automation to implement release architecture rather than define it implicitly.

---

# Partial Release Failure

Release operations frequently interact with multiple systems.

A future release workflow may involve:

```text
Git repository
artifact storage
package registry
documentation publication
release metadata
distribution service
deployment system
```

A workflow may succeed in one system and fail in another.

This creates partial release states.

For example:

```text
tag created
artifact published
release notes creation failed
```

or:

```text
tag created
publication failed
```

or:

```text
artifact published
distribution activation failed
```

The Release Framework must define how such states are detected, represented, and recovered.

---

# Immutability Requirement

Published release identity must remain trustworthy.

If consumers receive different artifacts under the same version identifier, release identity becomes unreliable.

The framework therefore adopts the principle that published release artifacts should be immutable.

If a correction is required, the preferred model is:

```text
incorrect release
        ↓
withdraw / supersede if necessary
        ↓
produce corrected release
        ↓
assign new identity
```

rather than silently replacing existing content.

---

# Security Context

Release infrastructure is a security-sensitive part of the software supply chain.

A compromised release system may distribute malicious or unintended artifacts even when source code and build infrastructure remain correct.

Security risks include:

* unauthorized tag creation;
* unauthorized publication;
* compromised release credentials;
* artifact replacement;
* provenance manipulation;
* malicious dependency substitution;
* compromised CI/CD workflows;
* insecure release storage;
* insufficient branch protection;
* insufficient access control.

Release security must therefore be integrated into architecture and governance.

---

# Provenance Context

Consumers and maintainers may need to determine where a release originated.

At minimum, provenance concepts should allow a relationship such as:

```text
Release
   │
   ├── version
   ├── source commit
   ├── build identity
   ├── artifact identity
   ├── validation evidence
   └── publication metadata
```

More advanced provenance mechanisms may later include:

* cryptographic signatures;
* attestations;
* software bill of materials;
* reproducible-build verification;
* supply-chain metadata.

EPIC-REL-001 establishes the architecture without requiring premature implementation of every advanced mechanism.

---

# Documentation Context

Release documentation has two different audiences.

Engineering documentation explains how releases are created and governed.

Release communication explains what changed in a particular release.

These responsibilities should not be conflated.

The Release Framework must therefore integrate with the Documentation Framework while separately defining:

* changelog requirements;
* release note requirements;
* compatibility information;
* migration information;
* known limitation reporting.

---

# Plugin Release Context

Official FamilyOS plugins introduce additional release complexity.

A plugin release may need to establish:

* plugin version;
* platform compatibility;
* capability compatibility;
* manifest compatibility;
* compliance status;
* plugin-specific validation;
* independent release notes;
* publication state.

The framework must support such releases without creating entirely separate release systems for every plugin.

Common release semantics should remain reusable across the ecosystem.

---

# Emergency Release Context

Not all releases can follow normal planning timelines.

Security vulnerabilities, critical regressions, or severe operational defects may require accelerated releases.

An emergency path may reduce certain procedural delays.

It must not eliminate essential controls.

The Release Framework therefore needs explicit emergency release governance.

A faster release path must remain:

* identifiable;
* authorized;
* validated appropriately;
* traceable;
* documented;
* recoverable.

---

# Rollback Context

The ability to release software creates a corresponding need to recover from defective releases.

However, rollback is not always technically safe.

Changes may include:

* persistent data migration;
* schema changes;
* irreversible external actions;
* compatibility transitions;
* protocol changes;
* configuration changes.

The framework must therefore support both:

```text
rollback
```

and:

```text
forward recovery
```

depending on system characteristics.

---

# Observability Context

Release workflows must be understandable while they execute and after they complete.

Relevant observations may include:

* release start;
* candidate identity;
* validation state;
* approval state;
* version assignment;
* tag creation;
* publication state;
* distribution state;
* completion;
* failure;
* recovery.

Observability provides evidence for engineering diagnosis and governance.

It also allows automation to determine whether a release is truly complete.

---

# Governance Context

As long as releases are performed by a small number of maintainers, release authority may appear obvious.

That assumption does not scale.

The framework must define responsibilities such as:

* release owner;
* approver;
* automation authority;
* repository authority;
* publishing authority;
* emergency authority;
* exception authority.

The exact implementation may evolve over time, but the responsibility model must remain explicit.

---

# Compliance Context

Release engineering sits at the boundary between development activity and distributed platform state.

For this reason, release processes must respect the policies and standards established across FamilyOS.

Applicable requirements may originate from:

* Engineering Foundation;
* Testing Framework;
* Quality Framework;
* Documentation Framework;
* Build Framework;
* Plugin Compliance Framework;
* security architecture;
* ADRs;
* RFCs;
* specifications;
* future release policies.

EPIC-REL-001 must provide a mechanism for these requirements to become release gates where applicable.

---

# Release Evidence Model

Release decisions should produce evidence that survives individual terminal sessions or CI/CD executions.

A conceptual release evidence set may contain:

```text
Release Evidence
├── release identity
├── version
├── source revision
├── build identity
├── artifact inventory
├── validation results
├── quality status
├── compliance status
├── security status
├── documentation status
├── approval state
├── tag
├── publication state
└── timestamps
```

The exact storage and automation mechanisms may evolve independently.

The architectural requirement is that sufficient evidence exists to establish release trust and historical traceability.

---

# Historical Reconstruction

One of the long-term requirements of the framework is the ability to answer historical questions.

For a given FamilyOS release, maintainers should eventually be able to determine:

* what source revision produced it;
* which artifacts belonged to it;
* which version was assigned;
* which tag identified it;
* what changed from the previous release;
* what validation occurred;
* which known issues existed;
* when it was published;
* whether it was superseded or withdrawn.

Historical reconstruction is essential for maintenance, debugging, compliance, incident investigation, and long-term platform sustainability.

---

# Release Maturity Model

The Release Framework must support progressive maturity.

FamilyOS does not need to implement the most advanced release infrastructure immediately.

A possible progression is:

```text
Level 1
Documented manual release process

Level 2
Standardized release validation

Level 3
Automated release preparation

Level 4
Automated evidence collection

Level 5
Controlled automated publication

Level 6
Strong provenance and signing

Level 7
Policy-driven release orchestration
```

The framework defines the target architecture while allowing implementation to evolve incrementally.

---

# Constraints

The Release Framework must operate within several constraints.

## C1 — Architecture Before Automation

The release model must be defined before substantial release automation is introduced.

---

## C2 — Compatibility With Existing Git Workflows

The framework must preserve the useful release conventions already established within FamilyOS while making them explicit and governable.

---

## C3 — No Build Duplication

Release engineering must consume Build Framework outputs rather than reimplement build responsibilities.

---

## C4 — Evidence Reuse

Testing, quality, compliance, security, and documentation evidence should be reused rather than unnecessarily recomputed by independent release systems.

---

## C5 — Incremental Adoption

The framework must support gradual implementation.

Not every advanced release capability must exist immediately.

---

## C6 — Automation Independence

Normative release semantics must not depend on a single CI/CD vendor, hosting platform, package registry, or automation tool.

---

## C7 — Ecosystem Extensibility

The framework must support future FamilyOS components without requiring fundamental redesign.

---

# Architectural Drivers

The primary drivers for EPIC-REL-001 are:

```text
Traceability
Consistency
Reproducibility
Safety
Governance
Automation
Recoverability
Security
Observability
Scalability
```

Each design decision in the Release Framework should strengthen one or more of these properties.

---

# Key Questions the Framework Must Resolve

EPIC-REL-001 must provide clear answers to the following questions.

## Release Identity

What constitutes an official FamilyOS release?

How is a release uniquely identified?

---

## Versioning

How are release versions selected?

What do major, minor, patch, and pre-release identifiers mean?

---

## Readiness

What evidence is required before release approval?

---

## Candidates

How is a release candidate created and kept stable during qualification?

---

## Artifacts

How are release artifacts identified and connected to build outputs?

---

## Provenance

How can a release be traced back to its source and build context?

---

## Validation

What checks must occur against the final candidate?

---

## Tagging

When is a Git tag created?

What does an official tag guarantee?

---

## Publishing

When does a validated candidate become officially published?

---

## Distribution

How does a published release become available to consumers?

---

## Recovery

What happens if publication fails or the release is defective?

---

## Governance

Who may approve, publish, withdraw, or supersede releases?

---

## Evidence

What information must survive after the release process completes?

---

# Desired Future State

The target FamilyOS release workflow is conceptually:

```text
CHANGE
  │
  ▼
IMPLEMENT
  │
  ▼
BUILD
  │
  ▼
TEST
  │
  ▼
QUALITY
  │
  ▼
COMPLIANCE
  │
  ▼
PREPARE RELEASE
  │
  ▼
VERIFY READINESS
  │
  ▼
CREATE RELEASE CANDIDATE
  │
  ▼
VALIDATE EXACT CANDIDATE
  │
  ▼
APPROVE
  │
  ▼
ASSIGN VERSION
  │
  ▼
CREATE OFFICIAL TAG
  │
  ▼
PUBLISH ARTIFACTS
  │
  ▼
VERIFY PUBLICATION
  │
  ▼
DISTRIBUTE
  │
  ▼
OBSERVE
  │
  ▼
MAINTAIN
```

Each significant transition has explicit criteria and evidence.

---

# Success Conditions

The Release Framework succeeds when FamilyOS can release components without depending on undocumented individual knowledge.

A successful release system must allow maintainers to answer:

```text
What are we releasing?

Why is it ready?

Where did it come from?

Which exact artifacts are included?

What version does it have?

Which repository state does it represent?

What validation has passed?

Who or what approved it?

Where was it published?

Can the release be reconstructed later?

What do we do if it fails?
```

If these questions can be answered consistently and objectively, the release engineering foundation is functioning correctly.

---

# Context Summary

FamilyOS already possesses many of the engineering capabilities required to create reliable software.

The missing capability is a formal system governing the final transition from validated engineering output to official release.

EPIC-REL-001 fills this gap.

It establishes release engineering as the connective layer between:

```text
Build
Testing
Quality
Compliance
Documentation
Security
Repository State
Versioning
Publication
Distribution
Recovery
```

The framework must preserve the discipline already established across FamilyOS while preventing release processes from becoming fragmented, manual, ambiguous, or dependent on individual memory.

By formalizing release identity, readiness, candidates, versioning, provenance, validation, tagging, publication, observability, governance, and recovery, FamilyOS gains the foundation required to release platform components safely and consistently as the ecosystem continues to grow.
