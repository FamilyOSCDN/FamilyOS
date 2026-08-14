# FamilyOS CLI

FamilyOS CLI provides the command-line and engineering validation surfaces for
the FamilyOS repository. The project currently supports a controlled Python
development environment and one provider-neutral validation command shared by
local development and GitHub Actions.

The canonical package-build and candidate-artifact workflow is not implemented
yet. The commands below set up and validate the source repository; they do not
produce a release or trusted build artifact.

## Prerequisites

- Python 3.13
- Git
- a checkout of this repository

Run all commands from the repository root. Creating an isolated virtual
environment avoids mixing FamilyOS dependencies with system Python packages:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python --version
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

The reported Python version must be Python 3.13.

## Canonical controlled bootstrap

`pyproject.toml` is the sole hand-edited authority for direct dependencies.
The committed `requirements.txt` is the generated and exactly pinned Python
3.13 development/CI dependency state. Install that controlled state first,
then install FamilyOS without resolving dependencies again:

```bash
python -m pip install -r requirements.txt
python -m pip install --no-deps --no-build-isolation -e .
python -m pip check
```

Do not substitute `pip install -e ".[dev]"` for this bootstrap. That command
would perform a new dependency resolution instead of installing the committed
dependency state.

## Dependency freshness

Check that `requirements.txt` still corresponds to the canonical dependency
inputs in `pyproject.toml`:

```bash
python scripts/check_dependency_lock.py
```

This check is read-only. It does not update `requirements.txt`.

When intentionally changing a direct dependency, edit `pyproject.toml`, then
regenerate the committed dependency state with:

```bash
python scripts/compile_dependencies.py
```

Review the resulting `requirements.txt` diff, rerun the freshness check, and
run canonical validation before submitting the change. Never edit the
generated lock manually.

## Canonical local validation

Run the complete repository validation profile with:

```bash
familyos validation ci
```

The command executes the mandatory gates in deterministic order:

1. dependency freshness;
2. dependency consistency (`pip check`);
3. Ruff;
4. MyPy;
5. Pytest;
6. official builtin Plugin Compliance.

For deterministic JSON evidence, optionally write the canonical report:

```bash
familyos validation ci --output ci-validation.json
```

The generated report is local validation evidence, not a package-build
artifact. `ci-validation.json` is not currently ignored by Git, so it will
appear as an untracked file; do not commit it. Remove it after use:

```bash
rm ci-validation.json
```

The repository's `Canonical CI Validation` GitHub Actions workflow performs
the same locked bootstrap and invokes the same provider-neutral
`familyos validation ci` command. The workflow does not redefine Ruff, MyPy,
Pytest, dependency, or Plugin Compliance semantics. A validation failure that
occurs in CI can therefore normally be reproduced locally with this command.

## Common failures

### Unsupported Python version

Create and activate a Python 3.13 virtual environment. Dependency compilation
and freshness checking deliberately reject other Python minor versions.

### Dependency inputs changed

If the freshness check reports that canonical dependency inputs changed,
regenerate through `python scripts/compile_dependencies.py`, review the lock
diff, and rerun validation.

### Resolved lock content changed

Regenerate `requirements.txt` only through the compilation script. Do not
repair pins manually.

### `pip check` reports an inconsistent environment

Recreate the virtual environment and repeat the canonical controlled
bootstrap. Do not fix the environment by installing ad hoc package versions.

### `familyos` is not found

Confirm that the intended virtual environment is active and repeat the
editable installation command:

```bash
python -m pip install --no-deps --no-build-isolation -e .
```

### A canonical validation gate fails

Read the diagnostic printed beneath the failed gate. Run
`familyos validation ci --output ci-validation.json` when structured evidence
is useful. Fix the reported repository issue and rerun the complete canonical
command so local validation continues to match CI.

## Safe local cleanup

The virtual environment and tool caches are local, derived state. With the
environment deactivated, they may be removed and reconstructed from the
committed repository inputs:

```bash
deactivate
rm -rf .venv
find . -path ./.git -prune -o -type d \( \
  -name .pytest_cache -o -name .ruff_cache -o -name .mypy_cache \
  \) -exec rm -rf {} +
```

The `find` command targets only these three known cache directory names
anywhere under the repository root (for example `src/.pytest_cache` and
`src/.ruff_cache` in addition to their repository-root counterparts) and
prunes `.git`. Review the paths before removal and never use cleanup
commands against the repository root or authoritative source directories.
No canonical cleanup contract exists yet for build outputs because
canonical build and artifact generation have not been implemented.

## Current build boundary

FamilyOS does not yet expose a canonical package-build command, candidate
artifact location, artifact-validation pipeline, or build-output cleanup
command. Those capabilities remain future EPIC-BLD-001 implementation work.
Do not infer them from setuptools internals or ad hoc packaging commands.

The normative Build Framework is under
`docs/epics/EPIC-BLD-001-build-framework/`. Repository engineering standards
are under `docs/engineering/`.
