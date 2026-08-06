# Documentation Framework

# 07 Documentation Metadata

## Purpose

Documentation metadata defines the information required to identify, classify, manage, and automate FamilyOS documentation artifacts.

Metadata provides structured information about documentation resources and enables:

- traceability,
- lifecycle management,
- automation,
- validation,
- discoverability.

Every official FamilyOS documentation artifact SHOULD contain appropriate metadata.

## Metadata Principles

FamilyOS documentation metadata follows these principles:

- consistency,
- completeness,
- accuracy,
- machine readability,
- long-term stability.

Metadata MUST describe the document itself and MUST NOT replace the document content.

## Metadata Objectives

Documentation metadata enables:

- artifact identification,
- ownership tracking,
- version management,
- status visibility,
- automated processing,
- dependency management.

## Required Metadata Fields

Official documentation artifacts SHOULD define the following metadata fields.

## Identifier

The identifier uniquely identifies the documentation artifact.

Examples:

- RFC-0015
- ADR-0007
- EPIC-DOC-001
- SPEC-0005

Identifiers MUST:

- be unique,
- remain stable,
- never be reused.

## Title

The title provides the human-readable name of the document.

Titles SHOULD:

- clearly describe the subject,
- use approved terminology,
- remain consistent with repository naming.

## Document Type

The document type defines the category of documentation.

Examples:

- RFC,
- ADR,
- EPIC,
- SPEC,
- GUIDE,
- REFERENCE.

The document type determines:

- expected structure,
- validation rules,
- lifecycle behavior.

## Version

The version identifies the current document revision.

Versioning SHOULD follow controlled version management.

Examples:

```text
1.0.0
1.1.0
2.0.0

Version changes SHOULD reflect the impact of modifications.

Status

The status indicates the lifecycle state of the document.

Supported statuses include:

Draft,
Review,
Approved,
Active,
Deprecated,
Archived.

Status changes MUST follow lifecycle rules.

Ownership

Ownership identifies responsibility for maintaining the document.

Ownership information MAY include:

team,
role,
maintainer,
domain owner.

Ownership ensures accountability.

Creation Information

Creation metadata records initial document information.

Examples:

creation date,
initial author,
originating feature or decision.

Creation information improves historical traceability.

Update Information

Update metadata records document evolution.

Examples:

last update date,
last editor,
change reference.

Update information supports maintenance activities.

Metadata Structure

Metadata MAY be represented using structured formats.

Examples:

YAML front matter,
JSON metadata files,
EPIC manifests,
specification descriptors.

Example:

id: EPIC-DOC-001
title: Documentation Framework
type: EPIC
version: 1.0.0
status: Active
Metadata Location

Metadata MAY exist:

inside the document,
in a companion file,
in repository manifests.

The chosen approach MUST remain consistent within a documentation category.

Metadata Validation

Metadata SHOULD be validated automatically.

Validation MAY verify:

identifier format,
required fields,
version format,
status values,
reference integrity.

Invalid metadata SHOULD prevent publication of official documentation.

Metadata and Automation

Metadata enables automated documentation workflows.

Automation MAY use metadata for:

indexing,
generation,
publication,
validation,
reporting.
Metadata and Traceability

Metadata creates relationships between:

documentation artifacts,
source code,
requirements,
decisions,
releases.

Traceability information SHOULD remain available throughout the document lifecycle.

Metadata Governance

Metadata standards are governed by the Documentation Framework.

Changes to metadata rules SHOULD consider:

backward compatibility,
automation impact,
repository consistency.
Metadata Evolution

Metadata requirements evolve with FamilyOS needs.

Future improvements SHOULD support:

stronger automation,
better discovery,
improved governance,
ecosystem scalability.

Documentation metadata provides the foundation for reliable documentation management across FamilyOS.
