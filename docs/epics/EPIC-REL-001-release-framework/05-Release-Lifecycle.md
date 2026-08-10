# Release Framework

# 05 Release Lifecycle

## Overview

EPIC-REL-001 — Release Framework defines a canonical release lifecycle for FamilyOS.

The lifecycle governs the transition from release intent to completed official release.

Its purpose is to ensure that release state is:

* explicit;
* traceable;
* validatable;
* observable;
* governable;
* recoverable.

A release lifecycle must not depend on informal interpretation of repository tags, terminal history, CI/CD output, or artifact availability.

Each significant release stage must have a defined meaning.

---

# Purpose

The Release Lifecycle establishes:

* canonical release states;
* transition rules;
* release gates;
* normal progression;
* blocked states;
* failure states;
* recovery paths;
* withdrawal semantics;
* supersession semantics;
* completion semantics.

The lifecycle provides the common state model used by release planning, release candidates, validation, automation, governance, publishing, observability, and recovery.

---

# Lifecycle Principle

The central lifecycle principle is:

> Release state must be explicit rather than inferred.

For example:

```text
tag exists
```

does not necessarily mean:

```text
release completed successfully
```

Similarly:

```text
artifact uploaded
```

does not necessarily mean:

```text
release published correctly
```

The lifecycle therefore separates preparation, qualification, approval, publication, verification, and completion.

---

# Canonical Lifecycle

The canonical FamilyOS release lifecycle is:

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

Exceptional states include:

```text
BLOCKED
FAILED
WITHDRAWN
SUPERSEDED
ROLLED_BACK
```

Not every release profile must expose every state independently.

However, equivalent lifecycle semantics must remain preserved.

---

# Lifecycle Phases

The lifecycle may be grouped into five major phases.

```text
Planning Phase
    PLANNED

Preparation Phase
    PREPARED
    READY

Qualification Phase
    CANDIDATE
    VALIDATED
    APPROVED

Publication Phase
    RELEASED
    PUBLISHED
    DISTRIBUTED

Completion Phase
    COMPLETED
```

Exceptional states may occur across several phases.

---

# State Model

Each lifecycle state has:

* entry criteria;
* permitted operations;
* expected evidence;
* allowed transitions;
* exit criteria.

A state transition should occur only when its conditions are satisfied.

---

# PLANNED

## Definition

`PLANNED` represents a release that has been identified but is not yet prepared for formal qualification.

A planned release may have:

* intended scope;
* intended release type;
* tentative version;
* target milestone;
* expected components;
* planned release window;
* known dependencies.

The release is not yet considered ready for candidate creation.

---

## Typical Inputs

Inputs may include:

* roadmap milestone;
* completed feature scope;
* maintenance requirement;
* security requirement;
* framework completion;
* plugin update;
* documentation release need.

---

## Expected Evidence

Planning evidence may include:

```text
release intent
release scope
target component
target release type
known dependencies
```

---

## Permitted Transitions

```text
PLANNED → PREPARED
PLANNED → BLOCKED
PLANNED → CANCELLED
```

Where cancellation is represented operationally, it may remain a planning outcome rather than a long-lived official release state.

---

# PREPARED

## Definition

`PREPARED` means that the release scope and required release materials have been assembled sufficiently for readiness evaluation.

Preparation may include:

* source state identification;
* component selection;
* intended version identification;
* artifact expectations;
* release documentation preparation;
* required checks identification;
* release profile selection;
* risk identification.

The release is still not considered release-ready.

---

## Entry Criteria

Typical entry criteria include:

* release scope known;
* target component known;
* release type known;
* required release profile identified.

---

## Exit Criteria

A release may leave `PREPARED` when readiness evaluation can begin.

---

## Permitted Transitions

```text
PREPARED → READY
PREPARED → BLOCKED
PREPARED → PLANNED
```

Returning to `PLANNED` may be appropriate when release scope changes materially.

---

# READY

## Definition

`READY` means that the release has satisfied applicable readiness criteria and may become a formal release candidate.

Readiness may require:

* successful build;
* required tests passing;
* quality gates passing;
* compliance status acceptable;
* security checks acceptable;
* documentation ready;
* repository state valid;
* known risks evaluated.

`READY` represents qualification readiness, not final release approval.

---

# Readiness Gate

The transition:

```text
PREPARED → READY
```

is controlled by the Release Readiness Gate.

Conceptually:

```text
Build                 PASS
Tests                 PASS
Quality               PASS
Compliance            PASS
Security              PASS
Documentation         PASS
Repository            PASS
Risk                  ACCEPTABLE
--------------------------------
READINESS             PASS
```

The exact requirements depend on the applicable release profile.

---

# Readiness Failure

If readiness requirements are not satisfied, the release must not transition to `READY`.

Possible outcomes include:

```text
BLOCKED
```

or:

```text
PREPARED
```

with required remediation.

---

# CANDIDATE

## Definition

`CANDIDATE` identifies the exact release configuration submitted for final release qualification.

The candidate must be sufficiently stable that validation evidence can be meaningfully associated with it.

A candidate may contain:

```text
candidate identifier
source revision
intended version
build identity
artifact set
release metadata
release notes
validation scope
```

---

# Candidate Creation Gate

The transition:

```text
READY → CANDIDATE
```

requires candidate creation.

Candidate creation should establish:

* candidate identity;
* source identity;
* artifact identity;
* release scope;
* intended version;
* provenance relationship.

---

# Candidate Stability

Once candidate validation begins, material candidate changes should invalidate the candidate or its affected validation evidence.

Material changes may include:

* source changes;
* artifact changes;
* dependency changes;
* release configuration changes;
* significant release metadata changes;
* compatibility changes.

The preferred model is:

```text
Candidate 1
    ↓
change required
    ↓
Candidate 2
```

rather than mutating Candidate 1 without renewed qualification.

---

# Candidate Iteration

Several candidate iterations may exist before final release.

Example:

```text
v4.8.0-rc.1
     ↓
validation failure
     ↓
fix
     ↓
v4.8.0-rc.2
     ↓
validation pass
```

Each candidate iteration must remain traceable.

---

# VALIDATED

## Definition

`VALIDATED` means that the actual release candidate has passed applicable final release validation.

Validation may include:

* source verification;
* artifact verification;
* version verification;
* provenance verification;
* final test verification;
* packaging checks;
* documentation checks;
* security checks;
* compliance checks;
* compatibility checks;
* installation checks.

Validation must apply to the candidate intended for release.

---

# Validation Gate

The transition:

```text
CANDIDATE → VALIDATED
```

is controlled by the Release Validation Gate.

The result is conceptually:

```text
Candidate Integrity      PASS
Artifact Verification    PASS
Version                  PASS
Tests                    PASS
Quality                  PASS
Security                 PASS
Compliance               PASS
Documentation            PASS
--------------------------------
VALIDATION               PASS
```

---

# Validation Failure

If final validation fails:

```text
CANDIDATE → BLOCKED
```

or:

```text
CANDIDATE → FAILED
```

depending on whether remediation is expected within the same release effort.

A corrected candidate should normally receive a new candidate identity.

---

# APPROVED

## Definition

`APPROVED` means that the validated candidate has received all required governance approval for release.

Approval may include:

* maintainer approval;
* release owner approval;
* risk acceptance;
* security approval;
* emergency authorization;
* exception approval.

Not every release requires manual approval.

Some low-risk release profiles may allow policy-driven automatic approval.

However, approval semantics must remain explicit.

---

# Approval Gate

The transition:

```text
VALIDATED → APPROVED
```

is controlled by governance.

Possible outcomes include:

```text
APPROVE
BLOCK
EXCEPTION REQUIRED
```

---

# Approval Evidence

Approval evidence may record:

* approver;
* time;
* candidate identity;
* accepted risk;
* exceptions;
* approval scope.

---

# RELEASED

## Definition

`RELEASED` means that the candidate has been assigned its final official release identity and the authoritative repository release anchor has been established.

For Git-based FamilyOS releases, this may include:

* final version;
* official annotated tag;
* exact source commit.

The transition to `RELEASED` creates a durable official release identity.

It does not necessarily mean that all artifacts have already been published externally.

---

# Release Identity Gate

The transition:

```text
APPROVED → RELEASED
```

requires:

* final version confirmation;
* version uniqueness;
* source state verification;
* repository state verification;
* official release tag creation where applicable.

Conceptually:

```text
Validated Candidate
      ↓
Approved
      ↓
Version Assigned
      ↓
Official Tag Created
      ↓
RELEASED
```

---

# Why RELEASED and PUBLISHED Are Separate

The distinction prevents the architecture from assuming that repository tagging and artifact publication are one atomic operation.

For example:

```text
tag created successfully
artifact publication failed
```

The release has acquired an official repository identity but publication is incomplete.

This state must remain observable.

---

# PUBLISHED

## Definition

`PUBLISHED` means that the release has been made available through its authoritative publication targets.

Depending on the release type, publication may include:

* Git hosting release;
* package registry;
* artifact registry;
* documentation publication;
* plugin registry;
* release metadata;
* source archives.

Publication must be verified.

---

# Publication Gate

The transition:

```text
RELEASED → PUBLISHED
```

requires successful execution and verification of all mandatory publication targets.

A partial publication must not be treated as `PUBLISHED` unless policy explicitly defines a target subset as sufficient.

---

# Partial Publication

If some publication targets succeed and others fail, the release may transition to:

```text
FAILED
```

while preserving publication evidence.

Example:

```text
Git Tag              PASS
Repository Release   PASS
Package Registry     FAIL
Documentation        NOT STARTED
--------------------------------
Release State        FAILED
```

Recovery must begin from the actual recorded state.

---

# DISTRIBUTED

## Definition

`DISTRIBUTED` means that the published release has been promoted or made available to its intended consumer scope.

Distribution may include:

* stable channel activation;
* plugin channel promotion;
* package availability;
* documentation visibility;
* downstream synchronization;
* controlled rollout.

Not all release profiles require a distinct distribution stage.

---

# Distribution Gate

The transition:

```text
PUBLISHED → DISTRIBUTED
```

requires applicable distribution operations to complete successfully.

This may include post-publication verification before promotion.

---

# COMPLETED

## Definition

`COMPLETED` represents successful finalization of the release lifecycle.

A release should reach `COMPLETED` only after all applicable release obligations have been satisfied.

These may include:

* release identity finalized;
* official tag available remotely;
* artifacts published;
* publication verified;
* distribution complete;
* release notes available;
* release evidence recorded;
* repository final state validated;
* post-release verification completed.

---

# Completion Gate

The final transition:

```text
DISTRIBUTED → COMPLETED
```

or, for simpler profiles:

```text
PUBLISHED → COMPLETED
```

requires successful finalization.

Completion must be explicit.

---

# Completed Release Invariant

Once a release reaches `COMPLETED`, its historical identity should remain stable.

Later lifecycle events may change operational status, such as:

```text
COMPLETED → SUPERSEDED
COMPLETED → WITHDRAWN
```

but must not rewrite the original release history.

---

# BLOCKED

## Definition

`BLOCKED` means that release progression cannot continue because one or more required conditions are not satisfied.

A blocked release is not necessarily failed permanently.

Typical causes include:

* failed tests;
* unresolved quality gate;
* missing documentation;
* invalid version;
* unresolved security issue;
* missing approval;
* invalid repository state;
* dependency incompatibility;
* release risk requiring decision.

---

# Blocked State Behavior

A blocked release must identify:

* blocking condition;
* current lifecycle stage;
* required remediation;
* responsible owner where applicable.

After remediation, the release may return to an appropriate active state.

Example:

```text
CANDIDATE
   ↓
validation issue
   ↓
BLOCKED
   ↓
fix
   ↓
new CANDIDATE
```

---

# FAILED

## Definition

`FAILED` means that a release operation encountered a failure after meaningful release execution began.

This is especially important when side effects may already have occurred.

Typical failures include:

* tag creation failure;
* partial publication;
* registry failure;
* distribution failure;
* post-release verification failure.

---

# Failure Evidence

A failed release must preserve:

```text
stage
candidate
version
completed operations
failed operation
external side effects
error
recovery requirement
```

---

# Failed vs Blocked

The distinction is:

```text
BLOCKED
release cannot continue because prerequisite is unsatisfied

FAILED
release execution attempted and failed
```

A validation failure before publication may often be considered blocked.

A partial publication failure is more naturally considered failed.

---

# WITHDRAWN

## Definition

`WITHDRAWN` means that an official release has been intentionally removed from normal consumption because it should no longer be used or distributed.

Withdrawal may be necessary because of:

* severe defect;
* security vulnerability;
* invalid artifact;
* release integrity problem;
* incorrect publication;
* governance decision.

Withdrawal does not erase release history.

---

# Withdrawal Invariant

A withdrawn release remains historically identifiable.

The lifecycle should preserve:

```text
release identity
source revision
original publication
withdrawal reason
withdrawal date
replacement guidance
```

---

# SUPERSEDED

## Definition

`SUPERSEDED` means that a later official release replaces the release as the preferred version.

Supersession is a normal lifecycle outcome.

For example:

```text
v4.8.0
   ↓
v4.8.1 published
   ↓
v4.8.0 SUPERSEDED
```

Superseded releases may remain available unless policy requires removal.

---

# ROLLED_BACK

## Definition

`ROLLED_BACK` means that a release was published or distributed but the active consumer state was intentionally returned to a previous release.

The release itself remains part of history.

Rollback does not mean that the release never existed.

---

# Rollback Relationship

Conceptually:

```text
Release B
   ↓
problem detected
   ↓
rollback
   ↓
Release A restored
```

Release B may then become:

```text
ROLLED_BACK
WITHDRAWN
SUPERSEDED
```

depending on policy.

---

# Normal Transition Model

The normal lifecycle path is:

```text
PLANNED
   │
   ▼
PREPARED
   │
   ▼
READY
   │
   ▼
CANDIDATE
   │
   ▼
VALIDATED
   │
   ▼
APPROVED
   │
   ▼
RELEASED
   │
   ▼
PUBLISHED
   │
   ▼
DISTRIBUTED
   │
   ▼
COMPLETED
```

---

# Exceptional Transition Model

Exceptional transitions may include:

```text
PLANNED   → BLOCKED
PREPARED  → BLOCKED
READY     → BLOCKED
CANDIDATE → BLOCKED
VALIDATED → BLOCKED

RELEASED    → FAILED
PUBLISHED   → FAILED
DISTRIBUTED → FAILED

COMPLETED → SUPERSEDED
COMPLETED → WITHDRAWN
COMPLETED → ROLLED_BACK
```

The exact transition matrix may evolve with implementation.

---

# State Regression

Release progression should normally move forward.

However, controlled regression may be necessary.

Examples:

```text
READY → PREPARED
```

when release scope changes.

```text
VALIDATED → CANDIDATE
```

when renewed validation is required.

```text
APPROVED → CANDIDATE
```

when material changes invalidate approval.

State regression must be explicit.

---

# Candidate Invalidation

A candidate should be invalidated when material inputs change.

Examples include:

* source revision changes;
* artifact set changes;
* build configuration changes;
* dependency changes;
* compatibility assumptions change;
* final version changes in a way that affects artifacts.

Candidate invalidation should produce a new candidate iteration.

---

# Approval Invalidation

Approval may be invalidated when:

* candidate changes;
* material risk changes;
* security status changes;
* compliance status changes;
* release scope changes;
* exception conditions change.

Approval must always correspond to the actual release candidate and applicable risk state.

---

# Version Finalization

A release version may be tentative during early lifecycle states.

A conceptual progression is:

```text
PLANNED
tentative version

CANDIDATE
candidate version

APPROVED
final version intent

RELEASED
official version
```

The authoritative versioning rules are defined in `06-Versioning-Strategy.md`.

---

# Tag Timing

Official release tags should be created only when the lifecycle has reached the appropriate release identity stage.

The preferred model is:

```text
VALIDATED
   ↓
APPROVED
   ↓
verify repository state
   ↓
create official tag
   ↓
RELEASED
```

Creating final official tags before qualification increases ambiguity.

---

# Release Gate Model

The lifecycle contains several gates.

```text
Preparation Gate
Readiness Gate
Candidate Gate
Validation Gate
Approval Gate
Release Identity Gate
Publication Gate
Distribution Gate
Completion Gate
```

Each gate protects a state transition.

---

# Gate Outcomes

A gate should produce one of a small number of explicit outcomes.

```text
PASS
BLOCK
FAIL
EXCEPTION_REQUIRED
```

Not every gate requires all outcomes.

---

# Gate Evidence

Gate execution should preserve evidence sufficient to explain the result.

Conceptually:

```text
gate
candidate
result
checks
timestamp
actor
exceptions
```

---

# Release Profiles

Release profiles may simplify the lifecycle.

For example, a documentation-only framework release may use:

```text
PREPARED
   ↓
READY
   ↓
VALIDATED
   ↓
APPROVED
   ↓
RELEASED
   ↓
COMPLETED
```

while a distributed platform release may use the complete lifecycle.

Profiles may compress states operationally.

They must not remove essential release semantics.

---

# Framework Release Lifecycle

The current FamilyOS framework release pattern can map to the lifecycle as follows:

```text
documentation work complete
        ↓
PREPARED

framework checks pass
        ↓
READY

final repository state selected
        ↓
CANDIDATE

documentation / quality validation
        ↓
VALIDATED

release decision
        ↓
APPROVED

commit + version + annotated tag
        ↓
RELEASED

push branch + tag
        ↓
PUBLISHED

verify remote state
        ↓
COMPLETED
```

This mapping provides a direct path from current practices to the formal Release Framework.

---

# Plugin Release Lifecycle

A future official plugin release may use:

```text
PLANNED
   ↓
PREPARED
   ↓
READY
   ↓
CANDIDATE
   ↓
Plugin Tests
   ↓
Plugin Compliance
   ↓
Compatibility Validation
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

---

# Emergency Release Lifecycle

Emergency releases require an accelerated but controlled lifecycle.

An example is:

```text
INCIDENT
   ↓
PREPARED
   ↓
EMERGENCY READINESS
   ↓
CANDIDATE
   ↓
MINIMUM REQUIRED VALIDATION
   ↓
EMERGENCY APPROVAL
   ↓
RELEASED
   ↓
PUBLISHED
   ↓
VERIFIED
   ↓
COMPLETED
```

Emergency paths may compress planning.

They must retain identity, traceability, validation, approval, and recovery.

---

# Security Release Lifecycle

A security-sensitive release may introduce additional controls.

Possible sequence:

```text
PREPARED
   ↓
restricted readiness
   ↓
candidate
   ↓
security validation
   ↓
coordinated approval
   ↓
controlled publication
   ↓
advisory publication
   ↓
distribution
   ↓
verification
```

The Release Framework supports these extensions without redefining core states.

---

# Lifecycle Idempotency

Release workflows should support safe retry where possible.

For each state transition, tooling should determine whether the transition:

* has not started;
* completed successfully;
* completed partially;
* already exists;
* requires recovery.

Example:

```text
create tag
   ↓
tag already exists
   ↓
verify target commit
   ↓
if identical → continue safely
if different → block
```

---

# Lifecycle Atomicity

Some transitions may be nearly atomic.

Others inherently span several systems.

The architecture should distinguish:

```text
atomic state transition
```

from:

```text
multi-step state transition
```

Multi-step transitions must preserve intermediate state.

---

# Publication Transaction Model

A publication may conceptually act as a transaction.

```text
BEGIN PUBLICATION

create release metadata
publish artifacts
publish release notes
verify targets

COMMIT RELEASE STATE
```

If perfect rollback is impossible, the workflow must still preserve enough state for controlled recovery.

---

# Post-Release Verification

Publication alone is insufficient.

Post-release verification should confirm applicable conditions such as:

* tag visible remotely;
* release object exists;
* expected artifacts exist;
* artifact checksums match;
* release notes visible;
* package registry resolves correct version;
* channel references correct release.

Only after these checks should the release progress toward completion.

---

# Completion Evidence

A completed release should have a final evidence summary.

Conceptually:

```text
Release: vX.Y.Z

Source                VERIFIED
Candidate             VALIDATED
Approval              APPROVED
Version               FINAL
Tag                   VERIFIED
Artifacts             PUBLISHED
Release Notes         PUBLISHED
Distribution          VERIFIED
Evidence              RECORDED

State: COMPLETED
```

---

# Lifecycle Observability

Every significant state change should be observable.

Potential events include:

```text
release.planned
release.prepared
release.ready
release.candidate.created
release.validated
release.approved
release.released
release.published
release.distributed
release.completed
release.blocked
release.failed
release.withdrawn
release.superseded
release.rolled_back
```

The exact event format is an implementation concern.

---

# Lifecycle Auditability

State transitions should eventually preserve:

* previous state;
* new state;
* candidate;
* release version;
* actor or automation identity;
* timestamp;
* supporting evidence;
* exceptions.

This provides a durable release history.

---

# Lifecycle Security

Sensitive transitions require stronger protection.

Examples include:

```text
APPROVED → RELEASED
RELEASED → PUBLISHED
PUBLISHED → DISTRIBUTED
COMPLETED → WITHDRAWN
```

These transitions may require additional authorization.

---

# Lifecycle Governance

Governance determines which transitions may occur automatically and which require explicit approval.

For example:

```text
PREPARED → READY
```

may be entirely automated.

```text
VALIDATED → APPROVED
```

may require human approval for major releases.

```text
APPROVED → RELEASED
```

may require controlled release authority.

---

# Lifecycle Compliance

Release compliance may evaluate both:

* state requirements;
* transition requirements.

Examples:

```text
Candidate MUST exist before final validation.

Official release tag MUST NOT precede required approval.

Published release MUST have required release notes.

Withdrawn release MUST preserve historical identity.
```

---

# Release Lifecycle Record

A future FamilyOS implementation may maintain a machine-readable lifecycle record.

Illustrative example:

```text
release:
  version: 4.8.0
  state: completed

candidate:
  id: 4.8.0-rc.2

source:
  revision: abc123

transitions:
  - prepared
  - ready
  - candidate
  - validated
  - approved
  - released
  - published
  - completed
```

This is conceptual rather than a required schema.

---

# Lifecycle Invariants

The following invariants apply.

## L1 — Every release has an explicit current state.

## L2 — State transitions are deliberate.

## L3 — Required gates must pass before protected transitions.

## L4 — Candidate validation applies to the actual candidate.

## L5 — Material candidate change invalidates affected evidence.

## L6 — Approval applies to a specific validated candidate.

## L7 — Official release identity is established before publication completion.

## L8 — Publication must be verified.

## L9 — Partial failure must remain visible.

## L10 — Completed release history must remain stable.

## L11 — Withdrawal must not erase historical identity.

## L12 — Recovery must operate from recorded actual state.

---

# Lifecycle Anti-Patterns

## Implicit State

Using tag presence, file existence, or CI success as the only indicator of release state.

---

## Skipped Qualification

Moving directly from successful build to publication.

---

## Candidate Mutation

Changing candidate contents after validation without renewing evidence.

---

## Approval Drift

Using approval obtained for a previous candidate.

---

## Premature Tagging

Creating final official release tags before applicable release gates complete.

---

## Publication Equals Completion

Declaring release completion immediately after artifact upload.

---

## Hidden Partial Failure

Losing track of which publication targets succeeded.

---

## Historical Erasure

Deleting release evidence because a release was withdrawn.

---

# Minimum Lifecycle

The minimum acceptable FamilyOS release lifecycle is:

```text
PREPARE
   ↓
VERIFY
   ↓
VALIDATE
   ↓
APPROVE
   ↓
IDENTIFY
   ↓
PUBLISH
   ↓
VERIFY
   ↓
COMPLETE
```

This minimum lifecycle may be implemented with simple tooling.

Its semantics must remain explicit.

---

# Target Lifecycle

At higher maturity, FamilyOS should support:

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
        │
        ├── SUPERSEDED
        ├── WITHDRAWN
        └── ROLLED_BACK
```

with structured state, policies, evidence, automation, and recovery.

---

# Relationship With Other Release Documents

The Release Lifecycle provides the state model used by:

`06-Versioning-Strategy.md` for version transitions.

`07-Release-Types-and-Channels.md` for release profile and channel progression.

`08-Release-Planning.md` for the planning and preparation phases.

`09-Release-Readiness.md` for the `PREPARED → READY` gate.

`10-Release-Candidates.md` for candidate creation and mutation rules.

`12-Release-Validation.md` for the `CANDIDATE → VALIDATED` gate.

`16-Tagging-and-Repository-State.md` for the `APPROVED → RELEASED` transition.

`17-Publishing-and-Distribution.md` for publication and distribution states.

`18-Rollback-and-Recovery.md` for exceptional and recovery transitions.

`20-Release-Observability.md` for lifecycle event visibility.

`21-Release-Governance.md` for transition authority.

---

# Final Statement

The FamilyOS Release Lifecycle establishes the authoritative state model for release progression.

It prevents release status from being inferred from isolated technical side effects and instead defines a controlled sequence from planning through qualification, approval, publication, verification, and completion.

By making release states, gates, failure conditions, exceptional outcomes, and recovery transitions explicit, FamilyOS gains a lifecycle that can evolve from disciplined manual execution to automated release orchestration without sacrificing traceability or governance.
