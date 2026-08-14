# FamilyOS CLI

FamilyOS CLI provides the command-line and engineering validation surfaces for
the FamilyOS repository. The project currently supports a controlled Python
development environment and one provider-neutral validation command shared by
local development and GitHub Actions.

The repository provides a canonical package-build command. A successful command
includes static structural, metadata, and content-inventory validation of its
discovered Python package candidates. Static validity does not establish
artifact integrity, trust, provenance, release readiness, or publication.

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

## Canonical package build

Build the FamilyOS wheel and source distribution with the repository-owned
interface:

```bash
familyos build
```

The command delegates packaging to the standard Python build frontend and the
backend declared by `pyproject.toml`. Its default operational output directory
is `dist/`. A different explicit directory may be supplied when isolation is
needed:

```bash
familyos build --output-dir /tmp/familyos-package-build
```

Root `dist/` and root `build/` are generated package-build outputs and are
ignored by Git. They are not authoritative source and must not be committed.

A successful command requires exactly one current wheel and exactly one current
source distribution in the resolved output directory. It classifies those two
outputs as candidates and fails if either is missing, duplicated, or accompanied
by another current output. After successful discovery, the application inspects
and decompresses those exact ZIP and gzip-compressed tar candidates through
bounded in-memory streams without filesystem extraction. It validates safe
coherent archive structure, required standard package metadata, package
name/version/runtime/dependency metadata consistency with `pyproject.toml`, and
an exact expected-versus-actual inventory. Python module authority comes from
the configured setuptools package discovery and source tree; non-code resource
intent comes independently from source files matching the configured setuptools
package-data policy. Required content must be present in both formats, and
unintended package or source-distribution content fails validation.

The states remain deliberately distinct:

```text
candidate artifact
    != structurally valid artifact
    != integrity-verified artifact
    != trusted artifact
    != release-ready artifact
```

`VALID` means only that a discovered candidate satisfies the implemented static
Python package validation contract. It does not verify `RECORD` hashes, install
either package, run imports or the CLI, establish provenance, or authorize
release use.

A packaging, execution, discovery, or structural-validation failure returns a
non-zero status and a concise diagnostic. Structural diagnostics identify the
candidate and failed contract. The command never publishes its outputs.
Temporary and intermediate output classification, Build ID association,
Artifact Identity, Artifact Integrity, functional package validation, Build
Evidence, and release handoff remain future work.

## CI package build

The `Canonical CI Validation` GitHub Actions workflow also runs
`familyos build --output-dir dist` after canonical validation succeeds, and
uploads the resulting `dist/` directory as the `familyos-package-candidates`
workflow artifact when the build succeeds. Because structural validation is
part of the canonical command, a local structural failure prevents upload
without duplicating validation logic in YAML. A failed mandatory validation
skips the build step entirely; a failed build, discovery, or structural
validation skips the candidate upload and fails the workflow. The workflow
transport does not establish Artifact Integrity, trust, release readiness, or
publication.

This path was first remotely verified by successful GitHub Actions run
`31792439104` for commit `63693e6`, before structural validation existed;
those historical outputs remain unvalidated, untrusted package candidates.
Structural validation itself was remotely verified by successful run
`31801029251` for commit `c49c655`, again containing exactly one wheel and one
source distribution. Candidates remain untrusted and non-integrity-verified;
remote transport alone does not establish Artifact Integrity or release
readiness, and the remaining functional Level 16 checks (clean-environment
installation, import/CLI smoke, source-distribution build/install validation)
remain future work.

To reproduce the full CI path locally:

```bash
python -m pip install -r requirements.txt
python -m pip install --no-deps --no-build-isolation -e .
familyos validation ci
familyos build --output-dir dist
```

Generated `*.egg-info/` metadata is excluded from repository authority and
configured as ignored state. Setuptools may regenerate it locally during
installation, dependency resolution, or package construction without dirtying
Git-tracked authority. Post-commit verification after hygiene commit `a85b5a7`
confirmed that editable installation, dependency freshness, canonical package
construction, and canonical validation leave tracked status clean.
`pyproject.toml` remains the canonical packaging metadata authority, while
`requirements.txt` remains the controlled resolved dependency state.

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
No canonical cleanup contract exists yet for candidate artifacts or other
future build outputs.

## Current build boundary

FamilyOS exposes canonical package-build execution, explicit candidate
discovery, and application-owned static Python package validation covering
archive structure, emitted runtime/dependency metadata, and package-content
inventory. It does not yet expose functional installation/runtime validation,
Artifact Identity, Artifact Integrity, Build Evidence, release handoff, or a
canonical build-output cleanup command. Those capabilities remain future
EPIC-BLD-001 implementation work. Do not infer integrity, trust, provenance, or
release semantics from a successful build command.

The normative Build Framework is under
`docs/epics/EPIC-BLD-001-build-framework/`. Repository engineering standards
are under `docs/engineering/`.
