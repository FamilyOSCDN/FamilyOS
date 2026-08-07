# Plugin Compliance Framework

# 07 Compliance Profiles

## Introduction

Compliance Profiles define how FamilyOS composes compliance rules for specific plugin contexts.

A compliance profile does not create new compliance requirements.

It selects, constrains, and interprets existing rules according to factors such as plugin classification, lifecycle stage, trust level, release context, and certification target.

Profiles therefore provide the bridge between the universal Rule Catalog and the specific validation expectations applied to an individual plugin.

The core relationship is:

```text
Rule Catalog
    │
    ▼
Compliance Profile
    │
    ▼
Applicable Rule Set
    │
    ▼
Plugin Evaluation
```

---

# Purpose

The purpose of Compliance Profiles is to allow FamilyOS to apply different validation depths without creating fragmented compliance definitions.

Profiles provide the foundation required to:

* select applicable rules;
* enforce mandatory rules;
* define severity thresholds;
* distinguish development from release validation;
* support plugin classification differences;
* support certification targets;
* define evidence expectations;
* govern profile evolution;
* preserve one authoritative rule catalog.

Profiles must remain deterministic and versioned.

---

# Profile Principle

The central principle is:

> Profiles select compliance requirements; they do not redefine them.

A rule must retain the same semantic meaning regardless of the profile in which it is evaluated.

For example:

```text
PLUGIN-ARCH-001
```

must represent the same architectural requirement in:

```text
development
official
third-party
certification
```

A profile may decide whether that rule applies or whether its failure is blocking.

It must not alter the requirement itself.

---

# Profile Model

A conceptual Compliance Profile contains:

```text
ComplianceProfile
├── id
├── version
├── title
├── description
├── plugin_classifications
├── lifecycle_stages
├── included_rules
├── excluded_rules
├── mandatory_rules
├── severity_policy
├── evidence_policy
├── exception_policy
├── certification_target
├── parent_profiles
└── lifecycle
```

The final schema may evolve, but these concepts define the intended semantic model.

---

# Profile Identity

Every published profile must have a stable identifier.

Conceptual examples include:

```text
development
built-in
official
third-party
release
certification
```

A more explicit future naming convention may use:

```text
PLUGIN-PROFILE-DEVELOPMENT
PLUGIN-PROFILE-OFFICIAL
PLUGIN-PROFILE-THIRD-PARTY
PLUGIN-PROFILE-CERTIFICATION
```

The exact naming format should be standardized before implementation.

---

# Profile Versioning

Profiles must be versioned independently from plugin implementations.

A profile version records the exact rule composition and decision policy applied during evaluation.

A compliance result should therefore identify:

```text
Profile ID
Profile Version
```

in addition to:

```text
Plugin Version
Platform Version
Compliance Framework Version
```

This enables reproducible historical evaluation.

---

# Profile Resolution

The framework must resolve the appropriate profile before rule evaluation begins.

Profile resolution may use:

* plugin classification;
* lifecycle stage;
* execution mode;
* release context;
* certification target;
* explicit engineering configuration.

Conceptually:

```text
Plugin
  │
  ▼
Classification
  │
  ▼
Validation Context
  │
  ▼
Profile Resolver
  │
  ▼
Resolved Profile
```

Profile resolution must never silently select a weaker profile because a stronger profile failed.

---

# Plugin Classification

Plugin classification is one of the primary inputs to profile selection.

Initial classifications may include:

```text
development
experimental
built-in
official
first-party
third-party
```

Classification identifies ecosystem responsibility and expected governance level.

Classification alone does not determine compliance.

It determines which profile family should normally apply.

---

# Development Profile

The Development Profile exists to provide fast, useful compliance feedback during active implementation.

Its objectives include:

* detecting fundamental structural errors;
* detecting invalid metadata;
* enforcing critical architecture boundaries;
* validating basic capability contracts;
* identifying dependency violations;
* exposing security-critical failures early.

The Development Profile should prioritize speed and developer feedback.

It should not necessarily require all release or governance evidence.

---

# Development Profile Characteristics

A conceptual Development Profile may require:

```text
Identity
Metadata
Structure
Architecture
Capabilities
Dependencies
Basic Testing
Critical Security
```

It may permit some rules to remain:

```text
NOT_EVALUATED
```

when those rules require evidence available only during later lifecycle stages.

However, mandatory platform safety requirements remain enforced.

---

# Experimental Profile

The Experimental Profile supports plugins that are intentionally unstable or exploratory.

Experimental status may relax:

* documentation completeness;
* compatibility guarantees;
* governance metadata;
* long-term lifecycle requirements.

It must not relax fundamental:

* identity integrity;
* runtime safety;
* critical security;
* prohibited dependency boundaries.

Experimental must mean unstable, not ungoverned.

---

# Built-In Plugin Profile

Built-in plugins are distributed as part of the FamilyOS platform.

They therefore require stronger validation than development plugins.

A Built-In Profile may require:

* complete metadata;
* valid architecture;
* capability contract compliance;
* contribution compliance;
* dependency compliance;
* configuration validation;
* security validation;
* testing;
* quality gates;
* documentation;
* compatibility;
* lifecycle validation.

Built-in origin does not exempt a plugin from compliance.

---

# Official Plugin Profile

The Official Plugin Profile represents a strong first-party compliance baseline.

Official plugins are expected to demonstrate platform-grade engineering maturity.

The profile should generally require all primary compliance domains:

```text
Identity
Metadata
Structure
Architecture
Capabilities
Contributions
Dependencies
Configuration
Security
Testing
Quality
Documentation
Compatibility
Lifecycle
Governance
```

Official plugin validation should produce sufficient evidence for release governance and future certification workflows.

---

# Third-Party Plugin Profile

The Third-Party Profile applies to externally developed plugins intended to participate in the FamilyOS ecosystem.

Its purpose is to protect platform integrity while allowing independent implementation.

A Third-Party Profile should enforce:

* public API boundaries;
* metadata completeness;
* dependency restrictions;
* capability contracts;
* contribution contracts;
* security requirements;
* compatibility declarations;
* lifecycle safety.

It should avoid requirements that unnecessarily depend on internal FamilyOS engineering processes.

---

# First-Party Extension Profile

FamilyOS may support first-party extensions that are maintained by the platform organization but are not distributed as core built-in plugins.

Such plugins may use a profile between Built-In and Official depending on governance needs.

The important architectural principle is that profile selection remains explicit rather than inferred from repository location.

---

# Release Profile

The Release Profile represents validation required before a plugin artifact can enter a release process.

It may extend another classification profile.

For example:

```text
Official Profile
      │
      ▼
Release Profile
```

The Release Profile may add requirements related to:

* complete test evidence;
* quality gates;
* documentation completeness;
* compatibility declarations;
* release metadata;
* version correctness;
* dependency locking;
* lifecycle verification.

---

# Certification Profile

The Certification Profile represents technical compliance expectations required before entering a certification process.

It should not perform certification itself.

The profile produces:

```text
Compliance Result
        │
        ▼
Certification Eligibility
```

Certification may still require additional governance steps outside the compliance framework.

---

# Profile Composition

Profiles should support composition.

A conceptual model is:

```text
Base Profile
    │
    ▼
Official Profile
    │
    ▼
Release Profile
    │
    ▼
Certification Profile
```

Composition allows stronger profiles to extend existing requirements without duplicating the entire rule set.

---

# Profile Inheritance

Where profile inheritance is supported, it must remain simple and deterministic.

A child profile may:

* include additional rules;
* strengthen severity thresholds;
* require additional evidence;
* restrict exceptions;
* activate additional domains.

A child profile should not silently weaken mandatory requirements inherited from its parent.

---

# Multiple Inheritance

Complex multiple profile inheritance should be avoided unless there is a strong architectural need.

Multiple inheritance can introduce ambiguous rule resolution.

Prefer explicit composition where possible.

For example:

```text
Official Base
    +
Release Requirements
    +
Certification Requirements
```

is easier to reason about than an uncontrolled inheritance graph.

---

# Rule Inclusion

Profiles define which rules are included.

Conceptually:

```text
included_rules:
  - PLUGIN-ID-001
  - PLUGIN-META-001
  - PLUGIN-ARCH-001
  - PLUGIN-TEST-001
```

Profiles may also include rule groups or domains where appropriate.

However, expanded rule membership must remain inspectable.

---

# Rule Exclusion

Profiles may explicitly exclude rules that are not applicable to the profile context.

Exclusion must not be used to bypass mandatory requirements.

A profile exclusion should identify why a valid rule is not part of the current compliance target.

---

# Mandatory Rule Enforcement

Mandatory rules apply regardless of ordinary profile composition.

Conceptually:

```text
Selected Profile
      +
Mandatory Rules
      =
Effective Rule Set
```

This protects foundational safety and architecture constraints.

---

# Effective Rule Set

The effective rule set is the final collection of rules evaluated for a plugin.

It is derived from:

```text
Profile Rules
      +
Inherited Rules
      +
Mandatory Rules
      -
Valid Exclusions
      =
Effective Rule Set
```

This rule set must be visible in structured compliance output.

---

# Severity Policy

Profiles may define how severity affects final compliance status.

For example, a Development Profile may permit:

```text
WARNING
```

without failing validation.

A Release Profile may treat the same warning as release-blocking if policy requires it.

The underlying rule severity remains unchanged.

The profile defines decision thresholds.

---

# Severity Threshold Example

Conceptually:

```text
Development Profile
  CRITICAL -> Block
  ERROR    -> Block
  WARNING  -> Report
  INFO     -> Report

Certification Profile
  CRITICAL -> Block
  ERROR    -> Block
  WARNING  -> Policy Dependent
  INFO     -> Report
```

The exact behavior must be standardized in compliance policy.

---

# Evidence Policy

Profiles may define evidence strength requirements.

For example:

```text
Development
  local test evidence acceptable

Release
  CI-produced evidence required

Certification
  trusted release evidence required
```

This allows stronger lifecycle contexts to require stronger provenance without redefining individual compliance rules.

---

# Evidence Completeness

A profile may define whether all applicable rules must have complete evidence.

For example:

```text
Development
  some non-critical rules may remain NOT_EVALUATED

Release
  blocking rules must be fully evaluated

Certification
  all certification-required rules must have accepted evidence
```

Incomplete evidence must remain visible.

---

# Evidence Freshness Policy

Profiles may define acceptable evidence freshness.

For example:

```text
Development
  current working tree

CI
  current commit

Release
  release candidate commit

Certification
  final release artifact
```

Evidence generated for a different source state should not satisfy stronger profile requirements automatically.

---

# Exception Policy

Profiles may restrict or prohibit exceptions.

For example:

```text
Development
  governed exceptions allowed

Official Release
  limited exceptions

Certification
  only explicitly approved exceptions
```

Profile policy must never override a rule whose exception policy is:

```text
NONE
```

---

# Suppression Policy

Profiles may also define whether suppressed findings affect compliance.

A development workflow may permit temporary suppressions.

A certification workflow may require all suppressions to be reviewed or removed.

Suppression always remains visible in the compliance result.

---

# Lifecycle-Aware Profiles

Profiles may correspond to lifecycle stages.

Conceptually:

```text
Development Profile
      │
      ▼
CI Profile
      │
      ▼
Release Profile
      │
      ▼
Certification Profile
```

This progression allows validation depth to increase as the plugin approaches distribution or certification.

---

# Validation Modes

Profiles may also influence execution mode.

Possible modes include:

```text
fast
standard
full
certification
```

Execution mode may affect:

* validator selection;
* expensive checks;
* evidence reuse;
* lifecycle tests.

Execution optimization must never change compliance meaning for the same effective profile.

---

# Fast Profile Checks

Fast validation should prioritize low-cost checks such as:

* metadata;
* structure;
* imports;
* dependency declarations;
* basic capability schemas.

Fast checks are useful during active development.

They should not be presented as full compliance validation unless the profile explicitly defines them as sufficient.

---

# Full Profile Checks

Full validation may include:

* complete test execution;
* quality validation;
* lifecycle tests;
* security analysis;
* compatibility verification;
* documentation validation.

Full profile checks are suitable for CI, release, or certification contexts.

---

# Profile and Domain Mapping

Profiles may activate different compliance domains.

Conceptually:

```text
Development
├── Identity
├── Metadata
├── Structure
├── Architecture
├── Capabilities
└── Dependencies

Official
├── Identity
├── Metadata
├── Structure
├── Architecture
├── Capabilities
├── Contributions
├── Dependencies
├── Configuration
├── Security
├── Testing
├── Quality
├── Documentation
├── Compatibility
├── Lifecycle
└── Governance
```

This mapping is illustrative.

The authoritative mapping must be defined in profile configuration.

---

# Profile Applicability

A profile itself may define applicability.

For example:

```text
official
```

may apply only when:

```text
plugin.classification == official
```

A profile requested outside its permitted context should produce an explicit validation error unless governance allows the override.

---

# Explicit Profile Override

Engineering tooling may allow explicit profile selection.

For example:

```text
familyos plugin compliance check --profile official
```

An explicit override must remain visible in the Compliance Result.

Tooling must not silently select a different profile than requested.

---

# Profile Escalation

The system may allow a stronger profile to be selected than required.

For example, a development plugin may voluntarily run the Official Profile.

This can provide early feedback.

The reverse should not occur automatically.

A plugin requiring the Official Profile must not silently fall back to Development Profile validation.

---

# Profile Resolution Failure

If no valid profile can be resolved, validation must stop with an explicit error.

The framework must not assume compliance under a default weak profile.

Conceptually:

```text
Unknown Classification
        │
        ▼
Profile Resolution Failure
        │
        ▼
Validation Error
```

---

# Profile Reporting

Every compliance report must identify the active profile.

Human-readable output should make this clear:

```text
Profile: official
Profile Version: 1.0.0
```

Without profile context, a compliance status is ambiguous.

---

# Comparing Results Across Profiles

Compliance results produced using different profiles are not directly equivalent.

For example:

```text
COMPLIANT under development
```

does not imply:

```text
COMPLIANT under certification
```

Reports and tooling must preserve this distinction.

---

# Profile Promotion

A plugin may progress through stronger profiles.

Conceptually:

```text
Development
    │
    ▼
Built-In / Official
    │
    ▼
Release
    │
    ▼
Certification
```

Each stage requires successful evaluation against the corresponding profile.

---

# Profile Downgrade

A profile downgrade must be explicit and governed.

It should never happen automatically because stronger validation failed.

For example:

```text
Certification Profile Fails
```

must not become:

```text
Official Profile Passes
```

and then be presented as certification-ready.

Profile context must remain transparent.

---

# Certification Eligibility

A profile may define criteria for deriving certification eligibility.

Conceptually:

```text
Certification Profile
        │
        ▼
Effective Rule Set
        │
        ▼
Compliance Result
        │
   ┌────┴────┐
   ▼         ▼
Eligible   Not Eligible
```

Eligibility is still distinct from certification.

---

# Profile Governance

Compliance profiles are governed artifacts.

Changes require review because they can materially change compliance expectations.

Governance must cover:

* profile creation;
* rule inclusion;
* rule exclusion;
* inheritance;
* severity thresholds;
* evidence requirements;
* exception policy;
* deprecation;
* migration.

---

# Profile Change Impact

A profile change can make previously compliant plugins non-compliant.

Therefore, changes must be evaluated for ecosystem impact.

Examples include:

* adding a new mandatory rule;
* promoting a warning to a blocker;
* requiring stronger evidence;
* removing an exception path;
* activating a new compliance domain.

Breaking changes require migration guidance.

---

# Profile Lifecycle

Profiles should have explicit lifecycle states.

A conceptual lifecycle is:

```text
DRAFT
  │
  ▼
ACTIVE
  │
  ▼
DEPRECATED
  │
  ▼
RETIRED
```

Draft profiles must not silently affect stable validation.

---

# Profile Deprecation

Deprecated profiles should identify:

* replacement profile;
* deprecation version;
* reason;
* migration guidance;
* retirement plan.

Historical compliance results must remain interpretable.

---

# Profile Registry

The framework should maintain an authoritative profile registry.

Conceptually:

```text
ProfileRegistry
├── development
├── experimental
├── built-in
├── official
├── third-party
├── release
└── certification
```

Consumers must resolve profiles through this registry or equivalent governed mechanism.

---

# Profile Discovery

Developer tooling should make profiles discoverable.

Future CLI concepts may include:

```text
familyos plugin compliance profiles
```

and:

```text
familyos plugin compliance profile show official
```

Profile discovery improves transparency and reduces hidden compliance expectations.

---

# Profile Explanation

Tooling should be capable of explaining why a rule is active under a profile.

For example:

```text
PLUGIN-SEC-004

Included because:
  profile = official
  domain = security
  mandatory = true
```

This improves debugging and compliance understanding.

---

# Profile Difference Analysis

The framework may eventually support profile comparison.

For example:

```text
development -> official
```

could show newly required rules.

Conceptually:

```text
Added Rules: 42
Additional Domains: Security, Quality, Governance
Stronger Evidence: CI required
Additional Blocking Warnings: 3
```

This would help developers prepare plugins for promotion.

---

# Profile Composition Example

A conceptual model may be:

```text
BASE
├── Identity
├── Metadata
├── Structure
└── Critical Security

DEVELOPMENT
└── BASE
    + Architecture
    + Capabilities
    + Dependencies

OFFICIAL
└── DEVELOPMENT
    + Contributions
    + Configuration
    + Testing
    + Quality
    + Documentation
    + Compatibility
    + Lifecycle
    + Governance

RELEASE
└── OFFICIAL
    + Release Evidence Policy

CERTIFICATION
└── RELEASE
    + Certification Evidence Policy
    + Restricted Exceptions
```

This model is illustrative, not yet a final implementation contract.

---

# Profile Anti-Patterns

The framework must avoid several profile anti-patterns.

## Rule Duplication

Do not copy rule definitions into multiple profiles.

## Semantic Mutation

Do not change rule meaning based on profile.

## Hidden Downgrade

Do not silently switch to a weaker profile.

## Unbounded Inheritance

Do not create complex inheritance graphs that make applicability impossible to understand.

## Security Weakening

Do not allow ordinary profiles to disable mandatory security rules.

## Ambiguous Evidence

Do not accept weaker evidence without explicit profile policy.

---

# Profile Invariants

The Compliance Profile model establishes the following invariants:

1. Profiles select rules; they do not redefine them.
2. Every profile has a stable identity.
3. Every active profile is versioned.
4. Profile resolution is deterministic.
5. Mandatory rules cannot be removed through ordinary profile configuration.
6. Stronger profiles may add requirements but must not silently weaken inherited ones.
7. Profile downgrades are explicit.
8. Evidence requirements may become stronger across lifecycle stages.
9. Exceptions remain governed.
10. Compliance status is always interpreted in profile context.
11. Different profiles produce different assurance levels.
12. Certification profiles determine eligibility, not certification itself.
13. Profiles are governed and traceable.
14. Deprecated profiles remain historically interpretable.
15. Tooling must expose the active profile clearly.

---

# Profile Summary

The FamilyOS compliance profile model can be summarized as:

```text
Rule Catalog
     │
     ▼
Base Requirements
     │
     ▼
Classification Profile
     │
     ▼
Lifecycle Profile
     │
     ▼
Evidence Policy
     │
     ▼
Effective Rule Set
     │
     ▼
Compliance Evaluation
```

Profiles allow FamilyOS to support progressive assurance while preserving one authoritative compliance language.

---

# Final Profile Principle

The governing principle of Compliance Profiles is:

> Different plugin contexts may require different levels of assurance, but they must all derive from the same governed compliance rules.

This ensures that FamilyOS can support development flexibility, official plugin rigor, third-party extensibility, release governance, and certification readiness without fragmenting the meaning of plugin compliance.
