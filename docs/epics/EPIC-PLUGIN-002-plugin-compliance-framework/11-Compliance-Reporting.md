# Plugin Compliance Framework

# 11 Compliance Reporting

## Introduction

Compliance Reporting defines how FamilyOS exposes plugin compliance results to developers, CI systems, release workflows, certification systems, and governance processes.

Reporting is a projection of the canonical Compliance Result.

It must never become an independent source of compliance semantics.

The same evaluation must retain the same meaning regardless of whether its result is presented through:

* CLI output;
* machine-readable data;
* CI summaries;
* release reports;
* certification packages;
* governance dashboards.

The core relationship is:

```text
Compliance Result
       │
       ├── Human-Readable Report
       ├── Machine-Readable Report
       ├── CI Summary
       ├── Release Summary
       └── Certification Evidence
```

---

# Purpose

The purpose of Compliance Reporting is to transform structured compliance data into representations appropriate for different consumers while preserving one canonical meaning.

The reporting model provides the foundation required to:

* communicate overall compliance status;
* expose active profile context;
* expose rule outcomes;
* group findings by domain;
* expose evidence references;
* preserve framework and platform versions;
* communicate remediation guidance;
* distinguish plugin failure from validation infrastructure failure;
* support CI automation;
* support release governance;
* support certification workflows;
* preserve auditability;
* support historical comparison.

Reports must remain deterministic and traceable to the underlying evaluation.

---

# Reporting Principle

The governing reporting principle is:

> Reports explain compliance results; they do not define them.

The canonical Compliance Result is the authoritative source.

A renderer may change presentation.

It must not change:

* rule outcome;
* severity;
* finding meaning;
* profile;
* compliance status;
* certification eligibility.

---

# Canonical Reporting Source

All report formats must derive from one structured Compliance Result.

Conceptually:

```text
Validation Engine
       │
       ▼
Compliance Result
       │
       ├────────► CLI Renderer
       ├────────► JSON Renderer
       ├────────► CI Renderer
       ├────────► Release Renderer
       └────────► Certification Renderer
```

Renderers must not independently rerun compliance policy.

---

# Compliance Result Context

Every complete report must identify the validation context.

At minimum:

```text
Evaluation ID
Plugin ID
Plugin Version
Plugin Classification
Platform Version
Compliance Framework Version
Profile ID
Profile Version
Execution Mode
Validation Timestamp
Overall Compliance Status
```

Where applicable, the report should also identify:

```text
Source Revision
Artifact Digest
Validator Set
Evidence Trust Context
Certification Target
```

Without this context, a compliance result is incomplete.

---

# Report Identity

Every generated report should be associated with its Evaluation ID.

A report may also have its own representation-specific identity where required.

For example:

```text
Evaluation ID: evaluation-123
Report Format: json
```

The evaluation remains the primary compliance identity.

---

# Report Types

The framework should support several report categories.

The baseline includes:

```text
DEVELOPER
MACHINE
CI
RELEASE
CERTIFICATION
GOVERNANCE
```

These categories describe intended consumption.

They do not define different compliance results.

---

# Developer Report

The Developer Report prioritizes remediation and clarity.

It should answer quickly:

* is the plugin compliant;
* which profile was used;
* what failed;
* where it failed;
* how severe the issue is;
* how to fix it;
* what remains unevaluated.

The report should minimize irrelevant infrastructure detail while preserving access to diagnostics when needed.

---

# Developer Summary

A conceptual developer summary may look like:

```text
Plugin: communication
Version: 1.2.0
Profile: official
Status: NON_COMPLIANT

Critical: 0
Errors: 2
Warnings: 3
Info: 1

Failed Domains:
  Architecture
  Documentation
```

The exact visual format belongs to CLI presentation design.

---

# Developer Finding Detail

A finding should be rendered with enough information to act.

Example:

```text
ERROR PLUGIN-ARCH-001

Unsupported internal runtime import detected.

Location:
src/familyos_plugin/service.py:18

Evidence:
import familyos.runtime.internal.loader

Remediation:
Use the public Plugin SDK runtime interface.
```

The human report should not require developers to inspect raw serialized objects.

---

# Machine-Readable Report

Machine-readable reports provide the canonical integration format for automated consumers.

They should preserve all semantic fields required for deterministic processing.

A conceptual structure includes:

```text
ComplianceReport
├── schema_version
├── evaluation
├── plugin
├── platform
├── framework
├── profile
├── status
├── domain_summaries
├── rule_outcomes
├── findings
├── evidence_refs
├── exceptions
├── suppressions
├── diagnostics
└── certification_eligibility
```

The final serialization schema should be formally specified.

---

# Report Schema Version

Machine-readable reports must identify their schema version.

Example:

```text
schema_version: 1.0
```

Report schema versioning must remain distinct from:

```text
Compliance Framework Version
Profile Version
Rule Version
Plugin Version
```

This allows representation changes without confusing them with compliance policy changes.

---

# Schema Compatibility

Report consumers should be able to determine whether they support a given report schema.

Breaking schema changes require explicit version transitions.

Backward-compatible additions should avoid changing the meaning of existing fields.

---

# Machine-Readable Formats

The initial implementation may support JSON.

Future formats may include:

* YAML;
* SARIF;
* signed evidence bundles;
* registry-specific representations.

The canonical semantic model must remain format-independent.

---

# JSON Reporting

JSON is suitable for:

* CI integration;
* release automation;
* scripting;
* certification services;
* future dashboards.

A JSON report should preserve structured values rather than embed important semantics only in human-readable strings.

---

# Human and Machine Consistency

Human-readable and machine-readable reports must represent the same evaluation.

For example:

```text
Human:
Status: NON_COMPLIANT

Machine:
status = "NON_COMPLIANT"
```

A renderer bug must not create contradictory compliance meaning.

---

# Overall Status Reporting

Every report must clearly expose the overall compliance status.

The baseline statuses are:

```text
COMPLIANT
NON_COMPLIANT
INCOMPLETE
ERROR
```

The report should not substitute these with vague labels such as:

```text
Mostly Good
Nearly Ready
Acceptable
```

unless those labels are explicitly supplemental and never replace canonical status.

---

# Status Explanation

Reports should explain why the overall status was derived.

For example:

```text
Status: NON_COMPLIANT

Reason:
2 blocking ERROR findings under profile official.
```

or:

```text
Status: INCOMPLETE

Reason:
3 required rules were not evaluated because test evidence is unavailable.
```

This improves explainability.

---

# Domain Summaries

Reports should summarize compliance by domain.

Example:

```text
Identity        PASS
Metadata        PASS
Architecture    FAIL
Capabilities    PASS
Security        PASS
Testing         PASS
Quality         PASS
Documentation   FAIL
Compatibility   PASS
Lifecycle       PASS
Governance      PASS
```

Domain summaries provide navigation and risk concentration without replacing individual rule outcomes.

---

# Domain Metrics

A domain summary may include:

```text
Rules Evaluated
Rules Passed
Rules Failed
Rules Not Applicable
Rules Not Evaluated
Rule Errors
Findings by Severity
```

These values must be derived from canonical rule outcomes.

---

# Rule Reporting

Machine-readable reports should preserve every applicable rule outcome.

A conceptual representation includes:

```text
Rule ID
Domain
Outcome
Severity
Applicability
Evidence References
Finding References
Validator
Timestamp
```

Rules that are `NOT_APPLICABLE` should remain visible when full traceability is required.

---

# Findings Reporting

Reports must preserve all relevant findings.

For each finding:

```text
Finding ID
Rule ID
Domain
Category
Severity
Status
Title
Message
Location
Evidence References
Remediation
Suppression
Exception
```

Human renderers may collapse lower-priority fields until requested.

The structured report must preserve them.

---

# Findings Summary

Reports may provide severity summaries such as:

```text
CRITICAL: 0
ERROR:    4
WARNING:  7
INFO:     3
```

A count summary is useful but cannot replace finding details.

---

# Finding Grouping

Human reports may group findings by:

* severity;
* domain;
* file;
* rule family;
* remediation area.

Grouping is presentation only.

The canonical report preserves individual findings.

---

# Evidence Reporting

Reports should preserve references to evidence used during evaluation.

Machine-readable reports may include either:

* embedded normalized evidence;
* evidence references;
* links to external artifacts;
* artifact digests.

Large raw evidence should not necessarily be embedded directly.

---

# Evidence Summary

A report may summarize evidence such as:

```text
Evidence Collected: 42
Trusted: 31
Local: 11
Stale Rejected: 2
Conflicts: 0
```

Trust-level details should only be shown where meaningful to the active profile.

---

# Evidence Redaction

Reports must avoid leaking secrets or unnecessary sensitive data.

Human and machine renderers should preserve evidence meaning while applying required redaction.

For example:

```text
Secret detected in prohibited configuration location
```

is valid.

The secret value itself must not appear in the report.

---

# Exception Reporting

Approved exceptions must remain visible.

A report should identify:

```text
Exception ID
Rule ID
Scope
Authority
Justification
Expiration
Status
```

The report must not present an excepted rule as an ordinary PASS.

---

# Suppression Reporting

Suppressions must remain visible in structured reporting.

Human output may collapse suppression metadata when low priority, but the user must be able to inspect it.

The canonical finding remains present.

---

# Incomplete Evaluation Reporting

INCOMPLETE evaluations require clear explanation.

Reports should identify:

* rules not evaluated;
* missing evidence;
* pending manual reviews;
* unsupported validators;
* skipped required validation.

For example:

```text
3 required rules were not evaluated:
  PLUGIN-TEST-004 — missing test evidence
  PLUGIN-SEC-009 — manual review required
  PLUGIN-LIFE-003 — lifecycle environment unavailable
```

---

# Validation Error Reporting

Infrastructure failures must be separated from plugin compliance findings.

A report may include:

```text
Validation Errors:
  validator testing.results failed to parse report
```

This should not appear as:

```text
Plugin test compliance failed
```

unless actual test evidence demonstrates non-compliance.

---

# Diagnostic Reporting

Diagnostics belong to a separate report section.

Possible diagnostic categories include:

* engine;
* validator;
* evidence;
* profile;
* rule graph;
* configuration;
* serialization.

Diagnostics should support debugging without polluting compliance semantics.

---

# Certification Eligibility Reporting

Where applicable, reports may expose:

```text
Certification Eligibility: ELIGIBLE
```

or:

```text
Certification Eligibility: NOT_ELIGIBLE
```

Eligibility must be derived from defined certification profile policy.

It must not be interpreted as certification itself.

---

# Certification Report

A Certification Report is a stronger representation intended for certification workflows.

It may require:

* exact profile;
* complete rule outcomes;
* trusted evidence provenance;
* artifact digest;
* no unresolved blocking findings;
* exception metadata;
* framework version;
* certification eligibility.

Certification consumers should operate on structured data rather than screen-scraped CLI output.

---

# Release Report

A Release Report provides the compliance information required by release governance.

It may include:

```text
Release Candidate
Artifact Version
Artifact Digest
Compliance Profile
Compliance Status
Blocking Findings
Evidence Completeness
Compatibility Status
Lifecycle Validation
```

Release reporting should bind compliance to the exact artifact being considered.

---

# CI Report

CI reporting should provide concise automated feedback.

A CI summary may include:

```text
Plugin Compliance: NON_COMPLIANT
Profile: official
Blocking Findings: 2
Warnings: 1
```

and expose detailed artifacts separately.

---

# CI Annotations

Where CI platforms support annotations, findings may be mapped to:

* files;
* lines;
* warning/error levels;
* rule identifiers.

CI annotation logic must preserve the canonical finding severity and rule identity.

---

# CI Exit Behavior

CI should derive success or failure from overall Compliance Status and pipeline policy.

A conceptual model is:

```text
COMPLIANT      -> success
NON_COMPLIANT  -> failure
INCOMPLETE     -> failure
ERROR          -> infrastructure failure
```

The exact exit-code mapping belongs to CLI and CI integration specifications.

---

# Governance Report

Governance reports may prioritize:

* exceptions;
* suppressions;
* deprecated rules;
* expiring approvals;
* profile migrations;
* compliance drift;
* unresolved critical findings.

Governance reports are projections of canonical results and historical records.

---

# Historical Reporting

The reporting architecture should support comparison across evaluations.

A historical view may show:

```text
Evaluation A
  NON_COMPLIANT

Evaluation B
  NON_COMPLIANT

Evaluation C
  COMPLIANT
```

with finding changes such as:

```text
Resolved: 3
New: 0
Unchanged: 1
```

Historical comparison must not mutate past results.

---

# Compliance Drift Reporting

A previously compliant plugin may become non-compliant because of rule, platform, or dependency evolution.

Reports should eventually support drift indicators.

Example:

```text
Previous Status: COMPLIANT
Current Status: NON_COMPLIANT

Cause:
New mandatory rule PLUGIN-SEC-014
```

This helps separate code regressions from ecosystem policy changes.

---

# Report Determinism

Given the same Compliance Result and renderer version, report output should be stable.

Deterministic output improves:

* snapshot testing;
* CI diffs;
* auditability;
* developer confidence.

Presentation fields such as timestamps may naturally differ where regenerated independently.

Semantic content must not.

---

# Report Ordering

Reports should use stable ordering.

Suggested ordering:

```text
Summary
Context
Domain Summary
Critical Findings
Error Findings
Warning Findings
Info Findings
Incomplete Rules
Validation Errors
Exceptions
Suppressions
Evidence Summary
Diagnostics
```

Structured formats should also define deterministic array ordering where practical.

---

# Rule Ordering

Rules may be ordered by:

```text
Domain
Rule ID
```

This creates stable and predictable report output.

---

# Finding Ordering

Human-readable reports should prioritize:

```text
CRITICAL
ERROR
WARNING
INFO
```

Within severity:

```text
Domain
Rule ID
Location
Finding ID
```

This allows high-impact issues to appear first.

---

# Verbosity Levels

Human reporting may support verbosity levels such as:

```text
summary
standard
verbose
```

## Summary

Shows overall status and major findings.

## Standard

Shows all actionable findings and essential context.

## Verbose

Shows detailed evidence, diagnostics, and rule evaluation information.

Verbosity changes presentation only.

---

# Explain Mode

Tooling should support explaining individual findings or rules.

For example:

```text
familyos plugin compliance explain PLUGIN-ARCH-001
```

or a finding-specific query.

Explain mode may display:

* requirement;
* rationale;
* evidence;
* remediation;
* profile impact;
* source references.

---

# Report Portability

Machine-readable reports should be portable between:

```text
Local Development
      │
      ▼
CI
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

Portability requires schema stability and complete context.

---

# Artifact Binding

Release and certification reports should support binding to exact artifacts.

A conceptual relationship is:

```text
Plugin Artifact
      │
      ▼
Artifact Digest
      │
      ├── Compliance Result
      └── Compliance Report
```

This prevents a report from being mistakenly applied to a different artifact.

---

# Report Integrity

Future reporting may support integrity metadata such as:

* content digest;
* signature;
* producer attestation.

This becomes important when reports cross organizational or infrastructure trust boundaries.

---

# Signed Reports

A future signed report could provide:

```text
Compliance Report
      +
Artifact Digest
      +
Producer Identity
      +
Signature
```

This may be useful for certification or remote registry workflows.

Signed reports are not required for the initial implementation.

---

# Report Storage

The framework should not require permanent storage in its core architecture.

However, reports should be designed so external systems can persist them.

Possible consumers include:

* CI artifact storage;
* release systems;
* plugin registries;
* certification services;
* audit archives.

---

# Report Retention

Retention policy depends on workflow.

Development reports may be ephemeral.

Release and certification reports may require long-term retention.

Retention requirements belong to governance and infrastructure policy.

---

# Report Privacy

Reports may expose information about:

* plugin internals;
* source paths;
* dependencies;
* security findings;
* configuration;
* infrastructure.

Report renderers must support data minimization and redaction.

Public reports may require stronger redaction than internal reports.

---

# Public Reporting

If FamilyOS later exposes plugin compliance publicly, public reports should reveal only information appropriate for ecosystem consumers.

A public report may expose:

```text
Plugin
Version
Compliance Profile
Compliance Status
Certification Status
Framework Version
Evaluation Date
```

Detailed security evidence may remain restricted.

---

# Internal Reporting

Internal reports may contain richer information including:

* detailed findings;
* file locations;
* evidence diagnostics;
* validator output;
* exceptions;
* suppression details.

Access policy belongs to governance and infrastructure.

---

# Report Generation API

The reporting layer should expose stable rendering contracts.

Conceptually:

```text
ReportRenderer.render(result) -> Report
```

Different renderers may implement:

```text
TextRenderer
JsonRenderer
CiRenderer
ReleaseRenderer
CertificationRenderer
```

Renderers receive finalized Compliance Results.

---

# Renderer Independence

Renderers must not invoke validators or mutate results.

Their responsibility is transformation and presentation.

This preserves architectural separation.

---

# Report Validation

Machine-readable reports should themselves be validatable against a schema.

This enables consumers to detect:

* malformed reports;
* missing required fields;
* unsupported schema versions;
* invalid enum values.

Report schema validation is an integration concern, not plugin compliance validation.

---

# Report Testing

Reporting infrastructure requires dedicated tests.

Core test categories include:

* rendering;
* serialization;
* schema validation;
* deterministic ordering;
* redaction;
* finding grouping;
* domain summaries;
* status consistency;
* exception representation;
* incomplete evaluation representation;
* validation error representation.

---

# Cross-Renderer Consistency Tests

FamilyOS should test that different renderers preserve identical semantics.

For example:

```text
Text Status == JSON Status
Text Rule ID == JSON Rule ID
Text Severity == JSON Severity
```

Presentation differences are acceptable.

Semantic divergence is not.

---

# Report Anti-Patterns

The framework must avoid several reporting anti-patterns.

## Recomputing Compliance

Renderers must not derive their own overall status.

## Hidden Context

Never report COMPLIANT without showing which profile was evaluated.

## Score-Only Reporting

Do not replace explicit rule outcomes with a percentage score.

## Silent Findings

Do not omit blocking findings from standard human output.

## Error Conflation

Do not mix validator infrastructure errors with plugin violations.

## Exception Hiding

Do not present excepted failures as ordinary passes.

## Schema Ambiguity

Do not change field meaning without schema versioning.

---

# Compliance Score

The framework may eventually provide supplemental scoring or maturity indicators.

However, scores must never replace canonical compliance status.

For example:

```text
Compliance Status: NON_COMPLIANT
Score: 96%
```

must remain non-compliant if a blocking critical requirement failed.

A high numerical score cannot override explicit policy.

---

# Reporting Invariants

The Compliance Reporting model establishes the following invariants:

1. Every report derives from a canonical Compliance Result.
2. Renderers do not redefine compliance policy.
3. Every complete report identifies its profile.
4. Every complete report identifies framework and platform versions.
5. Overall status uses canonical compliance states.
6. Findings preserve rule IDs and severities.
7. Missing evidence remains visible.
8. Validation errors remain distinct from plugin violations.
9. Exceptions and suppressions remain visible.
10. Human and machine reports preserve the same semantics.
11. Domain summaries derive from rule outcomes.
12. Machine-readable reports have explicit schema versions.
13. Report formatting does not alter compliance meaning.
14. Release and certification reports may bind to exact artifacts.
15. Reports must support redaction where sensitive data exists.
16. Historical reports remain immutable.
17. Report ordering should remain deterministic.
18. Certification eligibility is not certification.
19. Compliance scores cannot override canonical status.
20. Consumers should not parse human-readable output when structured output exists.

---

# Reference Reporting Model

The complete reporting flow is:

```text
Validation Engine
       │
       ▼
Compliance Result
       │
       ├── Context
       ├── Rule Outcomes
       ├── Findings
       ├── Evidence References
       ├── Exceptions
       ├── Suppressions
       ├── Diagnostics
       └── Status
              │
              ▼
        Reporting Layer
              │
      ┌───────┼────────┐
      ▼       ▼        ▼
     CLI      CI      JSON
      │       │        │
      └───────┼────────┘
              ▼
        Release / Certification
```

All projections preserve the same underlying compliance semantics.

---

# Reporting Summary

The FamilyOS Compliance Reporting model transforms structured compliance results into reliable interfaces for humans and automated systems.

Its role can be summarized as:

```text
Compliance Result
      +
Consumer Context
      +
Renderer
      =
Compliance Report
```

The renderer may change presentation.

It must never change meaning.

---

# Final Reporting Principle

The governing principle of Compliance Reporting is:

> One compliance evaluation may have many representations, but it must have only one meaning.

This principle ensures that developers, CI systems, release workflows, certification systems, and governance processes all consume a consistent and trustworthy interpretation of FamilyOS plugin compliance.
