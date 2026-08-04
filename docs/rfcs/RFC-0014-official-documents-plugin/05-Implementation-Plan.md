# 05 — Implementation Plan

## Delivery strategy

Implementation SHALL proceed incrementally.

Each step MUST leave the repository in a valid state.

## Step 1 — Package foundation

Create:

```text
src/familyos_cli/plugins/builtin/documents/
├── __init__.py
├── plugin.py
└── plugin.yaml
```

Add tests for:

- plugin construction;
- metadata;
- plugin identifier;
- descriptor loading;
- enabled state.

## Step 2 — Capability

Add the `documents.generation` capability.

Add tests for:

- capability identifier;
- display name;
- description;
- deterministic capability collection.

## Step 3 — Generation contribution

Add:

```python
GenerationContribution(preset="documents")
```

Add tests proving the preset is exposed by the plugin.

## Step 4 — Policies

Create the initial policy model and policy set.

Add tests for:

- valid construction;
- invalid empty identifiers;
- deterministic ordering;
- duplicate rejection;
- lookup;
- immutability.

## Step 5 — Rules

Create the initial rule model and rule set.

Add tests for:

- valid construction;
- invalid empty identifiers;
- deterministic ordering;
- duplicate rejection;
- lookup;
- immutability.

## Step 6 — Recipe

Create `DocumentsDocumentationRecipe`.

The recipe SHALL describe its generated artifacts through current generation
contracts.

Add tests for:

- recipe identity;
- recipe description;
- generated artifact declarations;
- deterministic output;
- registration through the plugin.

## Step 7 — Templates

Create the Documents template root and initial templates.

Recommended first artifacts:

- Documents domain overview;
- document policies;
- document rules;
- document lifecycle guidance;
- document metadata guidance;
- security and privacy considerations.

Add template rendering tests.

## Step 8 — Contribution integration

The plugin contributions tuple SHALL include:

- generation preset contribution;
- generation recipe contribution;
- template contribution.

Add tests that assert contribution types and values.

## Step 9 — Catalog integration

Verify that existing catalog services can discover:

- the `documents` preset;
- the Documents recipe;
- the Documents template root.

No core special case SHALL be introduced.

## Step 10 — Documentation and release preparation

Update relevant repository indexes and official plugin documentation.

Add the plugin to any canonical built-in plugin inventory.

## Per-step quality gate

After each step, run targeted checks:

```bash
mypy src/familyos_cli/plugins/builtin/documents

ruff check src/familyos_cli/plugins/builtin/documents tests/unit/plugins/builtin/documents

pytest tests/unit/plugins/builtin/documents -q
```

## Final quality gate

Before merging:

```bash
mypy src
ruff check src tests
pytest -q
```

## Commit discipline

Recommended commit sequence:

```text
docs: add RFC-0014 official documents plugin
feat(documents): add plugin foundation
feat(documents): add generation capability
feat(documents): add policies
feat(documents): add rules
feat(documents): add documentation recipe
feat(documents): add templates
test(documents): complete plugin integration coverage
docs(documents): finalize official plugin documentation
```
