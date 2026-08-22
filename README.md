# FamilyOS CLI

FamilyOS CLI provides the command-line and engineering validation surfaces for
the FamilyOS repository. The project currently supports a controlled Python
development environment and one provider-neutral validation command shared by
local development and GitHub Actions.

The repository provides a canonical package-build command. A successful command
includes static structural, metadata, and content-inventory validation of its
discovered Python package candidates. An explicit option additionally validates
the wheel through clean-environment installation and installed import/CLI smoke
checks. Neither result establishes artifact integrity, trust, provenance,
release readiness, or publication.

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

The command delegates packaging to the pypa/build frontend declared in the
repository's development dependency extra and the backend declared by
`pyproject.toml`. With no distribution flags, pypa/build first emits the source
distribution and then builds the wheel from that exact archive. Its default
operational output directory is `dist/`. A different explicit directory may be
supplied when isolation is needed:

```bash
familyos build --output-dir /tmp/familyos-package-build
```

The adapter passes the absolute repository `requirements.txt` path to
pypa/build as a dependency constraints file. The same constraints therefore
govern versions requested in the isolated sdist environment and the separate
isolated wheel-from-sdist environment. Constraints restrict requested package
versions; they neither install every locked package nor act as an allowlist.
A backend dependency absent from the file may still resolve normally, and
network access or an available cache may still be required. Build isolation and
the build-through-sdist sequence remain enabled.

Wheel functional validation is deliberately opt-in because creating a fresh
virtual environment and installing runtime dependencies is materially heavier
than static archive inspection:

```bash
familyos build --output-dir /tmp/familyos-package-build \
  --functional-validation
```

The option runs only after successful Artifact Discovery and static package
validation. It installs the exact discovered wheel into a fresh temporary venv,
imports `familyos_cli.main` with the venv interpreter, verifies that the module
resolved inside that venv rather than the checkout, and runs the installed
`familyos --help` entry point. The temporary environment and its external
working directory are removed deterministically.

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
    != statically valid artifact
    != functionally valid wheel
    != integrity-verified artifact
    != trusted artifact
    != release-ready artifact
```

Static `VALID` means only that a discovered candidate satisfies the implemented
archive, metadata, and content contract. Successful canonical execution also
proves that pypa/build rebuilt the wheel from the emitted source distribution.
Functional `VALID`, when explicitly requested, additionally means that this
derived wheel installed and its canonical import and console entry point
executed in the clean temporary environment. These results do not prove byte-
for-byte reproducibility, verify `RECORD` hashes, establish provenance, or
authorize release use.

A packaging, execution, discovery, static-validation, or requested functional-
validation failure returns a non-zero status and a concise diagnostic.
Diagnostics identify the candidate and failed contract or functional stage.
The command never publishes its outputs.
Temporary and intermediate output classification, Build ID association,
Artifact Identity, Artifact Integrity, Build Evidence, and release handoff
remain future work.

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

CI continues to invoke the default static command and does not opt into wheel
functional validation in this slice. Local functional capability evidence is
therefore distinct from future remote CI execution evidence.

This path was first remotely verified by successful GitHub Actions run
`31792439104` for commit `63693e6`, before structural validation existed;
those historical outputs remain unvalidated, untrusted package candidates.
Structural validation itself was remotely verified by successful run
`31801029251` for commit `c49c655`, again containing exactly one wheel and one
source distribution. Candidates remain untrusted and non-integrity-verified;
remote transport alone does not establish Artifact Integrity or release
readiness. That historical run does not prove the newer clean-environment wheel
installation/import/CLI capability and is not used as the local source-
distribution rebuildability regression evidence.

To reproduce the full CI path locally:

```bash
python -m pip install -r requirements.txt
python -m pip install --no-deps --no-build-isolation -e .
familyos validation ci
familyos build --output-dir dist
```

To exercise the additional local wheel capability, run
`familyos build --output-dir dist --functional-validation` separately. That
command is not part of the current remote CI evidence.

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

The virtual environment, tool caches, package-build outputs, and generated
packaging metadata are local derived state. They are not authoritative source
and may be removed when a clean local environment or package build is needed.

With the environment deactivated, the known derived state can be removed with:

```bash
deactivate
rm -rf .venv
rm -rf dist build
find . -path ./.git -prune -o -type d \( \
  -name .pytest_cache -o \
  -name .ruff_cache -o \
  -name .mypy_cache -o \
  -name "*.egg-info" \
  \) -exec rm -rf {} +
```

Root `dist/` and root `build/` are canonical generated package-output
locations and are ignored by Git. Generated `*.egg-info/` metadata and the
three listed tool-cache directory names are also ignored derived state and may
appear below repository subdirectories.

The cleanup procedure deliberately targets only these explicitly identified
derived paths. It must not be generalized to arbitrary repository directories,
tracked generated derivatives, source files, configuration, dependency
definitions, or other authoritative state.

After cleanup, the environment and package outputs can be reconstructed from
the committed repository inputs through the documented controlled bootstrap,
canonical validation, and canonical package-build commands. Correct build
behavior must not depend on the removed caches or historical generated output.

FamilyOS does not currently expose a dedicated `familyos clean` command; the
documented shell procedure is the canonical local developer cleanup procedure
for the implemented derived state.

## Current build boundary

FamilyOS exposes canonical package-build execution, explicit candidate
discovery, and application-owned static Python package validation covering
archive structure, emitted runtime/dependency metadata, and package-content
inventory. Canonical pypa/build execution builds the wheel from the emitted
source distribution, establishing source-distribution rebuildability. Its two
isolated backend environments constrain requested dependency versions through
the committed dependency state. The same build use case can explicitly add
clean-environment wheel installation, installed import-path validation, and
installed CLI smoke. It also exposes Artifact Identity, Artifact Integrity, and
machine-readable Build Evidence for successful canonical package builds. It
does not expose release handoff or a dedicated build-output cleanup command;
implemented derived state is cleaned through the documented local developer
procedure. Do not infer offline capability, byte reproducibility, trust,
provenance, release authority, or publication semantics from a successful
build command.

The normative Build Framework is under
`docs/epics/EPIC-BLD-001-build-framework/`. Repository engineering standards
are under `docs/engineering/`.
