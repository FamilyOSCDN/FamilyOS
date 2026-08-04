# 06 — Validation

## Conformance requirements

An implementation conforms to RFC-0014 when all mandatory requirements in this
document set are satisfied.

## Structural validation

The implementation SHALL contain:

```text
src/familyos_cli/plugins/builtin/documents/
tests/unit/plugins/builtin/documents/
```

The plugin package SHALL include:

- plugin metadata;
- plugin implementation;
- capability declaration;
- contributions;
- policies;
- rules;
- recipe;
- templates.

## Plugin validation

Tests SHALL verify:

- the plugin can be instantiated;
- plugin metadata is correct;
- plugin ID is `documents`;
- the plugin is enabled by default when required by the manifest;
- capability ID is `documents.generation`;
- contributions are deterministic;
- the `documents` preset is exposed;
- the Documents recipe is exposed;
- the Documents template root is exposed.

## Policy validation

Tests SHALL verify:

- valid policies are accepted;
- empty identifiers are rejected;
- duplicate identifiers are rejected;
- lookup behavior is deterministic;
- ordering is stable;
- exposed collections cannot be mutated unexpectedly.

## Rule validation

Tests SHALL verify:

- valid rules are accepted;
- empty identifiers are rejected;
- duplicate identifiers are rejected;
- lookup behavior is deterministic;
- ordering is stable;
- exposed collections cannot be mutated unexpectedly.

## Recipe validation

Tests SHALL verify:

- recipe identity;
- recipe description;
- artifact declarations;
- deterministic artifact order;
- compatibility with the recipe catalog;
- compatibility with the recipe executor.

## Template validation

Tests SHALL verify:

- template root discovery;
- template availability;
- successful rendering;
- deterministic output;
- absence of unresolved template variables;
- consistency with generated artifact declarations.

## Integration validation

The existing generation workflow SHOULD successfully execute a command
equivalent to:

```bash
familyos create domain Documents     --specification specifications/documents-domain.yaml     --preset documents
```

The exact specification path MAY differ.

The generated domain SHALL contain the artifacts declared by the recipe.

## Static validation

Targeted checks:

```bash
mypy src/familyos_cli/plugins/builtin/documents

ruff check src/familyos_cli/plugins/builtin/documents tests/unit/plugins/builtin/documents
```

Test checks:

```bash
pytest tests/unit/plugins/builtin/documents -q
```

Global checks:

```bash
mypy src
ruff check src tests
pytest -q
```

## Documentation validation

Documentation SHALL:

- use RFC-0014 consistently;
- use `documents` consistently as the plugin and preset identifier;
- reference ADR-0007 where architectural rules apply;
- separate normative requirements from informative guidance;
- avoid implementation details that contradict the repository;
- remain self-contained.

## Acceptance checklist

- [ ] Plugin package created.
- [ ] Manifest created.
- [ ] Plugin metadata implemented.
- [ ] Capability implemented.
- [ ] Generation preset contribution implemented.
- [ ] Recipe contribution implemented.
- [ ] Template contribution implemented.
- [ ] Policies implemented and tested.
- [ ] Rules implemented and tested.
- [ ] Recipe implemented and tested.
- [ ] Templates implemented and tested.
- [ ] Targeted MyPy passes.
- [ ] Targeted Ruff passes.
- [ ] Targeted Pytest passes.
- [ ] Global MyPy passes.
- [ ] Global Ruff passes.
- [ ] Global Pytest passes.
- [ ] Repository documentation indexes updated.

## Release condition

RFC-0014 MAY move from **Draft** to **Approved** only after:

1. architectural review;
2. implementation completion;
3. full validation;
4. repository integration;
5. documentation index updates.
