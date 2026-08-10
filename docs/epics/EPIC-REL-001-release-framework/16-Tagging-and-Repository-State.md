# Release Framework

# 16 Tagging and Repository State

## Overview

EPIC-REL-001 — Release Framework defines the rules governing repository state and release tagging for FamilyOS.

The Git repository is one of the primary sources of release identity and historical traceability.

A release tag is therefore not merely a convenient label.

It is an official repository anchor that binds a release version to an exact source state.

The Tagging and Repository State model establishes the relationship between:

* working tree;
* branch;
* HEAD;
* source revision;
* authoritative remote;
* release version;
* release candidate;
* official release tag;
* release publication;
* historical reconstruction.

The objective is to ensure that every official FamilyOS Git-based release can be traced to a precise and controlled repository state.

---

# Purpose

This document establishes:

* repository state requirements;
* working tree expectations;
* branch and HEAD relationships;
* remote synchronization;
* release commit identity;
* tag semantics;
* tag naming;
* annotated tags;
* tag immutability;
* tag verification;
* tag conflict handling;
* candidate tags;
* stable tags;
* remote publication;
* repository release evidence;
* repository recovery expectations.

The model prevents ambiguous releases caused by incorrect or uncontrolled repository state.

---

# Core Principle

The central principle is:

> An official release tag must identify the exact repository state that was qualified for release.

The following model is valid:

```text id="b3f7cc"
validated source revision
      ↓
approved release
      ↓
official tag
      ↓
remote verification
```

The following model is not sufficient:

```text id="ztxd5k"
work seems finished
      ↓
git tag
      ↓
hope it is correct
```

---

# Repository as Release Anchor

For Git-based FamilyOS releases, the repository provides a durable mapping between:

```text id="27mtqj"
release version
      ↓
release tag
      ↓
commit
      ↓
source tree
```

This mapping is foundational to historical release reconstruction.

---

# Repository State Model

The release-relevant repository state includes:

```text id="lv9xki"
Repository
├── current branch
├── HEAD
├── working tree
├── index
├── local references
├── remote tracking state
├── release tag namespace
└── authoritative remote
```

Not every element requires identical treatment for every release profile.

The relevant assumptions must remain explicit.

---

# Working Tree State

A stable release SHOULD normally originate from a clean working tree.

A clean working tree means no unintended:

* modified tracked files;
* staged but uncommitted changes;
* untracked release-relevant files;
* unresolved merge state.

A typical verification is:

```text id="fghmqq"
git status --short
```

For a clean state, the expected output is empty.

---

# Why Clean Working Tree Matters

A dirty working tree creates ambiguity between:

```text id="strtl3"
committed source
```

and:

```text id="9hh3ac"
actual local filesystem state
```

If release artifacts are produced from uncommitted changes, the official Git commit may not represent what was actually released.

This breaks source-to-release traceability.

---

# Generated Files

Generated build artifacts do not necessarily invalidate repository cleanliness if they are intentionally excluded from source control.

However, release tooling must distinguish expected generated output from accidental source modifications.

Generated files that alter tracked release source unexpectedly should block release qualification.

---

# Staged Changes

A staged but uncommitted change is still not part of a stable source revision.

For release identity purposes:

```text id="32di07"
git index
!=
official commit
```

The release process should require release-relevant changes to be committed before final tagging.

---

# HEAD

`HEAD` identifies the currently checked-out source revision.

For a release, the expected relationship is:

```text id="etab3g"
HEAD
=
approved release commit
```

before official tag creation.

The exact commit should be recorded as release evidence.

---

# Release Commit

The Release Commit is the Git commit representing the source state associated with the official release.

It should contain all release-relevant committed content required by the applicable profile.

For a framework release, this may include:

* numbered framework documents;
* EPIC metadata;
* changelog updates;
* validation state;
* release documentation;
* revision history.

---

# Release Commit Immutability

Git commit identity is content-addressed and should remain a stable release anchor.

The release process must record the full or sufficient unambiguous commit identifier.

Example:

```text id="q4pvcq"
Release Commit:
1b457dd...
```

---

# Branch Context

A release may originate from:

* main branch;
* feature branch;
* release branch;
* maintenance branch;
* other governed lineage.

The Release Framework does not mandate one branching strategy.

However, the intended release lineage must be understood.

---

# Current Branch

Before release, tooling SHOULD verify the expected branch where branch policy applies.

Example:

```text id="g22r7u"
feature/foundation-engineering-docs
```

may be the authorized source branch for a framework release.

A release accidentally performed from an unrelated branch should block.

---

# Branch Is Not Release Identity

A branch is mutable.

Therefore:

```text id="2qgekr"
branch name
```

must not be treated as sufficient historical release identity.

The durable release relationship is:

```text id="348ri3"
tag
→ commit
```

not:

```text id="oi7d60"
tag
→ branch name only
```

---

# Branch Synchronization

Where repository governance requires synchronization with an authoritative remote, the release process should verify that the intended release commit exists remotely.

Conceptually:

```text id="4tp0ls"
local release commit
=
remote branch release commit
```

before final release completion.

---

# Local vs Remote State

A local repository may contain valid work that does not yet exist in the authoritative remote.

For example:

```text id="il0c5p"
local HEAD:
abc123

origin/branch:
def456
```

This state means the release commit has not yet been fully shared or published.

Release completion must distinguish local validity from authoritative remote publication.

---

# Authoritative Remote

Repository governance should define the authoritative release remote.

For current FamilyOS workflows, this is typically the canonical `origin`.

The framework must not assume the remote name itself is universally significant.

The important concept is:

```text id="oj3twy"
authoritative remote
```

---

# Remote Verification

Before or after publication, the release process may verify remote state using commands such as:

```text id="9u04er"
git fetch origin
```

and reference comparisons.

The exact command sequence is implementation-specific.

The required outcome is explicit agreement between expected release state and authoritative repository state.

---

# Release Tag Definition

A Release Tag is an official Git reference identifying the repository commit associated with a release.

A release tag must communicate:

* release version;
* release subject where applicable;
* repository state;
* historical release identity.

---

# Tag Naming Strategy

FamilyOS framework releases may use the canonical pattern:

```text id="km3hnp"
v<version>-<release-subject>
```

Examples:

```text id="7uaofn"
v4.7.0-build-framework
v4.8.0-release-framework
v4.9.0-plugin-framework
```

The numeric portion follows `06-Versioning-Strategy.md`.

The suffix identifies the release subject.

---

# Tag Name Components

A tag name may contain:

```text id="nohm5k"
v
+
semantic version
+
release subject
```

Example:

```text id="14fke5"
v4.8.0-release-framework
```

where:

```text id="r9tqv4"
version = 4.8.0
subject = release-framework
```

---

# Tag Naming Requirements

Official tag names MUST be:

* deterministic;
* unambiguous;
* valid Git references;
* unique;
* consistent with release version;
* consistent with repository conventions.

Ad hoc names such as:

```text id="3ikgta"
final
final2
release-good
latest-working
```

are prohibited for official release identity.

---

# Annotated Tags

FamilyOS SHOULD use annotated Git tags for official framework and significant platform releases.

Example:

```text id="xk8sy4"
git tag -a v4.8.0-release-framework \
  -m "EPIC-REL-001 Release Framework completed"
```

Annotated tags can preserve:

* tag identity;
* tagger;
* timestamp;
* message.

They provide stronger release semantics than lightweight tags.

---

# Lightweight Tags

Lightweight tags MAY be used for internal or temporary workflows where policy permits.

They SHOULD NOT normally be preferred for significant official FamilyOS release milestones.

---

# Tag Message

The annotated tag message should clearly identify the release.

Example:

```text id="ytxr67"
EPIC-REL-001 Release Framework completed
```

Tag messages should be concise and factual.

They are not substitutes for release notes.

---

# Tag Creation Preconditions

Before creating an official release tag, the release process SHOULD verify:

```text id="0b3wg7"
candidate validated
release approved
final version confirmed
release commit confirmed
working tree acceptable
branch acceptable
tag name valid
tag absent
```

Tag creation should occur only after these conditions are satisfied.

---

# Tag Availability

Before creation, tooling must determine whether the intended tag already exists.

Example:

```text id="4cs5ea"
v4.8.0-release-framework
```

If absent, creation may proceed.

If present, its target must be examined.

---

# Existing Matching Tag

If the intended tag already exists and points to the expected release commit, automation may treat the tag operation as idempotently complete.

Conceptually:

```text id="cfwzrr"
tag exists
+
target commit correct
=
verify and continue
```

---

# Existing Conflicting Tag

If the intended tag exists but points to a different commit:

```text id="cb2tw7"
expected:
abc123

actual:
def456
```

the release MUST block.

The tag must not be force-moved automatically.

This indicates release identity conflict.

---

# Tag Immutability

Official release tags SHOULD be treated as immutable after publication.

Once a tag identifies an official release:

```text id="vwiplf"
v4.8.0-release-framework
→ abc123
```

it should remain anchored to `abc123`.

The tag should not later become:

```text id="wrr8s4"
v4.8.0-release-framework
→ def456
```

---

# Tag Movement

Moving an official published release tag is prohibited except under extraordinary governed repair conditions.

Such cases must be treated as release integrity incidents.

Normal corrections require a new release version and new tag.

---

# Tag Deletion

Deleting an official release tag can break historical references.

Tag deletion should therefore require explicit governance.

If a defective release must be withdrawn, withdrawal metadata is generally preferable to erasing the release tag.

---

# Candidate Tags

Release Candidate tags MAY use a pre-release version.

Examples:

```text id="jbiwqh"
v5.2.0-rc.1
v5.2.0-rc.2
```

Candidate tag usage is optional unless the release profile requires it.

---

# Candidate Tag Stability

Where candidate tags are used as validation anchors, they should be treated as immutable.

A changed candidate should receive:

```text id="rl0avb"
rc.2
```

instead of moving:

```text id="wbfxar"
rc.1
```

---

# Stable Tags

Stable release tags identify final official releases.

They should represent:

* validated release content;
* approved release identity;
* official source revision;
* intended version.

Stable tags receive the strongest immutability expectations.

---

# Tag and Candidate Relationship

The release record should allow the relationship:

```text id="hbzvhg"
5.2.0-rc.3
      ↓
final candidate
      ↓
5.2.0
      ↓
v5.2.0
```

or the FamilyOS subject-specific tag equivalent.

---

# Tag and Version Consistency

The version embedded in the tag must match the official release version.

Invalid:

```text id="ukyc14"
Release Version:
4.8.0

Tag:
v4.9.0-release-framework
```

Valid:

```text id="f8aqct"
Release Version:
4.8.0

Tag:
v4.8.0-release-framework
```

---

# Tag and Changelog Consistency

The release version represented by the tag must align with:

* changelog;
* release notes;
* EPIC metadata;
* release manifest;
* artifact metadata where applicable.

Version inconsistency must block release completion.

---

# Tag and Release Commit

Before creation, the tag target should be explicit.

For example:

```text id="6qjqwh"
git tag -a <tag> <commit> -m "<message>"
```

Even when tagging `HEAD`, tooling should know the exact resulting commit.

---

# Explicit Commit Tagging

For higher assurance, explicit commit targeting may be preferable:

```text id="nuzcij"
git tag -a v4.8.0-release-framework abc123 \
  -m "EPIC-REL-001 Release Framework completed"
```

This reduces ambiguity about what is being tagged.

---

# Local Tag Creation

Creating a tag locally establishes a local release anchor.

It does not yet prove publication to the authoritative repository.

The lifecycle must distinguish:

```text id="j9aiy3"
tag created locally
```

from:

```text id="26sx7y"
tag published remotely
```

---

# Tag Publication

Publishing an official tag may use:

```text id="1hieqn"
git push origin v4.8.0-release-framework
```

or an equivalent controlled mechanism.

Tag publication creates an externally visible release reference.

---

# Branch Publication

The release branch or commit may also need to be pushed before or with the tag.

A common safe sequence is:

```text id="a8qaxw"
commit release state
      ↓
push branch
      ↓
verify remote commit
      ↓
push release tag
      ↓
verify remote tag
```

The exact order may be profile-specific.

---

# Branch Before Tag

Publishing the branch before the tag may make release history easier to inspect because the tagged commit is already available on the authoritative branch.

This is a useful default for current FamilyOS framework releases.

---

# Tag Before Branch Risk

A tag may technically publish a commit not yet reachable through the expected remote branch.

While Git permits this, it may create confusion if repository policy expects the branch to represent the release lineage.

The workflow must follow explicit repository governance.

---

# Remote Tag Verification

After tag publication, the release workflow should verify:

```text id="kxbyj0"
remote tag exists
```

and:

```text id="o7pwua"
remote tag target
=
expected release commit
```

Successful `git push` output alone is weaker than direct state verification.

---

# Local and Remote Tag Agreement

The expected final relationship is:

```text id="nv87vr"
local tag
=
remote tag
=
release commit
```

---

# HEAD and Remote Branch Agreement

For release profiles requiring synchronized branch state:

```text id="1b3n9m"
HEAD
=
origin/<release-branch>
```

after publication.

This is the state FamilyOS has already been checking manually for framework releases.

---

# Release Repository State

A completed Git-based release may therefore require:

```text id="1lk06u"
Working Tree          CLEAN
HEAD                  expected commit
Remote Branch         expected commit
Release Tag           expected commit
Remote Release Tag    expected commit
Version               consistent
```

---

# Repository State Evidence

Release evidence may capture:

```text id="3doyec"
repository
branch
HEAD
remote branch
working tree status
tag
tag target
remote tag target
```

This makes release state reconstructable.

---

# Framework Release Example

A completed framework release may look like:

```text id="a7z8jh"
Release:
EPIC-BLD-001 — Build Framework

Version:
4.7.0

Branch:
feature/foundation-engineering-docs

HEAD:
1b457dd

Remote Branch:
1b457dd

Tag:
v4.7.0-build-framework

Tag Target:
1b457dd

Working Tree:
clean
```

This is the exact type of repository state EPIC-REL-001 is intended to formalize.

---

# Repository Release Gate

The transition:

```text id="4srq5c"
APPROVED
   ↓
RELEASED
```

is protected by repository and release identity checks.

A conceptual gate is:

```text id="vab56c"
Approval             PASS
Version              PASS
Release Commit       VERIFIED
Working Tree         PASS
Branch               PASS
Remote State         PASS
Tag Availability     PASS
--------------------------------
RELEASE IDENTITY     READY
```

---

# Release Commit Timing

The final release commit should contain the release state required by the release profile.

For framework releases, this normally means finalizing documents such as:

* `CHANGELOG.md`;
* `VALIDATION.md`;
* `Revision-History.md`;
* `30-Release.md`;
* `31-Implementation-Checklist.md`.

Tagging should occur after this final committed state exists.

---

# Release Commit Message

Commit messages should clearly communicate release preparation or completion according to repository conventions.

Example:

```text id="3p773y"
docs(release): complete EPIC-REL-001 release framework
```

or another repository-compliant format.

This document does not define the full commit message convention.

---

# Release Tag Timing

The official stable tag should be created after:

```text id="ljc2q5"
final release content committed
validation completed
release approved
repository state verified
```

Creating it earlier weakens the meaning of the tag.

---

# Release Tag as State Transition

The official tag should be treated as part of the transition to `RELEASED`.

Conceptually:

```text id="cexymt"
APPROVED
   ↓
official release version
   ↓
official repository tag
   ↓
RELEASED
```

---

# Tag Is Not Publication Completion

A tag may be created and pushed while later publication steps fail.

Therefore:

```text id="3s2oyi"
tag exists
```

does not necessarily mean:

```text id="za2q11"
release COMPLETED
```

The full Release Lifecycle remains authoritative.

---

# Tag Is Not Release Approval

Similarly, the ability to create a Git tag is not equivalent to governance approval.

Repository permissions and release authority must remain distinct concepts.

---

# Repository Permissions

The ability to:

* push commits;
* create tags;
* delete tags;
* modify protected branches;

should follow least-privilege and governance principles.

Official release tag creation may require stronger authority than normal development pushes.

---

# Protected Tags

Where supported, official tag patterns SHOULD be protected.

Example protected namespace:

```text id="5us9ou"
v*
```

or more specific official release patterns.

Protection design must avoid blocking legitimate internal candidate workflows unnecessarily.

---

# Signed Tags

Future FamilyOS releases MAY use cryptographically signed tags.

Signed tags can strengthen evidence that an authorized signing identity created the release anchor.

Signing policy must define:

* key ownership;
* verification;
* rotation;
* revocation;
* incident handling.

Signed tags are not required by the initial framework.

---

# Signed Commit Relationship

Future high-assurance release policies MAY also require signed release commits.

This is a separate control from signed tags.

The framework supports stronger source identity controls without requiring them immediately.

---

# Tag Verification by Consumers

Consumers or automation may verify:

* tag existence;
* tag target;
* tag signature where applicable;
* release version;
* source integrity.

This helps establish end-to-end release trust.

---

# Tag Namespace

Repository governance should avoid conflicting tag namespaces.

For example, FamilyOS may distinguish:

```text id="sok3e7"
stable framework tags
candidate tags
component tags
```

through naming rules.

Namespaces must remain understandable and predictable.

---

# Component Tags

Independently versioned components may use subject-specific tags.

Examples:

```text id="wna9fe"
v3.1.0-finance-plugin
v4.0.0-security-plugin
```

The tag must clearly identify both version and release subject.

---

# Platform Tags

Platform-wide releases may use simpler primary tags where appropriate.

Example:

```text id="djmaxp"
v5.0.0
```

if repository governance defines this as the authoritative platform release tag.

---

# Framework Tags

Engineering framework milestones may continue using:

```text id="nhapfg"
v<version>-<framework>
```

This provides clear historical meaning when several framework milestones share one repository.

---

# Tag Ordering

Tag ordering must use semantic version parsing rather than arbitrary lexical order when determining version history.

Example:

```text id="aj4xjj"
v4.10.0
```

must correctly compare as later than:

```text id="8g74t7"
v4.9.0
```

---

# Tag Discovery

Automation should be able to identify official tags according to known naming rules.

This supports:

* previous version detection;
* release history;
* version validation;
* changelog comparison.

---

# Tag Filtering

Not every Git tag may represent an official stable release.

Automation may need to distinguish:

```text id="8vby6q"
candidate tags
experimental tags
official release tags
```

The naming strategy must make this possible.

---

# Repository History Integrity

Release history depends on preserving Git history.

Practices such as rewriting already-published release commits can undermine release traceability.

Protected release branches and tags reduce this risk.

---

# Force Push Risk

Force-pushing history containing official release commits may detach expected branch lineage from existing release history.

Repository governance SHOULD restrict force pushes on release-relevant protected branches.

---

# Commit Reachability

A historical tag preserves access to its commit even if branch structure later changes.

However, release governance should avoid unnecessary history rewriting because it complicates operational understanding.

---

# Repository Migration

If FamilyOS moves to a different authoritative repository or hosting provider, release tags and commit history should be preserved.

Migration must maintain:

```text id="3sq8sa"
release tag
→ release commit
```

relationships.

---

# Remote Renaming

The local remote name may change.

For example:

```text id="gikmvo"
origin
```

could become another name.

Release semantics must remain tied to the authoritative remote concept rather than a hard-coded local alias.

---

# Repository Mirroring

If multiple remotes or mirrors exist, governance must define which repository state is authoritative.

Mirrors should preserve:

* commits;
* official tags;
* tag targets.

A mirror must not create divergent release identity.

---

# Repository Failure

If repository publication fails after local tag creation:

```text id="vft25l"
local tag      CREATED
remote tag     FAILED
```

the release enters an incomplete state.

Recovery should verify existing remote state before retrying.

---

# Branch Push Failure

Example:

```text id="a6gq3g"
release commit created
branch push failed
tag not pushed
```

The release remains unpublished.

Retry may be safe after verifying local state.

---

# Tag Push Failure

Example:

```text id="az5uem"
branch push succeeded
tag push failed
```

Recovery should:

* verify remote branch;
* verify tag absence or presence;
* retry tag publication safely.

---

# Partial Remote Success

Network failures may make client output ambiguous.

For example, a push command may time out after the remote accepted the update.

Recovery MUST inspect remote state before repeating potentially conflicting operations.

---

# Repository Recovery Principle

The governing rule is:

> Inspect actual repository state before retrying repository side effects.

Never assume that a failed command means no state change occurred.

---

# Wrong Tag Recovery

If an incorrect tag is created locally but not published, it may be corrected under local release procedure.

If the tag has already been published, correction becomes a governed release integrity issue.

---

# Published Wrong Tag

A published tag pointing to the wrong commit should not be force-moved casually.

Possible responses include:

* stop release progression;
* investigate consumer exposure;
* apply governance;
* create corrected release identity;
* document incident.

---

# Wrong Version Tag

If an incorrect version tag is published, the release process must not silently reuse or overwrite it.

A new valid release version may be required depending on exposure and policy.

---

# Repository Dry Run

Release tooling SHOULD support repository preflight checks without creating tags.

Example:

```text id="jm16rp"
Release Repository Preflight

Branch               PASS
HEAD                 abc123
Working Tree         CLEAN
Remote Branch        SYNCED
Version              4.8.0
Tag                  AVAILABLE

READY FOR TAGGING
```

---

# Repository Validation Automation

Deterministic repository checks are strong candidates for automation.

Potential checks include:

* clean working tree;
* expected branch;
* HEAD resolution;
* remote synchronization;
* release commit existence;
* tag availability;
* tag target;
* semantic version extraction.

---

# Repository Validation Must Fail Closed

If the release tool cannot determine repository state reliably, it should block rather than guess.

Examples include:

* remote unavailable;
* ambiguous tag conflict;
* unresolved merge;
* detached state not permitted by profile;
* inconsistent release metadata.

---

# Detached HEAD

A detached `HEAD` is not inherently invalid.

CI/CD often uses detached checkouts.

However, the release profile must understand and allow it.

The exact commit remains the authoritative source identity.

---

# Shallow Clones

Shallow CI clones may lack enough history for:

* previous tag detection;
* semantic version comparison;
* changelog generation.

Release pipelines should fetch sufficient history for required release checks.

---

# Submodules

If FamilyOS ever uses Git submodules, release repository state must include exact submodule revisions.

A release commit alone may not fully describe external source state unless submodule references are preserved.

---

# Multiple Repositories

Future platform releases may aggregate several repositories.

In such cases, the release manifest may need to capture:

```text id="qgh4mk"
core repository commit
plugin repository commit
documentation repository commit
```

The same traceability principles apply.

---

# Repository Evidence Record

A future structured record may resemble:

```text id="vtf6qr"
repository:
  branch: feature/foundation-engineering-docs
  commit: abc123
  working_tree: clean

remote:
  name: origin
  commit: abc123

release:
  version: 4.8.0
  tag: v4.8.0-release-framework
  tag_commit: abc123
```

This is illustrative.

---

# Repository Completion Check

A completed framework release should eventually verify:

```text id="bquugx"
HEAD                    expected commit
remote branch           expected commit
local tag               expected commit
remote tag              expected commit
working tree            clean
version                 consistent
```

---

# Current FamilyOS Release Pattern

The current practical FamilyOS framework release pattern already approximates:

```text id="czdlup"
finish framework
      ↓
validate
      ↓
commit
      ↓
verify HEAD
      ↓
push branch
      ↓
create annotated tag
      ↓
push tag
      ↓
verify HEAD / remote / tag
      ↓
working tree clean
```

EPIC-REL-001 converts this operational discipline into explicit framework rules.

---

# Recommended Framework Release Sequence

For FamilyOS framework releases, the default sequence SHOULD be:

```text id="5m45im"
1. Complete release documents.
2. Run framework validation.
3. Verify intended version.
4. Verify Git status.
5. Commit final release state.
6. Record release commit.
7. Push release branch.
8. Verify remote branch commit.
9. Create annotated official tag on release commit.
10. Push official tag.
11. Verify remote tag target.
12. Verify working tree remains clean.
13. Record final release evidence.
```

Governance may refine this sequence.

---

# Alternative Tag-Before-Branch Sequence

Other repository models may safely use a different ordering.

The Release Framework does not prohibit them.

The invariant is that final remote release state must be unambiguous and verified.

---

# Repository State and Release Lifecycle

Repository state interacts with several lifecycle stages.

```text id="72mgwx"
PREPARED
repository understood

CANDIDATE
source commit fixed

VALIDATED
candidate source verified

APPROVED
release commit authorized

RELEASED
official tag established

PUBLISHED
tag available on authoritative remote

COMPLETED
final repository state verified
```

---

# Repository State and Release Candidates

`10-Release-Candidates.md` requires a candidate to map to an exact source revision.

This document defines how that source revision is represented and later anchored through official tags.

---

# Repository State and Versioning

`06-Versioning-Strategy.md` defines release version semantics.

This document maps the version into repository tag identity.

---

# Repository State and Release Automation

`13-Release-Automation.md` defines idempotent and safe execution.

Repository tagging must follow those automation rules.

---

# Repository State and CI/CD

`14-CI-CD-Integration.md` defines trusted pipeline execution.

CI/CD release jobs must verify exact commit and tag state before privileged publication.

---

# Repository State and Publishing

`17-Publishing-and-Distribution.md` treats remote tag publication as one possible official release publication action.

---

# Repository State and Security

`19-Release-Security.md` governs protection of:

* release branches;
* tags;
* credentials;
* repository authority;
* signing where applicable.

---

# Repository State and Observability

`20-Release-Observability.md` defines how release repository transitions and failures become visible and auditable.

---

# Repository State and Governance

`21-Release-Governance.md` defines who may:

* approve release source;
* create official tags;
* publish tags;
* delete or repair release references.

---

# Tagging Invariants

The following invariants apply.

## TAG1 — Every official Git-based release tag identifies one exact commit.

## TAG2 — The tag version matches the official release version.

## TAG3 — Official tag names are unique.

## TAG4 — Published official tags are treated as immutable.

## TAG5 — Tag creation follows applicable validation and approval.

## TAG6 — Existing conflicting tags block release progression.

## TAG7 — Remote tag publication is verified.

## TAG8 — Tag presence alone does not imply release completion.

## TAG9 — Candidate tags, when used as validation anchors, remain stable.

## TAG10 — Tag repair requires governance when published history is affected.

---

# Repository State Invariants

## RS1 — The release source revision is explicitly identifiable.

## RS2 — Release-relevant working tree ambiguity is eliminated before final release.

## RS3 — The release commit represents the committed release state.

## RS4 — Authoritative remote state is explicitly verified where required.

## RS5 — Branch references never replace commit identity.

## RS6 — Repository state conflicts block release progression.

## RS7 — Release history must remain reconstructable from tags and commits.

## RS8 — Retry operations inspect actual remote state.

## RS9 — Protected repository history must not be rewritten casually.

## RS10 — Repository semantics remain independent from hosting provider.

---

# Tagging Anti-Patterns

## Tag Current Whatever

Creating a tag without verifying which commit is currently checked out.

---

## Tag Before Validation

Creating a final official tag before candidate qualification is complete.

---

## Force-Move Release Tag

Updating a published official tag to point to a new commit.

---

## Reuse Version Tag

Publishing different release content under an existing tag name.

---

## Tag Equals Approval

Assuming a tag is legitimate merely because someone had technical permission to create it.

---

## Push Without Verification

Assuming a successful push message proves the final remote state.

---

# Repository Anti-Patterns

## Dirty Release

Producing release content from uncommitted changes.

---

## Branch as Identity

Recording only a mutable branch name without commit identity.

---

## Local-Only Release

Treating a locally committed and tagged state as an official shared release.

---

## Blind Retry

Repeating pushes or tag operations after network failure without verifying remote state.

---

## Release from Unexpected Branch

Tagging an approved version from an unrelated or unauthorized source lineage.

---

## History Rewrite

Force-pushing release history after official tags are published without governed migration.

---

# Minimum Repository Release Requirements

At minimum, a FamilyOS Git-based official release should verify:

```text id="mv1l7a"
release commit known
working tree acceptable
version valid
tag name valid
tag unique
tag target correct
remote publication successful
remote tag verified
```

---

# Framework Release Minimum

For current FamilyOS framework releases, the minimum should normally include:

```text id="fg2vm7"
git status clean
HEAD recorded
branch recorded
remote branch synchronized
annotated release tag created
tag points to HEAD
branch pushed
tag pushed
remote tag verified
```

---

# Target Repository Experience

At higher maturity, the release tooling should produce:

```text id="zlru4r"
FamilyOS Repository Release State

Repository            FamilyOS
Branch                feature/foundation-engineering-docs
Working Tree          CLEAN

Release Commit        2f84abc
Remote Branch         2f84abc
Synchronization       PASS

Version               4.8.0
Tag                   v4.8.0-release-framework
Local Tag Target      2f84abc
Remote Tag Target     2f84abc

Tag Integrity         PASS
Repository State      VERIFIED
```

---

# Historical Reconstruction

Years after publication, maintainers should be able to start from:

```text id="9ixbdg"
v4.8.0-release-framework
```

and determine:

```text id="5iktum"
tag
→ exact commit
→ exact repository tree
→ release documentation
→ release history
```

This is one of the primary reasons official tag integrity matters.

---

# Final Statement

The FamilyOS Tagging and Repository State model establishes Git repository state as a formal part of release engineering.

It ensures that official release versions are anchored to exact source revisions, that working tree and branch assumptions remain controlled, that authoritative remote state is verified, and that release tags serve as stable historical references rather than mutable labels.

By formalizing the relationship between `HEAD`, branch, remote state, release commit, version, annotated tag, and final verification, FamilyOS turns its existing disciplined Git release practices into a reproducible and governable release architecture.
