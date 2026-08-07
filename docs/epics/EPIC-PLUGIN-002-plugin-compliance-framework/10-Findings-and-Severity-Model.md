# Plugin Compliance Framework

# 10 Findings and Severity Model

## Introduction

The Findings and Severity Model defines how FamilyOS represents compliance problems, validation uncertainty, infrastructure failures, and remediation guidance.

A compliance finding is not the same as a rule.

A rule defines a requirement.

A finding records a concrete condition discovered during a specific evaluation.

The model must preserve a strict separation between:

* rule outcome;
* finding;
* severity;
* exception state;
* suppression state;
* overall compliance status.

This separation is essential for deterministic compliance decisions and clear reporting.

---

# Purpose

The Findings and Severity Model provides a normalized representation for compliance conditions discovered during validation.

It enables FamilyOS to:

* communicate rule violations clearly;
* distinguish technical failures from compliance failures;
* preserve finding identity;
* support remediation;
* support suppressions and exceptions;
* apply consistent severity semantics;
* derive compliance status predictably;
* support machine-readable reporting;
* support audit and certification workflows.

Findings must remain understandable to both humans and automated consumers.

---

# Finding Principle

The governing principle is:

> A finding describes an observed compliance condition; it does not independently determine overall compliance.

Overall compliance is derived later through policy.

A finding records what happened.

Policy determines the consequence.

---

# Finding Definition

A Compliance Finding represents one identified compliance-relevant condition associated with an evaluation.

A conceptual model is:

```text
ComplianceFinding
├── id
├── evaluation_id
├── rule_id
├── domain
├── severity
├── category
├── status
├── title
├── message
├── evidence_refs
├── location
├── remediation
├── suppression
├── exception
├── created_at
└── metadata
```

The exact schema may evolve.

The semantic separation must remain stable.

---

# Finding Identity

Every finding should have a unique identifier.

A Finding ID identifies one occurrence of a condition during one evaluation.

For example:

```text
Rule: PLUGIN-ARCH-001
Evaluation A -> Finding F-001
Evaluation B -> no finding
Evaluation C -> Finding F-019
```

The rule identity remains stable.

The finding identity is evaluation-specific.

---

# Finding and Rule Relationship

The canonical relationship is:

```text
Compliance Rule
      │
      ▼
Rule Evaluation
      │
   ┌──┴──┐
   ▼     ▼
 PASS   FAIL
          │
          ▼
       Finding
```

Not every finding must represent a direct rule violation.

The framework may also produce findings for:

* missing evidence;
* validation errors;
* expired exceptions;
* unsupported validation conditions.

However, every compliance finding must have a clear origin.

---

# Finding Categories

Findings should be categorized according to their meaning.

A conceptual baseline includes:

```text
VIOLATION
INCOMPLETE
VALIDATION_ERROR
GOVERNANCE
ADVISORY
```

The exact vocabulary should remain compact and globally consistent.

---

# Violation Findings

A VIOLATION finding represents evidence that an applicable compliance requirement was not satisfied.

Examples include:

* prohibited dependency detected;
* required metadata missing;
* capability contract violated;
* mandatory documentation absent;
* security boundary violated.

Violation findings normally originate from a rule outcome of:

```text
FAIL
```

---

# Incomplete Findings

An INCOMPLETE finding represents a requirement that could not be fully evaluated.

Possible causes include:

* missing required evidence;
* required manual review not completed;
* unavailable validator;
* unsupported execution environment.

Incomplete findings must remain distinct from violations.

They indicate insufficient assurance rather than demonstrated non-conformance.

---

# Validation Error Findings

A VALIDATION_ERROR finding represents a problem in the compliance infrastructure or validation execution.

Examples include:

* validator crash;
* malformed evidence;
* rule graph failure;
* unsupported validator implementation;
* evidence adapter error.

These findings do not directly prove plugin non-compliance.

They indicate that the framework could not complete reliable validation.

---

# Governance Findings

A GOVERNANCE finding represents a governance-related compliance condition.

Examples may include:

* expired exception;
* missing owner;
* invalid approval;
* unsupported certification authority;
* deprecated profile usage.

Governance findings may affect compliance or certification eligibility depending on profile policy.

---

# Advisory Findings

An ADVISORY finding communicates useful non-blocking information.

Examples include:

* recommended migration;
* deprecated API usage;
* upcoming rule activation;
* non-critical documentation improvement.

Advisory findings should not be confused with rule failures unless policy explicitly models them as such.

---

# Severity Model

Severity expresses the importance of a finding.

The baseline severity model is:

```text
INFO
WARNING
ERROR
CRITICAL
```

Severity is independent from finding category.

For example:

```text
category = VIOLATION
severity = WARNING
```

and:

```text
category = VIOLATION
severity = CRITICAL
```

represent different levels of consequence.

---

# INFO

INFO represents informational compliance feedback.

Typical uses include:

* successful migration hints;
* deprecation notices;
* low-risk observations;
* diagnostic context.

INFO findings should not normally block compliance.

---

# WARNING

WARNING represents a condition requiring attention but not necessarily immediate compliance failure under every profile.

Examples may include:

* deprecated supported API usage;
* incomplete recommended documentation;
* non-critical maintainability concern.

Profiles may decide whether warnings affect release or certification eligibility.

---

# ERROR

ERROR represents a material compliance violation.

Examples include:

* required metadata missing;
* invalid capability contract;
* required tests failing;
* unsupported dependency;
* mandatory documentation missing.

ERROR findings normally prevent compliant status when the rule is blocking.

---

# CRITICAL

CRITICAL represents a severe compliance condition affecting platform safety, security, trust, or foundational architecture.

Examples may include:

* prohibited privileged access;
* bypass of security controls;
* execution of unsupported internal runtime behavior;
* critical manifest integrity violation;
* tampering with compliance mechanisms.

CRITICAL findings should normally block:

* compliance;
* release;
* certification.

Exceptions should be highly restricted or forbidden.

---

# Severity Is Not Status

Severity and rule outcome must remain separate.

For example:

```text
Rule Outcome: FAIL
Severity: WARNING
```

means the requirement failed but policy considers the issue less severe.

Likewise:

```text
Rule Outcome: FAIL
Severity: CRITICAL
```

means the same basic failure state with significantly stronger impact.

This separation prevents ambiguous rule semantics.

---

# Rule Outcome Model

The canonical rule outcome model is:

```text
PASS
FAIL
NOT_APPLICABLE
NOT_EVALUATED
ERROR
```

These statuses describe evaluation state.

They do not describe importance.

Severity describes importance.

---

# Finding Status

Findings may have their own lifecycle status.

A conceptual model may include:

```text
OPEN
ACKNOWLEDGED
SUPPRESSED
EXCEPTED
RESOLVED
```

Finding status describes how the finding is being handled.

It must not rewrite the original rule outcome.

---

# Open Findings

OPEN means the finding remains active and unresolved.

It should participate normally in compliance decision policy.

---

# Acknowledged Findings

ACKNOWLEDGED means the finding has been reviewed or accepted for follow-up.

Acknowledgement does not mean compliance.

It simply records that the issue is known.

---

# Suppressed Findings

SUPPRESSED means the finding remains valid but its workflow or presentation has been modified through an approved suppression mechanism.

The finding remains traceable.

The underlying rule outcome remains unchanged.

---

# Excepted Findings

EXCEPTED means an approved exception affects how the failed requirement influences compliance policy.

The finding remains visible.

The original evidence remains unchanged.

An exception does not transform:

```text
FAIL
```

into:

```text
PASS
```

---

# Resolved Findings

RESOLVED means the underlying condition has been corrected in a later evaluation or explicitly closed according to governance policy.

Historical findings must remain attached to their original evaluation.

They must not be deleted.

---

# Finding Lifecycle

A conceptual finding lifecycle is:

```text
OPEN
 │
 ├──► ACKNOWLEDGED
 │
 ├──► SUPPRESSED
 │
 ├──► EXCEPTED
 │
 └──► RESOLVED
```

Not every transition is valid for every finding category or severity.

Governance determines allowed transitions.

---

# Finding Title

Every finding should provide a concise title.

Example:

```text
Unsupported internal runtime import detected
```

The title should be understandable without reading raw evidence.

---

# Finding Message

The finding message explains the detected condition.

It should answer:

* what happened;
* which requirement is affected;
* why the condition matters;
* what evidence supports the finding.

Messages should avoid unnecessary implementation detail when remediation guidance can provide it separately.

---

# Finding Location

Where possible, findings should identify the affected location.

Examples include:

```text
src/plugin/capabilities/foo.py:42
```

```text
plugin.yaml:dependencies
```

```text
docs/README.md
```

```text
capability: communication.send
```

Location information improves developer feedback.

---

# Location Model

A structured location may include:

```text
FindingLocation
├── path
├── line
├── column
├── symbol
├── section
└── logical_resource
```

Not every finding requires filesystem location.

Logical locations are equally valid.

---

# Evidence References

Findings should reference the evidence supporting them.

Conceptually:

```text
Finding
├── Evidence A
├── Evidence B
└── Evidence C
```

A developer or reviewer should be able to move from finding to evidence.

This preserves explainability.

---

# Remediation

Every actionable violation should include remediation guidance.

Remediation should explain how to correct the condition.

A good remediation answer should indicate:

* what to change;
* where to change it;
* which supported mechanism to use;
* which documentation or rule reference applies.

---

# Remediation Example

Weak remediation:

```text
Fix dependency.
```

Preferred remediation:

```text
Replace the import from familyos.runtime.internal.loader with the public loader interface exposed by the FamilyOS Plugin SDK.
```

Actionable remediation is a core developer-experience requirement.

---

# Remediation References

Findings may reference:

* rule documentation;
* migration guides;
* architecture documentation;
* examples;
* RFCs;
* ADRs;
* plugin SDK reference.

These references should complement remediation rather than replace it.

---

# Remediation Confidence

Some remediation can be deterministic.

Other remediation may require judgment.

The framework should avoid presenting speculative remediation as guaranteed correction.

Where appropriate, tooling may distinguish:

```text
recommended remediation
```

from:

```text
required remediation
```

---

# Suppression Model

A suppression changes how a known finding is handled without invalidating the finding.

A conceptual model is:

```text
FindingSuppression
├── id
├── finding_id
├── rule_id
├── justification
├── scope
├── authority
├── created_at
├── expires_at
└── status
```

Suppressions must always be explicit and traceable.

---

# Suppression Scope

A suppression may apply to:

* one finding;
* one file;
* one plugin version;
* one rule within a plugin;
* one evaluation context.

Broad suppressions should require stronger governance.

Global wildcard suppression should be avoided.

---

# Suppression Expiration

Suppressions should support expiration.

A temporary suppression without expiration risks becoming permanent technical debt.

Expired suppressions must no longer influence current compliance behavior.

---

# Suppression Authority

Profiles or governance policy may define who can create a valid suppression.

Examples include:

* plugin maintainer;
* architecture authority;
* security authority;
* release authority.

Security-sensitive findings may prohibit ordinary suppressions entirely.

---

# Exception Model

An exception differs from a suppression.

A suppression manages a finding.

An exception modifies the policy treatment of a requirement.

Conceptually:

```text
Rule Failure
    │
    ▼
Finding
    │
    ├── Suppression -> visibility/workflow adjustment
    │
    └── Exception   -> policy impact adjustment
```

The distinction must remain strict.

---

# Exception Structure

A conceptual exception contains:

```text
ComplianceException
├── id
├── rule_id
├── plugin_scope
├── justification
├── authority
├── created_at
├── expires_at
├── conditions
└── status
```

Exceptions must be independently auditable.

---

# Exception Eligibility

Rules should define whether exceptions are allowed.

Possible policy values include:

```text
NONE
GOVERNED
TEMPORARY
PROFILE_SPECIFIC
```

A CRITICAL security rule may define:

```text
NONE
```

and therefore remain non-exemptible.

---

# Exception Expiration

Exceptions should normally be time-bound when they exist to support migration or temporary compatibility.

Expired exceptions must not continue affecting compliance decisions.

The framework should generate a governance finding when an exception expires.

---

# Exception Conditions

Exceptions may include explicit conditions.

Example:

```text
Valid only for plugin version 2.x
```

or:

```text
Valid until migration to public capability API is complete
```

Conditions must be machine-readable where practical.

---

# Severity and Profile Policy

Severity meaning is global.

Decision impact is profile-specific.

For example:

```text
WARNING
```

may be non-blocking under:

```text
development
```

but require review under:

```text
certification
```

The profile may strengthen decision thresholds.

It must not rewrite the finding severity itself.

---

# Blocking Semantics

Profiles must define which findings are blocking.

A conceptual baseline may be:

```text
INFO      -> non-blocking
WARNING   -> profile-dependent
ERROR     -> blocking
CRITICAL  -> always blocking
```

This is illustrative.

The authoritative behavior belongs to Compliance Policy.

---

# Mandatory Rule Findings

A finding associated with a mandatory rule requires stronger treatment.

Conceptually:

```text
Mandatory Rule
      │
      ▼
FAIL
      │
      ▼
Finding
      │
      ▼
Blocking Decision
```

Ordinary profile configuration must not disable the effect of mandatory rules.

---

# Finding Aggregation

The framework may summarize findings by:

* severity;
* domain;
* rule;
* category;
* plugin component.

For example:

```text
Critical: 0
Errors: 3
Warnings: 7
Info: 4
```

Summaries are useful.

They must never replace individual findings.

---

# Domain Aggregation

Reports may summarize findings by domain:

```text
Architecture
  ERROR: 2

Security
  CRITICAL: 0
  ERROR: 1

Documentation
  WARNING: 4
```

This helps identify areas requiring remediation.

---

# Duplicate Findings

The framework should avoid unnecessary duplicate findings.

If one underlying condition violates several rules, each rule outcome must remain explicit.

However, reporting may group related findings.

Grouping must not hide the affected rules.

---

# Cascading Findings

Prerequisite failures can cause misleading cascades.

Example:

```text
Metadata invalid
    │
    ▼
Capability cannot be resolved
    │
    ▼
Contribution cannot be resolved
```

The framework should prefer:

```text
Metadata rule -> FAIL
Dependent rules -> NOT_EVALUATED
```

rather than generating many duplicate violation findings.

---

# Finding Fingerprints

The framework may support stable finding fingerprints for comparison across evaluations.

A fingerprint may derive from:

* rule ID;
* plugin;
* logical location;
* normalized condition.

This can help identify recurring findings.

A fingerprint must not replace Finding ID.

---

# Finding Comparison

Future tooling may classify findings between evaluations as:

```text
NEW
UNCHANGED
RESOLVED
REGRESSED
```

This supports developer workflows and compliance drift analysis.

Historical results must remain immutable.

---

# Finding Ordering

Finding presentation should be deterministic.

A preferred ordering may use:

```text
Severity
Domain
Rule ID
Location
Finding ID
```

For user-facing output, critical findings should normally appear before lower-severity findings.

The canonical structured result may preserve its own stable sort order.

---

# Severity Ordering

The framework defines severity ordering as:

```text
CRITICAL
   >
ERROR
   >
WARNING
   >
INFO
```

This ordering supports aggregation and presentation.

It must not be confused with overall compliance status precedence.

---

# Compliance Status and Severity

Overall compliance status is not simply the highest finding severity.

It is derived from:

```text
Rule Outcomes
+
Profile Policy
+
Mandatory Rules
+
Exceptions
+
Evidence Completeness
+
Validation Errors
=
Compliance Status
```

This is essential.

A plugin with no violation findings may still be:

```text
INCOMPLETE
```

because required evidence is missing.

---

# Compliance Status Model

The baseline overall states remain:

```text
COMPLIANT
NON_COMPLIANT
INCOMPLETE
ERROR
```

These statuses summarize the complete evaluation.

They are not finding severities.

---

# Non-Compliant Status

NON_COMPLIANT means that one or more applicable blocking requirements were demonstrated to be violated.

Typical causes include:

* blocking ERROR findings;
* CRITICAL findings;
* failed mandatory rules.

---

# Incomplete Status

INCOMPLETE means that required assurance could not be obtained.

Typical causes include:

* missing required evidence;
* required manual review pending;
* skipped required validator;
* unsupported required validation.

Incomplete is not equivalent to compliant.

---

# Error Status

ERROR means the framework could not produce a reliable compliance decision due to validation infrastructure failure.

Examples include:

* invalid rule graph;
* compliance engine failure;
* critical validator infrastructure failure.

This status must remain distinguishable from plugin failure.

---

# Finding and Status Example

Example:

```text
Rule: PLUGIN-DOC-004
Outcome: FAIL
Severity: WARNING
Finding: Documentation compatibility section missing
```

Under Development Profile:

```text
Overall Status: COMPLIANT
Warning reported
```

Under a stricter Certification Profile:

```text
Overall Status: NON_COMPLIANT
```

The rule and severity remain the same.

Only policy differs.

---

# Critical Finding Example

Example:

```text
Rule: PLUGIN-SEC-009
Outcome: FAIL
Severity: CRITICAL
Finding: Plugin bypasses authorization boundary
```

Typical effect:

```text
NON_COMPLIANT
Release blocked
Certification ineligible
```

This remains true even if all other rules pass.

---

# Validation Error Example

Example:

```text
Rule: PLUGIN-TEST-010
Outcome: ERROR
Finding Category: VALIDATION_ERROR
Severity: ERROR
Message: Test evidence adapter failed to parse required report
```

The correct result may be:

```text
ERROR
```

or:

```text
INCOMPLETE
```

depending on policy.

It must not become:

```text
NON_COMPLIANT
```

unless actual evidence demonstrates a plugin violation.

---

# Finding Serialization

Findings must be serializable.

Structured findings support:

* CLI;
* CI;
* JSON reports;
* dashboards;
* certification systems;
* historical analysis.

The canonical representation should preserve all semantic fields even when a human report shows only a subset.

---

# Human-Readable Findings

Human-facing output should prioritize:

* severity;
* title;
* rule ID;
* location;
* explanation;
* remediation.

Example:

```text
ERROR  PLUGIN-ARCH-001

Unsupported internal runtime import detected.

Location:
src/my_plugin/service.py:18

Remediation:
Use the public Plugin SDK runtime interface.
```

Raw validator diagnostics may be available separately.

---

# Machine-Readable Findings

Machine-readable output should preserve fields such as:

```text
id
rule_id
domain
severity
category
status
evidence_refs
location
suppression
exception
```

This allows downstream systems to make deterministic decisions.

---

# Exit Code Mapping

CLI and CI tooling may map compliance results to exit codes.

They should map overall status rather than individual severity counts.

For example:

```text
COMPLIANT      -> success
NON_COMPLIANT  -> compliance failure
INCOMPLETE     -> incomplete validation failure
ERROR          -> infrastructure failure
```

Exact numerical codes belong to CLI specifications.

---

# Finding Auditability

Every finding must remain auditable.

A reviewer should be able to determine:

* which evaluation created it;
* which rule produced it;
* which evidence supports it;
* what severity applied;
* whether suppression existed;
* whether exception existed;
* how it influenced the final result.

---

# Finding Immutability

Findings belonging to finalized evaluations should be immutable.

A later correction creates a new evaluation.

For example:

```text
Evaluation A
  Finding F-001 OPEN

Plugin corrected

Evaluation B
  PLUGIN-ARCH-001 PASS
```

Finding F-001 remains part of Evaluation A.

---

# Resolution Tracking

A separate historical comparison layer may later indicate that F-001 was resolved by Evaluation B.

This must not modify Evaluation A.

This preserves audit integrity.

---

# Severity Governance

Severity assignment is a compliance policy decision.

Individual validator implementations must not arbitrarily assign severity.

Validators provide observations.

Rules define severity.

Governance reviews severity changes.

---

# Severity Change Impact

Changing rule severity can materially affect compliance.

For example:

```text
WARNING -> ERROR
```

may cause previously compliant plugins to fail stronger profiles.

Severity changes therefore require impact analysis and version-aware governance.

---

# Severity Downgrades

Lowering severity also requires governance.

A severity downgrade can weaken platform enforcement.

Security-critical or mandatory rules should require elevated review before downgrade.

---

# Finding Governance

Governance must define:

* finding categories;
* finding lifecycle;
* suppression authority;
* exception authority;
* severity semantics;
* retention;
* report visibility;
* certification handling.

These policies must be consistent across tools.

---

# Finding Testing

The Findings and Severity Model requires dedicated tests.

Core test areas include:

* finding creation;
* finding identity;
* severity ordering;
* category mapping;
* suppression handling;
* exception handling;
* expiration;
* serialization;
* deterministic ordering;
* compliance-status derivation;
* validation error distinction.

---

# Anti-Patterns

The framework must avoid several anti-patterns.

## Severity as Outcome

Do not use `ERROR` both as rule outcome and severity without explicit semantic distinction.

## Silent Suppression

Do not hide findings without traceable suppression metadata.

## Exception as Pass

Do not convert excepted failures into ordinary PASS results.

## Missing Evidence as Success

Do not treat absent findings as proof of compliance.

## Validator Crash as Violation

Do not report infrastructure failure as plugin non-compliance.

## Score-Only Reporting

Do not replace explicit findings with an opaque compliance score.

---

# Finding Invariants

The Findings and Severity Model establishes the following invariants:

1. Rules and findings have different identities.
2. Findings belong to specific evaluations.
3. Severity and rule outcome are separate.
4. Finding category and severity are separate.
5. Overall compliance status is derived independently.
6. Failed rules normally produce violation findings.
7. Missing evidence remains distinguishable from non-compliance.
8. Validator failures remain distinguishable from plugin failures.
9. Findings reference supporting evidence.
10. Actionable violations provide remediation guidance.
11. Suppressions remain visible.
12. Exceptions remain visible.
13. Exceptions do not convert FAIL into PASS.
14. CRITICAL findings receive the strongest enforcement.
15. Mandatory-rule findings cannot be silently bypassed.
16. Historical findings remain immutable.
17. Finding presentation is deterministic.
18. Severity semantics are globally governed.
19. Profiles determine decision impact, not finding meaning.
20. Compliance cannot be reduced to a severity count.

---

# Reference Model

The complete model is:

```text
Compliance Rule
      │
      ▼
Validation
      │
      ▼
Rule Outcome
      │
      ├── PASS
      ├── FAIL
      ├── NOT_APPLICABLE
      ├── NOT_EVALUATED
      └── ERROR
             │
             ▼
          Finding
             │
      ┌──────┼────────┐
      ▼      ▼        ▼
 Severity Category  Evidence
      │
      ▼
Suppression / Exception Policy
      │
      ▼
Compliance Decision
      │
      ▼
Overall Compliance Status
```

This architecture prevents compliance semantics from becoming ambiguous.

---

# Findings Summary

The FamilyOS Findings and Severity Model provides a consistent language for explaining compliance conditions.

Its purpose can be summarized as:

```text
Observed Condition
      +
Rule Context
      +
Evidence
      +
Severity
      +
Category
      +
Remediation
      =
Compliance Finding
```

Findings then become inputs to policy-driven compliance decisions.

---

# Final Findings Principle

The governing principle of the Findings and Severity Model is:

> Findings must explain what was observed, while policy determines what that observation means for compliance.

This separation allows FamilyOS to produce compliance results that are clear, deterministic, auditable, and consistent across development, CI, release, and certification workflows.
