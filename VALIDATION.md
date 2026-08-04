# EPIC-014 Package Validation

## Structural validation

- [x] `EPIC.yaml` exists.
- [x] `MANIFEST.md` exists.
- [x] `CHANGELOG.md` exists.
- [x] `VALIDATION.md` exists.
- [x] RFC-0014 directory exists.
- [x] All required RFC documents exist.
- [x] File names match the approved structure.
- [x] Internal navigation is defined.

## Content validation

- [x] The RFC identifies the Documents plugin as an official built-in plugin.
- [x] The RFC defines responsibilities and boundaries.
- [x] Goals and non-goals are explicit.
- [x] Architecture is compatible with Plugin SDK v2.
- [x] Public API expectations are documented.
- [x] The implementation plan is incremental.
- [x] Validation includes MyPy, Ruff, Pytest, and integration checks.

## Repository integration validation

After copying this package into the repository, run:

```bash
find docs/rfcs/RFC-0014-official-documents-plugin -maxdepth 1 -type f | sort

python - <<'PY'
from pathlib import Path
import yaml

path = Path("EPIC.yaml")
data = yaml.safe_load(path.read_text(encoding="utf-8"))

assert data["id"] == "EPIC-014"
assert data["primary_rfc"] == "RFC-0014"
assert data["plugin_id"] == "documents"
assert data["version"] == "0.1.0"

print("EPIC-014 metadata validation passed.")
PY
```

When implementation begins, the following project checks SHALL pass:

```bash
mypy src/familyos_cli/plugins/builtin/documents

ruff check src/familyos_cli/plugins/builtin/documents tests/unit/plugins/builtin/documents

pytest tests/unit/plugins/builtin/documents -q
```

Before release, global validation SHALL pass:

```bash
mypy src
ruff check src tests
pytest -q
```

## Validation result

**Package version:** 0.1.0  
**Documentation structure:** Valid  
**Implementation status:** Not started by this package  
**Release status:** Draft baseline
