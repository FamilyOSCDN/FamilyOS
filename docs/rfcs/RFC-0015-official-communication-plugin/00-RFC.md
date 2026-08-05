# RFC-0015 — Official Communication Plugin

## Metadata

| Field | Value |
|---|---|
| Identifier | RFC-0015 |
| Title | Official Communication Plugin |
| Version | 0.1.0 |
| Status | Draft |
| EPIC | EPIC-015 |
| Domain | Communication |
| Plugin ID | `communication` |
| Architecture dependency | ADR-0007 |
| Platform target | FamilyOS Platform v1.0 |

## Abstract

This RFC specifies the official FamilyOS Communication plugin.

The plugin provides communication-domain generation capabilities, templates,
recipes, domain policies, domain rules, and communication models through the
official plugin architecture.

It defines the FamilyOS communication domain independently from any messaging
provider. The plugin generates coherent source artifacts and documentation for
projects that manage family communication history, conversations, contacts, and
related metadata.

## Decision

FamilyOS SHALL include an official built-in plugin identified by
`communication`.

The plugin SHALL:

- expose stable plugin metadata;
- declare a Communication generation capability;
- contribute the `communication` generation preset;
- contribute one or more Communication generation recipes;
- contribute Communication templates;
- define Communication policies and rules;
- remain isolated from platform core concerns;
- use only public Plugin SDK v2 contracts.

## Scope

This RFC governs the documentation and implementation contract for:

```text
src/familyos_cli/plugins/builtin/communication/
tests/unit/plugins/builtin/communication/
docs/rfcs/RFC-0015-official-communication-plugin/
```

## Compatibility

The implementation MUST remain compatible with:

- FamilyOS Platform v1.0;
- Plugin SDK v2;
- the current contribution framework;
- the current generation framework;
- official plugin conventions established by ADR-0007.

## Normative references

- ADR-0007 — Official Plugins Architecture
- RFC-0014 — Official Documents Plugin
- FamilyOS Platform v1.0 architecture
- Plugin SDK v2
- FamilyOS Specifications and Reference documentation