# RFC-0014 — Official Documents Plugin

## Metadata

| Field | Value |
|---|---|
| Identifier | RFC-0014 |
| Title | Official Documents Plugin |
| Version | 0.1.0 |
| Status | Draft |
| EPIC | EPIC-014 |
| Domain | Documents |
| Plugin ID | `documents` |
| Architecture dependency | ADR-0007 |
| Platform target | FamilyOS Platform v1.0 |

## Abstract

This RFC specifies the official FamilyOS Documents plugin.

The plugin provides document-domain generation capabilities, templates, recipes,
domain policies, and domain rules through the official plugin architecture.

It does not replace a document management system. It defines the FamilyOS
document domain and generates coherent source artifacts and documentation for
projects that adopt that domain.

## Decision

FamilyOS SHALL include an official built-in plugin identified by `documents`.

The plugin SHALL:

- expose stable plugin metadata;
- declare a Documents generation capability;
- contribute the `documents` generation preset;
- contribute one or more Documents generation recipes;
- contribute Documents templates;
- define Documents policies and rules;
- remain isolated from platform core concerns;
- use only public Plugin SDK v2 contracts.

## Scope

This RFC governs the documentation and implementation contract for:

```text
src/familyos_cli/plugins/builtin/documents/
tests/unit/plugins/builtin/documents/
docs/rfcs/RFC-0014-official-documents-plugin/
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
- RFC-0013 — Official Education Plugin
- FamilyOS Platform v1.0 architecture
- Plugin SDK v2
- FamilyOS Specifications and Reference documentation
