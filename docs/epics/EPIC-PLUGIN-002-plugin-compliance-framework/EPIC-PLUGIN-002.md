# EPIC-PLUGIN-002 — Plugin Compliance Framework

## Status

Completed

## Overview

EPIC-PLUGIN-002 defines the official FamilyOS Plugin Compliance Framework.

The framework establishes the canonical model for evaluating, validating,
reporting, governing, and enforcing plugin compliance across the FamilyOS
plugin ecosystem.

## Purpose

The framework provides explicit, evidence-based, and governed compliance
semantics for FamilyOS plugins.

It covers:

- plugin identity and metadata
- structure and architecture
- capabilities and contributions
- dependencies and configuration
- security
- testing and quality
- documentation
- compatibility
- lifecycle
- governance
- automation and CI integration
- compliance gates
- certification eligibility

## Canonical Documentation

The framework is defined by the numbered documents `00-23`.

These documents remain the authoritative technical and governance definition
of the Plugin Compliance Framework.

## Historical Baseline

The historical framework baseline is:

- Tag: `v4.5.0-plugin-compliance-framework`
- Commit: `34f635c5fedeb7d3923cb97c31d09a32bc63eca5`
- Historical canonical files: 30
- Historical numbered documents: 24
- Historical control documents: 6

The historical tag is immutable.

## Normalized Repository Contract

The normalized EPIC repository contains:

- 24 numbered documents
- 7 control documents
- 31 canonical files

The seven control documents are:

- `EPIC-PLUGIN-002.md`
- `EPIC.yaml`
- `README.md`
- `MANIFEST.md`
- `CHANGELOG.md`
- `VALIDATION.md`
- `Revision-History.md`

## Compliance Principles

The framework preserves the following principles:

- compliance is explicit
- compliance is evidence-based
- compliance is deterministic where possible
- compliance rules have stable identities
- policy is separate from execution
- missing evidence never implies compliance
- validator errors are distinct from plugin violations
- compliance status is derived
- exceptions and suppressions remain visible
- certification is separate from compliance
- framework evolution is governed and versioned

## Compliance Domains

The framework governs:

1. Identity
2. Metadata
3. Structure
4. Architecture
5. Capabilities
6. Contributions
7. Dependencies
8. Configuration
9. Security
10. Testing
11. Quality
12. Documentation
13. Compatibility
14. Lifecycle
15. Governance

## Rule Outcomes

Canonical rule outcomes are:

- `PASS`
- `FAIL`
- `NOT_APPLICABLE`
- `NOT_EVALUATED`
- `ERROR`

## Compliance Statuses

Canonical compliance statuses are:

- `COMPLIANT`
- `NON_COMPLIANT`
- `INCOMPLETE`
- `ERROR`

## Certification Boundary

Compliance evidence may establish certification eligibility.

Compliance does not itself grant certification.

Final certification decisions remain owned by certification governance.

## Dependencies

The framework is aligned with:

- EPIC-ENG-001
- EPIC-DOC-001
- EPIC-TST-001
- EPIC-QLT-001
- EPIC-BLD-001
- EPIC-REL-001
- ADR-0007
- ADR-0008
- ADR-0009
- ADR-0010
- ADR-0011
- ADR-0013
- RFC-0010 through RFC-0015

## Closure Model

Repository normalization does not rewrite the historical release.

The historical `v4.5.0-plugin-compliance-framework` tag remains the immutable
framework baseline.

Final repository closure must only be declared after:

- canonical filesystem validation
- control-document alignment
- repository quality gates
- normalization commit creation
- remote publication verification
- clean working-tree verification
