# Plugin Compliance Framework

# 13 Compliance Gates

## Introduction

Compliance Gates define the enforcement points at which FamilyOS determines whether a plugin may progress to the next engineering or lifecycle stage.

A compliance gate does not define new compliance requirements.

It evaluates the canonical Compliance Result against a governed gate policy.

The target progression is:

```text
Development
    │
    ▼
Merge Gate
    │
    ▼
Build Gate
    │
    ▼
Release Gate
    │
    ▼
Certification Gate
```

Each gate provides a stronger level of assurance.

---

# Purpose

The purpose of Compliance Gates is to convert compliance results into controlled lifecycle decisions.

They provide the foundation required to:

* prevent known non-compliance from progressing;
* enforce mandatory rules;
* block incomplete validation where assurance is required;
* distinguish infrastructure errors from plugin violations;
* support progressive assurance;
* integrate compliance with engineering governance;
* provide auditable lifecycle decisions;
* support governed exceptions;
* protect release and certification workflows.

Compliance gates must remain deterministic and policy-driven.

---

# Gate Principle

The governing gate principle is:

> A plugin may progress only when the assurance required by the next lifecycle stage has been demonstrated.

A gate therefore answers:

```text
Is the current compliance evidence sufficient to allow progression?
```

It must not answer this question through undocumented judgment.

---

# Gate Model

A conceptual gate contains:

```text
ComplianceGate
├── id
├── version
├── lifecycle_stage
├── required_profile
├── accepted_statuses
├── mandatory_rules
├── severity_policy
├── evidence_policy
├── exception_policy
├── failure_behavior
└── governance
```

The exact implementation schema may evolve.

The semantic model must remain explicit.

---

# Gate Identity

Every governed gate should have a stable identity.

Conceptual examples include:

```text
PLUGIN-GATE-DEVELOPMENT
PLUGIN-GATE-MERGE
PLUGIN-GATE-BUILD
PLUGIN-GATE-RELEASE
PLUGIN-GATE-CERTIFICATION
```

Gate identities allow:

* policy references;
* audit history;
* CI integration;
* release governance;
* versioned evolution.

---

# Gate Versioning

Gate policy must be versioned.

A gate decision should identify:

```text
Gate ID
Gate Version
Compliance Profile
Compliance Framework Version
```

This allows historical decisions to remain interpretable after governance evolves.

---

# Gate Evaluation

A gate consumes a finalized Compliance Result.

Conceptually:

```text
Compliance Result
       │
       ▼
Gate Policy
       │
       ▼
Gate Evaluation
       │
   ┌───┴────┐
   ▼        ▼
 PASS      BLOCK
```

A gate must not rerun compliance rules independently.

---

# Gate Decision Model

A conceptual Gate Decision contains:

```text
GateDecision
├── gate_id
├── gate_version
├── evaluation_id
├── plugin_id
├── compliance_status
├── decision
├── blocking_reasons
├── exceptions
├── timestamp
└── metadata
```

The decision should be machine-readable and auditable.

---

# Gate Decisions

The baseline gate decision vocabulary should remain compact.

Conceptually:

```text
PASS
BLOCK
ERROR
```

## PASS

The plugin satisfies the gate policy.

## BLOCK

The compliance result does not provide sufficient assurance for progression.

## ERROR

The gate itself cannot determine a reliable decision because of invalid policy or infrastructure failure.

---

# Compliance Status Handling

Gates must define how canonical compliance states are treated.

The baseline statuses are:

```text
COMPLIANT
NON_COMPLIANT
INCOMPLETE
ERROR
```

Gate policy determines which are acceptable.

For strong lifecycle stages, only:

```text
COMPLIANT
```

should normally permit progression.

---

# Non-Compliant Handling

A `NON_COMPLIANT` result normally causes the gate to block.

Conceptually:

```text
NON_COMPLIANT
      │
      ▼
Blocking Findings
      │
      ▼
Gate BLOCK
```

A governed exception may alter the gate decision only where both the affected rule and gate policy permit it.

---

# Incomplete Handling

`INCOMPLETE` means required assurance has not been demonstrated.

Strong gates must therefore treat incomplete validation as blocking.

For example:

```text
INCOMPLETE
    │
    ▼
Required Evidence Missing
    │
    ▼
Gate BLOCK
```

Absence of evidence must never be treated as permission to progress.

---

# Error Handling

A compliance result of:

```text
ERROR
```

means a reliable compliance decision could not be produced.

Release and certification gates must block in this state.

The problem may be infrastructure rather than plugin behavior, but progression remains unsafe until validation succeeds.

---

# Mandatory Rule Enforcement

Mandatory rules participate in every applicable gate.

A failed mandatory rule must not be neutralized by ordinary gate configuration.

Conceptually:

```text
Mandatory Rule FAIL
        │
        ▼
Gate BLOCK
```

unless the rule explicitly permits a governed exception and the gate accepts that exception.

---

# Severity-Based Blocking

Gate policies may consider finding severity.

A conceptual baseline is:

```text
CRITICAL -> block
ERROR    -> block
WARNING  -> gate-dependent
INFO     -> non-blocking
```

The rule severity remains unchanged.

The gate defines lifecycle consequence.

---

# Development Gate

The Development Gate provides the lightest formal assurance level.

Its purpose is to identify fundamental issues before code progresses deeper into the engineering lifecycle.

Typical requirements may include:

* valid plugin identity;
* valid metadata;
* structural compliance;
* critical architecture boundaries;
* critical dependency rules;
* critical security rules.

The Development Gate should remain fast enough for frequent use.

---

# Development Gate Policy

A conceptual policy may permit:

```text
COMPLIANT
```

with non-blocking warnings.

It should block:

* critical rule failures;
* mandatory rule failures;
* invalid plugin identity;
* unrecoverable compliance engine errors.

Some non-critical rules may remain unevaluated under a development profile.

---

# Merge Gate

The Merge Gate determines whether plugin changes may enter a protected integration branch.

It should provide stronger assurance than local development checks.

Typical requirements include:

* development gate requirements;
* static analysis;
* type checking;
* required tests;
* architecture compliance;
* capability compliance;
* dependency compliance;
* selected documentation checks.

---

# Merge Gate Policy

A protected branch may require:

```text
Compliance Status == COMPLIANT
```

for the configured merge profile.

Warnings may remain non-blocking if policy permits them.

Blocking findings must be visible to reviewers.

---

# Pull Request Gate

The Merge Gate may be implemented through pull request status checks.

Conceptually:

```text
Pull Request
    │
    ▼
CI Compliance
    │
    ▼
Merge Gate
    │
 ┌──┴───┐
 ▼      ▼
PASS   BLOCK
```

The gate should expose blocking reasons directly in the pull request workflow.

---

# Build Gate

The Build Gate determines whether a plugin may produce a governed build artifact.

It should require stronger evidence completeness than the Development or Merge Gate.

Typical requirements include:

* successful required tests;
* quality checks;
* dependency validation;
* complete required metadata;
* valid packaging inputs;
* no blocking architecture findings;
* no blocking security findings.

---

# Build Eligibility

The Build Gate may distinguish between:

```text
development build
```

and:

```text
release build
```

A local development artifact may use a weaker profile.

A release candidate build should use a stronger build or release profile.

The selected gate must remain explicit.

---

# Artifact Gate

After build completion, FamilyOS may evaluate the generated artifact itself.

Artifact validation may include:

* package contents;
* manifest integrity;
* version metadata;
* prohibited files;
* artifact digest;
* compatibility metadata.

This produces assurance that the built artifact still conforms to expectations.

---

# Release Gate

The Release Gate determines whether a plugin may enter an official release workflow.

This is a strong compliance gate.

It should normally require:

* full required compliance profile;
* complete trusted evidence;
* no blocking findings;
* no unresolved mandatory failures;
* validated compatibility;
* validated lifecycle behavior;
* complete required documentation;
* valid release metadata;
* exact artifact binding.

---

# Release Gate Model

Conceptually:

```text
Release Candidate
      │
      ▼
Full Compliance Evaluation
      │
      ▼
Release Gate
      │
   ┌──┴────┐
   ▼       ▼
 PASS     BLOCK
   │
   ▼
Release Eligible
```

A Release Gate pass means the plugin is compliance-eligible for release.

It does not itself publish the plugin.

---

# Release Gate and Warnings

The treatment of warnings at release time must be explicit.

Possible policies include:

```text
warnings allowed
warnings require approval
specific warning classes block
all warnings block
```

The framework should avoid a universal assumption that all warnings are equivalent.

---

# Release Evidence Requirements

Release gates should require stronger evidence provenance.

Examples include:

* CI-produced test evidence;
* trusted quality evidence;
* artifact-specific validation;
* platform compatibility evidence;
* current dependency analysis.

Local unverified evidence may be insufficient.

---

# Certification Gate

The Certification Gate determines whether a plugin may proceed into or complete a certification workflow.

The gate should consume a certification-profile Compliance Result.

Typical requirements include:

* `COMPLIANT` status;
* complete required evidence;
* accepted evidence trust;
* exact artifact identity;
* accepted framework version;
* no unresolved forbidden exceptions;
* no unresolved critical findings;
* certification eligibility.

---

# Certification Gate Boundary

The Certification Gate must remain separate from certification approval.

The relationship is:

```text
Compliance
    │
    ▼
Certification Gate
    │
    ▼
Certification Eligible
    │
    ▼
Certification Governance
    │
    ▼
Certified
```

Passing the gate does not automatically grant certification.

---

# Certification Eligibility

A compliance result may expose:

```text
ELIGIBLE
NOT_ELIGIBLE
```

The Certification Gate validates this against its own policy.

Eligibility is a technical precondition.

Certification may still require:

* provenance review;
* ownership verification;
* manual security review;
* governance approval;
* support commitments.

---

# Gate Profiles

Each gate should identify the exact profile required.

Conceptually:

```text
Development Gate -> development profile
Merge Gate       -> official or CI profile
Build Gate       -> build profile
Release Gate     -> release profile
Certification    -> certification profile
```

The exact mapping may vary by plugin classification.

---

# Gate Profile Escalation

A gate may require a stronger profile than the one previously evaluated.

For example:

```text
Merge Profile
     │
     ▼
Release Profile
```

The framework must execute or consume an appropriate new compliance evaluation.

A weaker prior result must not be reused as proof of stronger assurance.

---

# Gate Profile Downgrade

A gate must never silently downgrade its required profile.

For example:

```text
Release Profile fails
```

must not cause automatic fallback to:

```text
Official Profile
```

and then permit release.

Profile requirements are gate policy.

---

# Evidence Completeness

Gates may define required evidence completeness.

For example:

```text
Development Gate
  some non-critical evidence may be optional

Release Gate
  all blocking rule evidence required

Certification Gate
  all certification-required evidence required
```

The gate should clearly identify missing assurance.

---

# Evidence Trust Requirements

Gate policy may define minimum evidence trust.

Conceptually:

```text
Development
  LOCAL accepted

Merge
  CI TRUSTED preferred

Release
  TRUSTED required

Certification
  TRUSTED or ATTESTED required
```

This model is illustrative.

The final trust hierarchy must be governed explicitly.

---

# Artifact Binding Requirements

Release and certification gates should be capable of requiring exact artifact binding.

Conceptually:

```text
Compliance Result
      +
Artifact Digest
      =
Bound Assurance
```

A compliance result that cannot be connected to the artifact being released may be insufficient for strong gates.

---

# Gate Exceptions

Gate exceptions must be governed explicitly.

A conceptual exception flow is:

```text
Gate would BLOCK
      │
      ▼
Exception Request
      │
      ▼
Authority Review
      │
   ┌──┴────┐
   ▼       ▼
Denied   Approved
          │
          ▼
Conditional Gate Decision
```

Gate exceptions should be rare at stronger assurance levels.

---

# Rule Exceptions vs Gate Exceptions

Rule exceptions and gate exceptions are distinct.

A Rule Exception affects treatment of a specific compliance requirement.

A Gate Exception affects lifecycle progression despite the resulting compliance condition.

These must not be conflated.

A release gate may choose not to accept certain valid rule exceptions.

---

# Exception Constraints

A gate exception should define:

* gate;
* plugin;
* scope;
* justification;
* authority;
* expiration;
* conditions;
* affected findings;
* audit reference.

The decision must remain visible in lifecycle records.

---

# Non-Exemptible Gates

Some gate policies may prohibit exceptions for particular conditions.

Examples include:

* critical security violations;
* artifact integrity failures;
* invalid plugin identity;
* compliance engine tampering.

Such constraints protect the platform trust boundary.

---

# Temporary Gate Overrides

Temporary migration periods may require controlled gate overrides.

Overrides must be:

* explicit;
* scoped;
* time-limited;
* auditable;
* approved.

Temporary overrides must not become permanent hidden policy.

---

# Gate Expiration

Gate decisions should be contextual and may expire when underlying evidence becomes stale.

For example:

```text
Release Gate PASS
```

may become unusable after:

* artifact changes;
* source revision changes;
* dependency changes;
* compliance profile changes;
* critical policy updates.

A gate decision is not a permanent plugin property.

---

# Revalidation Before Progression

A gate may require fresh evaluation immediately before progression.

This is especially important for:

* release;
* certification;
* long-lived release candidates.

Revalidation should use current policy and evidence.

---

# Gate and Compliance Drift

A previously passed gate may no longer be valid after compliance drift.

Conceptually:

```text
Previous Gate PASS
      │
      ▼
Rule / Platform Change
      │
      ▼
Revalidation
      │
      ▼
Current Gate BLOCK
```

Historical gate decisions remain valid records of their original context.

They do not override current requirements.

---

# Gate Ordering

Lifecycle gates form a progressive assurance chain.

Conceptually:

```text
Development
    │
    ▼
Merge
    │
    ▼
Build
    │
    ▼
Release
    │
    ▼
Certification
```

Passing a stronger gate generally implies that requirements of weaker gates were satisfied or superseded in the same validation context.

The framework should not rely on this assumption without explicit profile composition.

---

# Gate Independence

Each gate must remain independently evaluable.

A Release Gate should not rely only on a historical Merge Gate pass.

It should consume a current release-grade Compliance Result.

This prevents stale lifecycle approvals.

---

# Gate Short-Circuiting

Some failures may justify stopping a workflow early.

For example:

```text
Critical Security Failure
        │
        ▼
Release Gate BLOCK
```

There may be no value in continuing publication stages.

However, validation should still collect useful findings when practical.

---

# Gate Failure Reasons

A blocked gate must expose clear reasons.

For example:

```text
Release Gate: BLOCK

Reasons:
- PLUGIN-SEC-009 CRITICAL
- PLUGIN-DOC-004 ERROR
- 2 required rules NOT_EVALUATED
```

Gate decisions should not produce opaque messages such as:

```text
Release denied.
```

without actionable context.

---

# Gate Reporting

Compliance reports should expose gate evaluation where relevant.

A report may include:

```text
Gate: RELEASE
Decision: BLOCK
Gate Version: 1.0.0
Blocking Findings: 2
Incomplete Rules: 1
```

Gate reporting remains separate from canonical rule outcomes.

---

# Gate and CI Status

CI systems may expose gate decisions as status checks.

Examples include:

```text
Plugin Compliance — Merge Gate
Plugin Compliance — Release Gate
```

The CI provider should not independently redefine pass or failure semantics.

---

# Branch Protection

Protected branches may require a Merge Gate pass before changes can be integrated.

Conceptually:

```text
Pull Request
    │
    ▼
Merge Gate PASS
    │
    ▼
Branch Merge Allowed
```

Branch policy belongs to engineering governance.

The gate supplies the compliance decision.

---

# Build System Integration

Build systems may require a Build Gate pass before generating distributable artifacts.

A failed gate should prevent release-grade artifact production.

Developer-local builds may use separate policy.

---

# Release System Integration

Release automation should require an accepted Release Gate decision associated with the exact release candidate.

The release system should verify:

* Gate ID;
* Gate version;
* Evaluation ID;
* artifact identity;
* decision;
* expiration or freshness where applicable.

---

# Certification Integration

Certification systems should consume a Certification Gate decision and underlying Compliance Result.

They may independently validate:

* evidence trust;
* artifact digest;
* governance approvals;
* certification policy.

Certification must not depend only on human-readable gate output.

---

# Gate Audit Trail

Every gate evaluation should produce an audit trail including:

```text
Gate ID
Gate Version
Evaluation ID
Plugin
Plugin Version
Artifact
Compliance Status
Blocking Reasons
Exceptions
Decision
Authority
Timestamp
```

This supports lifecycle traceability.

---

# Gate Decision Immutability

A finalized Gate Decision should be immutable.

If policy or evidence changes, a new gate evaluation must be created.

For example:

```text
Gate Evaluation A -> PASS
Gate Evaluation B -> BLOCK
```

Both remain valid historical records of their respective contexts.

---

# Gate History

A plugin lifecycle may eventually expose:

```text
Merge Gate         PASS
Build Gate         PASS
Release Gate       PASS
Certification Gate BLOCK
```

This provides a clear assurance history.

Each decision should reference the compliance evaluation that produced it.

---

# Gate Metrics

Operational systems may track metrics such as:

* gate pass rate;
* gate block rate;
* blocking domains;
* blocking severities;
* time to remediation;
* exception frequency;
* expired gate decisions.

Metrics support framework improvement.

They must not redefine compliance semantics.

---

# Gate Quality

Gate policy itself requires validation.

A malformed gate configuration can cause unsafe lifecycle decisions.

The framework should validate:

* known profile references;
* valid accepted statuses;
* mandatory rules;
* severity mappings;
* exception policy;
* evidence requirements.

Invalid gate policy should produce a gate infrastructure error.

---

# Gate Testing

Compliance Gates require dedicated tests.

Core test categories include:

* compliant pass;
* non-compliant block;
* incomplete block;
* infrastructure error;
* mandatory rule failure;
* warning policy;
* critical finding handling;
* rule exception handling;
* gate exception handling;
* expired exception handling;
* artifact binding;
* deterministic decision;
* immutable decision history.

---

# Cross-Gate Tests

FamilyOS should test expected progression across lifecycle gates.

For example:

```text
Development PASS
Merge PASS
Build PASS
Release PASS
Certification PASS
```

and failure scenarios such as:

```text
Merge PASS
Release BLOCK
```

when stronger requirements apply.

---

# Gate Anti-Patterns

The framework must avoid several gate anti-patterns.

## Gate Defines Rules

A gate must not invent compliance requirements outside the Rule Catalog.

## Silent Downgrade

A failing strong gate must not fall back to a weaker profile.

## Missing Evidence as Pass

A strong gate must not accept incomplete validation as compliance.

## Exception Without Traceability

No lifecycle progression should occur through an undocumented exception.

## CI Success Equals Compliance

A generic successful CI pipeline must not be assumed to mean a compliance gate passed.

## Historical Pass Reuse

A prior gate pass must not be reused after relevant context changes without freshness validation.

## Manual Override Without Policy

Human authority must operate through governed exception mechanisms.

---

# Initial Gate Baseline

The initial framework implementation should establish at least:

```text
Development Gate
Merge Gate
Release Gate
```

A Build Gate and Certification Gate may mature alongside the Build and Certification frameworks.

The initial baseline should prioritize official plugin enforcement.

---

# Official Plugin Gate Baseline

For official plugins, the target progression is:

```text
Development Compliance
        │
        ▼
Merge Gate
        │
        ▼
Full Official Compliance
        │
        ▼
Release Gate
        │
        ▼
Release Eligibility
```

Certification requirements may be introduced as the certification system matures.

---

# Future Gate Capabilities

Future evolution may include:

* signed gate decisions;
* remote gate verification;
* registry admission gates;
* deployment gates;
* periodic certification renewal gates;
* environment-specific gates;
* organization-specific policy overlays.

These extensions must consume the same canonical compliance model.

---

# Gate Invariants

The Compliance Gate model establishes the following invariants:

1. Gates consume finalized Compliance Results.
2. Gates do not define independent compliance rules.
3. Every gate has an explicit policy.
4. Strong gates normally require `COMPLIANT`.
5. `NON_COMPLIANT` blocks progression unless governed policy explicitly permits otherwise.
6. `INCOMPLETE` does not provide sufficient assurance for strong gates.
7. `ERROR` prevents reliable gate progression.
8. Mandatory rule failures cannot be silently bypassed.
9. Gate profiles are explicit.
10. Gates never silently downgrade profiles.
11. Evidence trust may become stronger across lifecycle stages.
12. Release and certification gates may require exact artifact binding.
13. Exceptions remain explicit and auditable.
14. Rule exceptions and gate exceptions remain distinct.
15. Gate decisions identify the compliance evaluation they consume.
16. Finalized gate decisions are immutable.
17. Gate passes may require revalidation after relevant context changes.
18. Historical gate decisions do not override current policy.
19. Gate consumers must use structured decisions rather than infer semantics from logs.
20. Certification Gate pass does not itself grant certification.

---

# Reference Gate Model

The complete lifecycle model is:

```text
Plugin Development
       │
       ▼
Compliance Evaluation
       │
       ▼
Development Gate
       │
       ▼
Merge
       │
       ▼
Compliance Evaluation
       │
       ▼
Build Gate
       │
       ▼
Build Artifact
       │
       ▼
Release Compliance
       │
       ▼
Release Gate
       │
       ▼
Release Eligible
       │
       ▼
Certification Compliance
       │
       ▼
Certification Gate
       │
       ▼
Certification Eligible
```

Each stage increases the required level of assurance.

---

# Gate Summary

Compliance Gates convert compliance evidence into lifecycle enforcement.

The model can be summarized as:

```text
Compliance Result
       +
Gate Policy
       +
Lifecycle Context
       =
Gate Decision
```

A Gate Decision controls progression but never changes the meaning of the underlying compliance result.

---

# Final Gate Principle

The governing principle of Compliance Gates is:

> Progression through the FamilyOS plugin lifecycle must be earned through the level of compliance evidence required by the next stage.

This principle ensures that plugins cannot move from development to integration, build, release, or certification without demonstrating the corresponding level of platform conformance.
