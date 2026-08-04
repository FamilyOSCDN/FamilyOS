# 03 — Architecture

## Overview

The Documents plugin is an official built-in plugin implemented within the
FamilyOS plugin layer.

Recommended package structure:

```text
src/familyos_cli/plugins/builtin/documents/
├── __init__.py
├── plugin.py
├── plugin.yaml
├── policies/
│   ├── __init__.py
│   ├── document_policy.py
│   └── document_policy_set.py
├── rules/
│   ├── __init__.py
│   ├── document_rule.py
│   └── document_rule_set.py
├── recipes/
│   ├── __init__.py
│   └── documents_documentation_recipe.py
└── templates/
    └── documents/
        └── ...
```

Recommended test structure:

```text
tests/unit/plugins/builtin/documents/
├── test_documents_plugin.py
├── test_documents_plugin_contributions.py
├── policies/
├── rules/
├── recipes/
└── templates/
```

## Plugin descriptor

The plugin descriptor SHOULD declare:

```yaml
id: documents
name: Documents Plugin
version: 1.0.0
author: FamilyOS Team
module: familyos_cli.plugins.builtin.documents.plugin
class: DocumentsPlugin
enabled: true
```

The final descriptor MUST conform to the repository's current manifest schema.

## Plugin class

The plugin class SHALL extend the public `Plugin` abstraction.

Conceptual contract:

```python
class DocumentsPlugin(Plugin):
    @property
    def metadata(self) -> PluginMetadata:
        ...

    @property
    def capabilities(self) -> tuple[PluginCapability, ...]:
        ...

    @property
    def contributions(self) -> tuple[Contribution, ...]:
        ...
```

Exact signatures SHALL follow the current Plugin SDK v2 implementation.

## Contributions

The plugin SHALL contribute at least:

1. `GenerationContribution(preset="documents")`
2. a `GenerationRecipeContribution`
3. a `TemplateContribution` for Documents templates

Conceptual contribution graph:

```text
DocumentsPlugin
├── GenerationContribution
│   └── preset: documents
├── GenerationRecipeContribution
│   └── DocumentsDocumentationRecipe
└── TemplateContribution
    └── templates/documents
```

## Capability model

The plugin SHALL declare a capability whose stable identifier is:

```text
documents.generation
```

Recommended display name:

```text
Documents Generation
```

The capability description SHOULD explain that the plugin generates
Documents-domain artifacts and documentation.

## Policies

A document policy expresses a configurable or declarative constraint governing
document-domain behavior.

The initial policy model SHOULD support:

- identifier;
- name;
- description;
- enabled state;
- metadata.

A policy set SHALL provide deterministic ordering and lookup behavior.

## Rules

A document rule expresses a domain invariant or validation rule.

The initial rule model SHOULD support:

- identifier;
- name;
- description;
- severity or category when justified;
- metadata.

A rule set SHALL provide deterministic ordering and lookup behavior.

## Recipes

The initial recipe SHOULD generate Documents domain documentation.

It MAY later be extended by additional recipes, but the first implementation
SHOULD remain focused and deterministic.

The recipe SHALL use public generation contracts only.

## Templates

Templates SHALL be owned by the plugin.

Templates MUST NOT depend on private runtime details.

Template paths SHOULD be stable and discoverable through
`TemplateContribution`.

## Dependency direction

Allowed dependency direction:

```text
documents plugin
    ↓
public plugin SDK
    ↓
public contribution contracts
    ↓
public generation contracts
```

Forbidden dependency direction:

```text
platform core
    ↓
documents plugin internals
```

The platform core MUST NOT import Documents-specific modules.

## Runtime behavior

The plugin SHALL be discoverable, loadable, and inspectable through the existing
plugin runtime.

Loading the plugin MUST NOT perform document I/O, network I/O, or external
service initialization.

## Error handling

Invalid plugin configuration MUST fail explicitly.

Invalid document policy or rule definitions MUST raise domain-specific errors or
standard validation errors consistent with existing official plugin patterns.

Silent fallback behavior SHOULD be avoided.
