# Plugin Compliance Framework

# 22 Release

## Introduction

The release of the Plugin Compliance Framework marks the transition from architectural definition to an officially governed FamilyOS engineering capability.

A framework release does not merely publish documentation or implementation artifacts.

It establishes a specific version of the compliance contract under which plugins may be evaluated.

A framework release therefore requires confidence that:

* its architecture is coherent;
* its rules are governed;
* its profiles are valid;
* its validators are reliable;
* its evidence semantics are stable;
* its reports are reproducible;
* its lifecycle impact is understood;
* its compatibility expectations are documented.

The release process must preserve the trustworthiness of the compliance system itself.

---

# Purpose

This document defines the release principles and requirements for EPIC-PLUGIN-002.

It establishes how the Plugin Compliance Framework should move through:

```text
Development
    │
    ▼
Validation
    │
    ▼
Release Candidate
    │
    ▼
Release Approval
    │
    ▼
Framework Release
    │
    ▼
Adoption
    │
    ▼
Enforcement
```

The framework must not become authoritative merely because implementation exists.

Authority follows validated and governed release.

---

# Release Principle

The governing release principle is:

> Every compliance decision must be attributable to an identifiable and reproducible framework release.

A plugin evaluated under one framework version must not be represented as though it had been evaluated under another.

---

# Release Scope

A framework release may include changes to:

* documentation;
* rule definitions;
* profiles;
* validators;
* evidence schemas;
* finding schemas;
* reporting schemas;
* gate policies;
* CLI integration;
* CI integration;
* governance metadata;
* security controls.

The release process must understand which of these components affect compliance semantics.

---

# Release Unit

The Plugin Compliance Framework should be treated as one governed release unit even when its implementation spans multiple packages or repositories.

The release identity should provide a stable reference for:

```text
Framework Version
Policy Version
Schema Compatibility
Validation Semantics
```

A Compliance Result must record the framework version used during evaluation.

---

# Release Identity

Every official framework release must have an explicit version.

Conceptually:

```text
Plugin Compliance Framework
Version: X.Y.Z
```

The version must be available to:

* CLI consumers;
* CI consumers;
* reports;
* release workflows;
* certification workflows;
* historical audits.

---

# Versioning

The framework should follow the FamilyOS release strategy and semantic versioning principles where appropriate.

Conceptually:

```text
MAJOR.MINOR.PATCH
```

Version changes communicate expected compatibility impact.

---

# Major Release

A major release may be required when framework semantics change incompatibly.

Examples include:

* incompatible Compliance Result model;
* incompatible rule semantics;
* major profile restructuring;
* incompatible evidence model;
* breaking gate semantics;
* removal of previously supported contracts.

Major releases require explicit migration planning.

---

# Minor Release

A minor release may introduce backward-compatible capability.

Examples include:

* new optional rules;
* new validators;
* new evidence adapters;
* new report formats;
* new non-breaking profiles;
* additional diagnostics.

A minor release should not unexpectedly invalidate previously valid stable workflows.

---

# Patch Release

A patch release should preserve intended compliance semantics.

Examples include:

* validator bug fixes;
* documentation corrections;
* reporting corrections;
* remediation improvements;
* non-semantic internal improvements.

A patch release must not intentionally introduce a new mandatory blocking requirement.

---

# Policy Versioning

Framework implementation version and compliance policy version may eventually require independent identification.

For example:

```text
Framework Engine: 2.3.1
Policy Bundle: 2.4.0
```

The architecture should permit this distinction if independent policy distribution becomes useful.

Initially, one framework release version may govern both.

---

# Schema Versioning

Machine-readable schemas require explicit versions.

Relevant schemas may include:

```text
Compliance Rule Schema
Compliance Profile Schema
Evidence Schema
Finding Schema
Compliance Result Schema
Report Schema
```

Schema versions must not be inferred solely from framework implementation versions.

---

# Release Candidate

Before an official framework release, a release candidate should be validated.

A release candidate represents the exact policy and implementation expected to become official.

Conceptually:

```text
Development
    │
    ▼
RC1
    │
    ├── Validation Failure ──► Fix
    │
    ▼
RC2
    │
    ▼
Approved Release
```

Multiple release candidates may be required.

---

# Release Candidate Freeze

During final validation, the release candidate should be sufficiently frozen to make evidence meaningful.

Changes to:

* rules;
* profiles;
* validators;
* schemas;
* gate policies;

should invalidate affected release validation and require appropriate revalidation.

---

# Release Candidate Validation

A framework release candidate should validate:

* documentation completeness;
* rule catalog integrity;
* profile integrity;
* validator tests;
* evidence behavior;
* finding behavior;
* report schemas;
* gate semantics;
* security boundaries;
* compatibility;
* migration documentation.

---

# Repository Quality Gates

Before release, the implementation must satisfy the active FamilyOS engineering quality requirements.

At minimum, where applicable:

```text
Ruff
MyPy
Pytest
```

must succeed according to repository policy.

Additional framework-specific checks may be required.

---

# Documentation Release Gate

The documentation release gate should verify:

* all required documents exist;
* no required document is empty;
* Markdown is structurally valid;
* terminology is consistent;
* internal references are valid;
* release metadata is current;
* revision history is updated;
* changelog is updated.

---

# Rule Catalog Release Gate

Before release, the Rule Catalog must satisfy:

* unique Rule IDs;
* valid domains;
* valid lifecycle states;
* known validators;
* valid evidence requirements;
* valid dependencies;
* valid ownership;
* valid severity;
* valid remediation;
* mandatory-rule integrity.

Invalid active rules must block release.

---

# Profile Release Gate

All active profiles must satisfy:

* valid identity;
* valid version;
* valid rule references;
* valid parent relationships;
* no inheritance cycles;
* mandatory-rule preservation;
* valid evidence policy;
* valid gate compatibility.

A broken profile invalidates the release candidate.

---

# Validator Release Gate

Authoritative validators should satisfy:

* contract tests;
* positive tests;
* negative tests;
* error-path tests;
* deterministic behavior;
* supported evidence production;
* documented ownership.

Security-sensitive validators may require additional review.

---

# Evidence Release Gate

The evidence subsystem should validate:

* serialization;
* provenance;
* freshness;
* trust semantics;
* scope;
* invalidation;
* conflict handling;
* redaction.

Evidence defects can invalidate compliance decisions and must therefore be treated seriously.

---

# Reporting Release Gate

Canonical Compliance Results must render consistently across supported output formats.

Release validation should compare:

```text
Text
JSON
CI
```

and any additional supported renderer.

All representations must preserve the same semantic result.

---

# Security Release Gate

Security validation should include tests for:

* policy tampering;
* profile tampering;
* validator replacement;
* evidence forgery;
* unauthorized exceptions;
* artifact mismatch;
* secret leakage;
* trust downgrade.

Critical unresolved trust-boundary defects must block framework release.

---

# Official Plugin Regression Gate

Before stable release, the framework should evaluate representative official plugins.

This detects unintended ecosystem impact.

A baseline may include:

```text
Security
Health
Finance
Education
Documents
Communication
```

The exact set may evolve with the official plugin ecosystem.

---

# Baseline Comparison

Release validation should compare current plugin results with the previous stable framework release where applicable.

The comparison should identify:

* new findings;
* resolved findings;
* status changes;
* severity changes;
* profile changes;
* evidence changes.

Unexpected regressions require investigation.

---

# Intended Compliance Changes

A new release may intentionally change plugin compliance status.

For example:

```text
Framework 1.4
Plugin A -> COMPLIANT

Framework 2.0
Plugin A -> NON_COMPLIANT
```

This is acceptable when caused by an intentional governed requirement change.

The change must be documented.

---

# Unintended Compliance Changes

Unexpected compliance changes may indicate:

* validator regression;
* profile error;
* evidence bug;
* rule ambiguity;
* compatibility defect.

These should block release until understood.

---

# Impact Analysis

Every release containing compliance-semantic changes should include impact analysis.

Impact analysis should identify:

* affected rules;
* affected profiles;
* affected plugin classifications;
* expected new findings;
* migration requirements;
* enforcement changes.

---

# Migration Requirement

A release introducing breaking compliance changes must provide migration guidance before enforcement.

Migration documentation should explain:

```text
What changed?
Why?
Who is affected?
What must be changed?
When does enforcement begin?
```

---

# Release Notes

Framework release notes should summarize changes relevant to plugin developers and governance consumers.

Important categories include:

```text
Added
Changed
Deprecated
Removed
Fixed
Security
Migration
```

Release notes should emphasize compliance-semantic changes.

---

# Changelog

`CHANGELOG.md` should maintain a durable history of framework evolution.

Every released version should record significant changes to:

* architecture;
* rules;
* profiles;
* validators;
* evidence;
* reporting;
* gates;
* governance;
* security.

---

# Revision History

`Revision-History.md` should document significant changes to the normative documentation set.

This is distinct from implementation commit history.

---

# Release Metadata

The framework should eventually maintain structured release metadata.

Potential fields include:

```text
framework_id
version
release_date
status
minimum_platform_version
rule_catalog_version
report_schema_version
```

Additional metadata may be introduced as implementation matures.

---

# Framework Release Artifact

A future framework release may produce a versioned artifact containing:

```text
Rules
Profiles
Schemas
Validator Metadata
Documentation References
Version Metadata
```

This can improve reproducibility across environments.

---

# Policy Bundle

A mature implementation may package compliance policy separately from engine code.

Conceptually:

```text
Compliance Engine
        +
Versioned Policy Bundle
        =
Executable Framework Release
```

The policy bundle must remain trusted and integrity-protected.

---

# Release Integrity

Framework release artifacts should eventually support integrity verification.

Potential mechanisms include:

* checksums;
* signatures;
* attestations.

The specific mechanism belongs to the broader FamilyOS release and security architecture.

---

# Release Approval

A stable framework release should require explicit approval according to FamilyOS governance.

Approval should consider:

* technical validation;
* architectural consistency;
* security;
* compatibility;
* migration impact;
* ecosystem readiness.

---

# Release Authority

The ability to publish an authoritative compliance framework release must be restricted to governed release mechanisms.

Individual plugins must not select arbitrary modified policy bundles and represent them as official FamilyOS compliance.

---

# Stable Release

A stable framework release is eligible for production compliance evaluation.

Stable status implies:

* documented semantics;
* validated implementation;
* governed policy;
* known compatibility;
* supported migration path.

Stable does not mean permanent.

---

# Preview Release

The framework may use preview releases for significant new capabilities.

Preview features may include:

* new domains;
* new validators;
* new evidence models;
* new profiles.

Preview policy should not silently become mandatory stable policy.

---

# Experimental Release

Experimental capabilities may be released for evaluation without production enforcement guarantees.

Experimental features should be clearly marked and excluded from strong lifecycle claims unless explicitly approved.

---

# Release Channels

A mature framework may distinguish:

```text
experimental
preview
stable
```

These channels describe framework maturity.

They must not be confused with plugin classification.

---

# Adoption After Release

Publishing a framework release does not necessarily activate all new rules immediately.

A rule may move through:

```text
Released
   │
   ▼
Shadow
   │
   ▼
Advisory
   │
   ▼
Blocking
```

This allows controlled adoption.

---

# Enforcement Date

When a release introduces future blocking requirements, the enforcement date should be explicit.

Developers should not discover a major new blocking policy only when a release gate suddenly fails.

---

# Grace Period

Non-critical breaking policy may receive a grace period.

The grace period should specify:

* affected rules;
* affected profiles;
* migration deadline;
* enforcement date.

Security-critical requirements may require immediate enforcement.

---

# Release Compatibility

Each stable framework release should document compatibility with relevant FamilyOS platform versions.

Conceptually:

```text
Framework 2.x
supports
FamilyOS Platform 5.x
```

Compatibility ranges must be explicit when technically relevant.

---

# Plugin Compatibility

Plugins should not normally declare arbitrary framework compatibility unless the platform architecture requires it.

The authoritative compatibility relationship should derive from:

* platform version;
* plugin contract version;
* framework policy;
* supported profiles.

---

# Tooling Compatibility

CLI and CI tooling must verify that they support the requested framework version.

Unsupported combinations should fail explicitly.

Silent interpretation of unknown policy is prohibited.

---

# Rollback

A framework release may require rollback if a severe defect is discovered.

Rollback must preserve historical identity.

For example:

```text
2.1.0 released
2.1.0 defect discovered
2.1.1 corrective release
```

The system should prefer corrective releases over rewriting already published versions.

---

# Published Release Immutability

Published framework releases should be treated as immutable.

If a released rule or validator is defective, FamilyOS should publish a corrected framework version.

Historical results must remain interpretable under the original release.

---

# Emergency Release

Critical security or integrity issues may require an emergency release.

Emergency releases still require:

* explicit version;
* documented reason;
* validation appropriate to the risk;
* changelog;
* affected-rule identification;
* revalidation guidance.

Urgency does not justify silent policy mutation.

---

# Security Advisory Integration

A security advisory may trigger:

```text
Security Advisory
       │
       ▼
Emergency Compliance Rule
       │
       ▼
Framework Release
       │
       ▼
Affected Plugin Revalidation
```

This provides a governed path for rapid ecosystem response.

---

# Revalidation After Release

A new framework release may trigger plugin revalidation.

The required scope depends on impact.

Possible scopes include:

```text
None
Affected Rules
Affected Domains
Affected Profiles
Affected Plugins
Entire Ecosystem
```

The framework should prefer the smallest safe revalidation scope.

---

# Release Drift

A framework release may intentionally create compliance drift.

Drift should be visible rather than treated as unexpected noise.

A release report may summarize:

```text
Previously Compliant: 6
Still Compliant: 5
Newly Non-Compliant: 1
Reason: New mandatory security rule
```

---

# Release and Certification

Certification systems must record the framework release used to establish compliance eligibility.

A certification process may require:

* minimum framework version;
* accepted profile version;
* current evidence;
* exact artifact binding.

Old compliance results may become insufficient for new certification decisions.

---

# Release and Build

The Build Framework may consume framework release identity when producing plugin artifacts.

A release-grade plugin artifact should eventually be traceable to:

```text
Source Revision
Build Identity
Plugin Artifact Digest
Compliance Framework Version
Compliance Result
```

---

# Release and CI

CI should use an explicitly resolved framework version.

Unexpected automatic upgrades can create non-reproducible compliance behavior.

Upgrade policy should be governed.

---

# Pinned Framework Versions

High-assurance workflows may pin framework versions.

For example:

```text
compliance-framework = 2.4.1
```

Pinning improves reproducibility.

Governance must still prevent indefinite use of obsolete policy.

---

# Minimum Supported Framework Version

Release or certification systems may define a minimum accepted framework version.

This allows FamilyOS to retire obsolete compliance policy safely.

---

# Release Validation Record

Each framework release should preserve a validation record containing enough evidence to demonstrate:

* repository quality checks passed;
* framework tests passed;
* policy validation passed;
* official plugin regression passed;
* security validation passed;
* release approval occurred.

---

# Release Failure

A release candidate must not become stable when critical validation fails.

Examples include:

```text
Duplicate active Rule ID
Profile cycle
Validator contract failure
Evidence integrity defect
Compliance status nondeterminism
Critical security failure
```

These are framework release blockers.

---

# Warning-Level Release Issues

Some non-critical issues may be accepted temporarily through governed release exceptions.

Examples might include:

* non-blocking documentation improvement;
* known performance limitation;
* experimental validator issue outside stable profiles.

Such exceptions must remain documented.

---

# Release Exception Governance

Framework release exceptions require:

* explicit issue;
* owner;
* rationale;
* scope;
* expiration or remediation target.

A release exception must not silently weaken plugin compliance policy.

---

# Release Checklist

Before a stable release, verify:

```text
[ ] Framework version defined
[ ] Release notes prepared
[ ] CHANGELOG updated
[ ] Revision history updated
[ ] Documentation complete
[ ] Rule catalog valid
[ ] Profiles valid
[ ] Validator tests pass
[ ] Evidence tests pass
[ ] Reporting tests pass
[ ] Gate tests pass
[ ] Security tests pass
[ ] Repository quality gates pass
[ ] Official plugin regression complete
[ ] Compatibility reviewed
[ ] Migration guidance prepared
[ ] Revalidation scope determined
[ ] Release approval recorded
```

This checklist may later become automated.

---

# Initial EPIC Release

The initial release of EPIC-PLUGIN-002 primarily establishes the normative framework definition.

Its initial release should communicate that:

```text
Architecture Defined
Policy Model Defined
Implementation Roadmap Defined
Operational Implementation May Continue
```

Documentation completion must not falsely imply that all advanced roadmap capabilities are already implemented.

---

# Initial Release Objective

The initial EPIC release should establish a stable architectural baseline from which implementation can begin.

Its primary outputs are:

* common vocabulary;
* architectural boundaries;
* compliance model;
* governance model;
* lifecycle model;
* implementation roadmap.

---

# Future Operational Release

A later operational release should indicate that executable compliance infrastructure is ready for normal FamilyOS engineering use.

Operational readiness requires the criteria defined in `20-Validation.md`.

---

# Release Maturity

The framework may progress through release maturity levels such as:

```text
Architecture Baseline
        │
        ▼
Developer Preview
        │
        ▼
Operational
        │
        ▼
Release-Enforced
        │
        ▼
Certification-Ready
        │
        ▼
Third-Party Ready
```

These maturity levels describe capability rather than semantic version numbers.

---

# Release Metrics

Useful release metrics may include:

* rule count;
* active rule count;
* profile count;
* validator count;
* test count;
* official plugin compliance rate;
* regression count;
* migration count;
* release exceptions;
* validation duration.

Metrics provide context.

They do not determine release readiness automatically.

---

# Release Auditability

A historical framework release should answer:

```text
What policy was active?
Which rules existed?
Which profiles existed?
Which validators were used?
Which schemas were current?
Which plugins were validated?
Which known limitations existed?
Who approved the release?
```

This auditability is essential for long-lived compliance and certification records.

---

# Release Anti-Patterns

The framework must avoid several release anti-patterns.

## Silent Policy Release

Do not introduce compliance-semantic changes without versioning.

## Mutable Published Release

Do not rewrite an already published framework version.

## Release Without Regression Testing

Do not publish broad policy changes without evaluating representative plugins.

## Release Without Migration

Do not introduce breaking requirements without remediation guidance.

## Automatic Uncontrolled Upgrade

Do not allow high-assurance workflows to change framework semantics unexpectedly.

## Documentation-Only Authority

Do not declare operational enforcement readiness solely because documentation is complete.

## Certification by Version

Do not assume that using a particular framework version automatically certifies a plugin.

---

# Release Invariants

The release model establishes the following invariants:

1. Every official framework release has an explicit version.
2. Compliance Results identify the framework release used.
3. Published framework releases are immutable.
4. Semantic changes are versioned.
5. Breaking changes require migration guidance.
6. Active policy must pass validation before release.
7. Stable profiles must pass profile validation.
8. Authoritative validators must be tested.
9. Critical trust failures block release.
10. Representative official plugins should be regression-tested.
11. Unexpected compliance drift must be investigated.
12. Intended compliance drift must be documented.
13. Release and certification remain separate.
14. Release candidates are validated before stable publication.
15. Emergency releases remain versioned and traceable.
16. Framework rollback does not rewrite history.
17. Machine-readable schemas have explicit versions.
18. Stable release does not imply permanent policy.
19. New blocking policy should be introduced predictably where practical.
20. Framework authority derives from governed release, not mere implementation existence.

---

# Reference Release Flow

The complete framework release flow is:

```text
Framework Changes
        │
        ▼
Documentation Validation
        │
        ▼
Policy Validation
        │
        ▼
Implementation Tests
        │
        ▼
Security Validation
        │
        ▼
Official Plugin Regression
        │
        ▼
Impact Analysis
        │
        ▼
Migration Review
        │
        ▼
Release Candidate
        │
        ▼
Release Approval
        │
        ▼
Stable Framework Release
        │
        ▼
Controlled Adoption
        │
        ▼
Revalidation / Enforcement
```

---

# Release Summary

The Plugin Compliance Framework release process ensures that compliance policy itself is released with the discipline expected from the plugins it governs.

The release model can be summarized as:

```text
Versioned Policy
      +
Validated Implementation
      +
Regression Evidence
      +
Compatibility Analysis
      +
Migration Guidance
      +
Governed Approval
      =
Trustworthy Framework Release
```

---

# Final Release Principle

The governing release principle of EPIC-PLUGIN-002 is:

> Compliance policy becomes authoritative only when its exact version, semantics, validation evidence, and lifecycle impact are known.

FamilyOS must therefore release the Plugin Compliance Framework as a governed and reproducible platform contract, preserving the ability to explain both present and historical plugin compliance decisions.
