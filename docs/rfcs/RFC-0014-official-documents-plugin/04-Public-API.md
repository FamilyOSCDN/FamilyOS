# 04 — Public API

## Stability policy

The public API defined by this RFC is the plugin-facing contract.

Internal modules MAY evolve while public identifiers, capability IDs, preset
names, and contribution behavior remain compatible.

## Stable identifiers

| Concept | Identifier |
|---|---|
| Plugin | `documents` |
| Generation preset | `documents` |
| Capability | `documents.generation` |
| Initial recipe | `DocumentsDocumentationRecipe` |

## Plugin metadata

The plugin SHALL expose metadata equivalent to:

| Field | Value |
|---|---|
| Name | Documents Plugin |
| Version | 1.0.0 |
| Author | FamilyOS Team |
| Description | Official Documents domain plugin |
| API version | Current supported Plugin SDK API version |

The actual metadata object MUST use the repository's canonical `PluginMetadata`
model.

## Contributions API

The `contributions` property SHALL return an immutable tuple.

It SHALL include one instance of each required contribution type:

```python
(
    GenerationContribution(preset="documents"),
    GenerationRecipeContribution(...),
    TemplateContribution(...),
)
```

The order SHOULD remain deterministic.

## Capability API

The plugin SHALL expose the `documents.generation` capability using
`PluginCapabilityId`.

The capability SHALL include:

- a stable identifier;
- a human-readable display name;
- a meaningful description;
- optional metadata.

## Policy API

Recommended public models:

```python
@dataclass(frozen=True, slots=True)
class DocumentPolicy:
    identifier: str
    name: str
    description: str
    enabled: bool = True
    metadata: dict[str, str] = field(default_factory=dict)
```

```python
@dataclass(frozen=True, slots=True)
class DocumentPolicySet:
    policies: tuple[DocumentPolicy, ...]
```

The final implementation SHOULD align with patterns already established by
other official plugins.

Required behavior:

- reject empty identifiers;
- preserve deterministic ordering;
- support lookup by identifier;
- reject duplicate identifiers;
- expose immutable or read-only collections.

## Rule API

Recommended public models:

```python
@dataclass(frozen=True, slots=True)
class DocumentRule:
    identifier: str
    name: str
    description: str
    metadata: dict[str, str] = field(default_factory=dict)
```

```python
@dataclass(frozen=True, slots=True)
class DocumentRuleSet:
    rules: tuple[DocumentRule, ...]
```

Required behavior:

- reject empty identifiers;
- preserve deterministic ordering;
- support lookup by identifier;
- reject duplicate identifiers;
- expose immutable or read-only collections.

## Recipe API

The initial recipe SHALL expose a stable recipe name and description.

It SHALL declare the artifacts it generates through current generation
contracts.

The recipe MUST NOT write files directly outside the generation pipeline.

## Template API

The plugin SHALL contribute a template root for the `documents` preset.

Generated artifacts SHOULD include clear ownership metadata indicating that they
originate from the official Documents plugin.

## Import policy

Public symbols intended for downstream use SHOULD be re-exported from stable
package `__init__.py` modules.

Private helpers SHOULD remain unexported.

## Backward compatibility

After version 1.0.0 of the plugin:

- plugin ID changes are forbidden;
- capability ID changes are forbidden;
- preset renaming requires a migration strategy;
- removal of public models requires deprecation;
- contribution behavior changes require documentation and tests.
