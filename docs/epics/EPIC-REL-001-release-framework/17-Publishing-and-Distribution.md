# Release Framework

# 17 Publishing and Distribution

## Overview

EPIC-REL-001 — Release Framework defines Publishing and Distribution as distinct release engineering responsibilities.

Publishing makes an approved release available through one or more authoritative release targets.

Distribution makes that published release available to its intended consumers or channels.

These concepts are related but must not be treated as equivalent.

A release may be published but not yet distributed.

A release may also be partially published across several targets without being considered fully published.

The Publishing and Distribution model establishes:

* publication semantics;
* publication targets;
* publication sequencing;
* distribution semantics;
* channel promotion;
* artifact identity preservation;
* publication verification;
* partial failure handling;
* retry behavior;
* withdrawal;
* release availability;
* consumer exposure;
* release completion boundaries.

The objective is to ensure that FamilyOS releases become externally available through controlled, observable, and recoverable transitions.

---

# Purpose

This document establishes:

* publishing responsibilities;
* distribution responsibilities;
* authoritative publication targets;
* publication gates;
* publication transactions;
* multi-target publication;
* artifact upload rules;
* release metadata publication;
* channel promotion;
* distribution verification;
* publication evidence;
* failure and recovery semantics;
* withdrawal and supersession;
* idempotency expectations.

The goal is to prevent FamilyOS from treating an upload command or Git push as sufficient proof that a release has been successfully distributed.

---

# Core Principle

The central principle is:

> Publication and distribution are controlled state transitions, not individual commands.

For example:

```text id="c01x58"
git push tag
```

is an operation.

It may contribute to publication.

It does not by itself define successful release publication.

Similarly:

```text id="g2m1qt"
package uploaded
```

does not prove that:

```text id="ptzz9s"
the release is fully published,
verified,
and available through the intended channel
```

---

# Publishing vs Distribution

The distinction is:

```text id="kba7df"
PUBLISHING
makes an approved release authoritative and available
through official release targets

DISTRIBUTION
makes that published release available to the intended
consumer population or release channel
```

A simple release profile may combine these steps operationally.

Their semantics must remain distinguishable.

---

# Lifecycle Position

Publishing and Distribution primarily govern:

```text id="3zafmx"
APPROVED
   ↓
RELEASED
   ↓
PUBLISHED
   ↓
DISTRIBUTED
   ↓
COMPLETED
```

The exact lifecycle profile may compress some states.

The distinction remains important for failure handling.

---

# RELEASED State

`RELEASED` means the official release identity has been established.

For Git-based releases, this may include:

* final version;
* official release commit;
* official release tag.

The release may not yet be available through every authoritative publication target.

---

# PUBLISHED State

`PUBLISHED` means all mandatory publication targets for the applicable release profile have been successfully updated and verified.

Examples may include:

* authoritative Git tag published;
* repository release created;
* package registry version published;
* artifact archive published;
* release notes published;
* documentation published.

Publication requirements depend on release type.

---

# DISTRIBUTED State

`DISTRIBUTED` means the published release has been promoted or exposed to its intended consumer scope.

Distribution may include:

* stable channel update;
* maintenance channel update;
* plugin registry promotion;
* documentation activation;
* package index visibility;
* rollout to downstream environments.

Distribution may occur immediately after publication or through a later controlled transition.

---

# Publication Target

A Publication Target is an authoritative system receiving part of the official release.

Examples include:

```text id="6z9dle"
Git repository
Git hosting release
package registry
artifact registry
plugin registry
container registry
documentation hosting
object storage
```

A release profile must identify its mandatory publication targets.

---

# Authoritative Publication Target

An authoritative target is one whose state contributes to the official release definition.

For example:

```text id="fghj1e"
Git remote tag
```

may be authoritative for a framework release.

A package registry may be authoritative for a packaged CLI release.

A cache or temporary mirror is not automatically authoritative.

---

# Publication Target Registry

At higher maturity, FamilyOS should maintain explicit publication target definitions.

Conceptually:

```text id="gfoj0v"
framework-release:
  - git-remote

plugin-release:
  - git-remote
  - plugin-registry

platform-release:
  - git-remote
  - package-registry
  - documentation-host
```

The exact configuration format is implementation-specific.

---

# Publication Preconditions

Publication SHOULD only begin after applicable requirements are satisfied.

Typical preconditions include:

```text id="0fgs8d"
candidate validated
release approved
version finalized
release identity established
artifacts verified
release notes ready
publication targets known
credentials available
recovery strategy understood
```

Failure of mandatory preconditions must block publication.

---

# Publication Gate

The Publication Gate protects:

```text id="glj48z"
RELEASED → PUBLISHED
```

A conceptual gate is:

```text id="d1jwzp"
Release Identity      PASS
Approval              PASS
Artifacts             VERIFIED
Provenance            PASS
Documentation         READY
Targets               AVAILABLE
Credentials           VALID
Version               CONSISTENT
--------------------------------
PUBLICATION READY     PASS
```

---

# External Side Effects

Publishing introduces externally visible side effects.

Examples include:

* creating remote tags;
* uploading packages;
* creating releases;
* making documentation public;
* updating registry metadata.

These operations should occur after lower-risk validation has already passed.

---

# Publication Sequencing

Multi-target publication requires deliberate ordering.

A safe sequence may be:

```text id="chleox"
verify release
      ↓
publish source anchor
      ↓
publish artifacts
      ↓
publish release metadata
      ↓
publish release notes
      ↓
verify publication
      ↓
promote distribution channel
```

The exact sequence depends on release profile.

---

# Ordering Principle

Publication ordering should minimize unsafe partial states.

For example, a stable channel should not normally point to a version whose artifacts have not yet been verified.

---

# Publication Transaction

A release publication may be modeled as a transaction-like process.

Conceptually:

```text id="6xz95l"
BEGIN PUBLICATION

publish target A
publish target B
publish target C

verify A
verify B
verify C

COMMIT PUBLISHED STATE
```

Many external systems cannot provide true distributed transaction semantics.

Therefore, FamilyOS must preserve intermediate state and recovery information.

---

# Atomic Publication

Where a target supports atomic publication, FamilyOS SHOULD use it where practical.

Atomic publication minimizes states where consumers can observe incomplete release content.

Examples may include:

* draft release followed by activation;
* staged package promotion;
* immutable object publication followed by alias switch.

---

# Non-Atomic Publication

Where publication is inherently multi-step, the workflow must record which operations completed.

Example:

```text id="bgw79t"
Git Tag             PASS
Package Registry    PASS
Documentation       FAIL
Release Notes       NOT STARTED
```

This is a partial publication state.

It must not be reported as fully published.

---

# Partial Publication

Partial publication occurs when at least one external release side effect succeeds but the complete mandatory publication set does not.

Possible causes include:

* network failure;
* registry outage;
* permission failure;
* invalid artifact;
* documentation publishing failure;
* release metadata error.

Partial publication requires explicit recovery.

---

# Partial Publication State

A partial release should preserve per-target state.

Conceptually:

```text id="g75evw"
PublicationState
├── git_tag: published
├── package: published
├── documentation: failed
└── stable_channel: not_started
```

This enables safe recovery.

---

# Publication Failure

A release publication may transition to `FAILED` when mandatory publication cannot complete.

The release history must record:

* failed target;
* successful targets;
* candidate;
* release version;
* artifacts involved;
* recovery options.

---

# Publication Retry

A retry must inspect actual external state before repeating side effects.

The rule is:

> Verify before retry.

For example:

```text id="oz5q8p"
package upload returned timeout
```

does not prove that the package does not exist.

The retry workflow should query the target first.

---

# Idempotent Publication

Publication operations SHOULD be idempotent where possible.

Example:

```text id="dy1u7j"
artifact absent
→ publish

artifact exists with expected checksum
→ verify and continue

artifact exists with different checksum
→ BLOCK
```

---

# Publication Collision

A publication collision occurs when an official release identity already exists with different content.

Example:

```text id="yd1mwd"
registry:
5.2.0 checksum A

attempted release:
5.2.0 checksum B
```

The release MUST block.

Existing immutable versions must not be silently overwritten.

---

# Source Publication

For Git-based releases, source publication may include:

* release commit pushed;
* official release tag pushed;
* remote tag verified.

For some release profiles, this alone may constitute the primary publication mechanism.

---

# Artifact Publication

Artifact publication moves qualified release artifacts into an authoritative artifact target.

The workflow should verify:

* artifact name;
* version;
* checksum;
* target;
* publication result.

The published artifact must match the candidate artifact where practical.

---

# Package Publication

Package releases may be published to package registries.

The publication process must verify:

```text id="g4vpxm"
package version
package identity
package metadata
artifact checksum
registry target
```

Package publication should be treated as immutable where the registry supports immutable versions.

---

# Plugin Publication

Official plugin releases may require publication into a plugin registry or plugin distribution mechanism.

Publication should preserve:

* plugin identity;
* plugin version;
* platform compatibility;
* compliance status;
* artifact integrity;
* release notes.

---

# Documentation Publication

Documentation may be published to:

* repository;
* documentation site;
* generated documentation host;
* downloadable archive.

Documentation publication must remain aligned with the corresponding release version.

---

# Release Metadata Publication

Release metadata may include:

* release version;
* release type;
* release channel;
* artifact inventory;
* source revision;
* compatibility information;
* provenance references;
* release notes.

Metadata should not contradict actual published state.

---

# Release Notes Publication

Required release notes should become accessible through an authoritative publication mechanism.

Possible targets include:

* Git hosting release page;
* documentation site;
* repository file;
* package registry metadata.

Release note publication should be verified like other release artifacts.

---

# Changelog Publication

The changelog is normally part of repository source state.

If a separate public changelog representation exists, it should match the released repository state.

---

# Publication Verification

Publication is not complete until mandatory targets are verified.

Verification should answer:

```text id="6r1zz8"
Does the release exist?

Does the expected version exist?

Do the expected artifacts exist?

Do their checksums match?

Does the tag point to the correct commit?

Are release notes accessible?

Is metadata correct?
```

---

# Verification Principle

The governing rule is:

> Trust the resulting target state, not only the command result.

A successful upload command is evidence of attempted publication.

Target verification establishes successful publication.

---

# Remote Tag Verification

For Git-based release publication:

```text id="9u75vz"
remote tag
=
expected release commit
```

should be confirmed.

---

# Artifact Verification

For file-based artifacts:

```text id="mp0hbt"
candidate checksum
=
published checksum
```

should be confirmed where the target allows it.

---

# Package Verification

Package verification may include:

* registry version lookup;
* package metadata inspection;
* clean-environment installation;
* checksum or digest verification;
* smoke testing.

---

# Documentation Verification

Documentation publication may verify:

* expected version visible;
* expected pages available;
* links valid where practical;
* release notes visible;
* no stale release banner.

---

# Publication Evidence

A publication record should eventually contain:

```text id="0vubl4"
release version
publication target
artifact / metadata identity
timestamp
publisher identity
result
verification status
```

This evidence supports historical reconstruction.

---

# Publication Timestamp

The release publication time should be recorded where meaningful.

When several targets publish at slightly different times, the framework may distinguish:

* release start;
* target publication times;
* release publication completion.

---

# Release Date

The official release date should align with the release's publication policy.

For simple releases, it may be the date mandatory publication completes.

The exact definition should remain consistent across FamilyOS release records.

---

# Distribution Definition

Distribution exposes a published release to intended consumers.

It may include:

* channel promotion;
* alias update;
* registry visibility;
* rollout activation;
* downstream synchronization.

Distribution is often more mutable than publication.

---

# Distribution Target

A Distribution Target represents the consumer-facing availability path.

Examples include:

```text id="j6j57g"
stable channel
preview channel
maintenance channel
plugin catalog
package index
documentation current alias
```

---

# Version vs Distribution Alias

Official versions are immutable.

Distribution aliases are mutable.

Example:

```text id="ylme5o"
stable → 5.2.0
```

may later become:

```text id="zpuw9d"
stable → 5.3.0
```

without changing either official release identity.

---

# Stable Promotion

Stable distribution should only occur after stable qualification.

The preferred sequence is:

```text id="osvvfi"
publish version
      ↓
verify version
      ↓
promote stable alias
      ↓
verify stable alias
```

---

# Candidate Distribution

Candidate releases may be exposed through a candidate channel.

Example:

```text id="1zgxt1"
candidate → 5.2.0-rc.3
```

Consumers must be able to distinguish candidate from stable availability.

---

# Preview Distribution

Preview releases may be distributed to a limited or explicitly pre-release audience.

The release must clearly communicate reduced stability expectations.

---

# Maintenance Distribution

A maintenance channel may point to a supported previous release line.

For example:

```text id="1d1cq8"
stable → 6.1.0
maintenance/5 → 5.9.4
```

This supports controlled parallel maintenance.

---

# Distribution Promotion

Promotion changes consumer-facing release state.

A promotion must identify:

* source release;
* source channel where applicable;
* target channel;
* release version;
* approval;
* verification result.

---

# Distribution Without Rebuild

Channel promotion SHOULD reuse the same published artifacts.

The preferred model is:

```text id="mdgn5u"
published artifact
      ↓
candidate channel
      ↓
stable channel
```

not:

```text id="i0y24o"
candidate artifact
      ↓
rebuild
      ↓
stable artifact
```

without renewed qualification.

---

# Stable Alias Verification

After channel promotion:

```text id="5m8sv0"
stable
=
intended release version
```

should be verified.

---

# Distribution Failure

Distribution may fail even after publication succeeds.

Example:

```text id="6y1gd7"
release published     PASS
stable channel update FAIL
```

The release remains published but not fully distributed.

This must remain explicit.

---

# Publication Without Distribution

A valid lifecycle may intentionally stop at `PUBLISHED`.

Examples include:

* release awaiting scheduled rollout;
* candidate released to registry but not stable;
* documentation staged but not activated.

The state must remain clear.

---

# Staged Distribution

Future FamilyOS releases may support staged distribution.

Conceptually:

```text id="25b0al"
published
   ↓
internal
   ↓
preview
   ↓
limited
   ↓
stable
```

Each stage may require verification.

---

# Progressive Distribution

Advanced release strategies may include:

* canary rollout;
* percentage rollout;
* environment-based rollout;
* geography-based rollout;
* consumer-group rollout.

EPIC-REL-001 does not require immediate implementation.

The architecture must remain compatible with these strategies.

---

# Distribution Observation

Promotion should be followed by appropriate observation.

Potential checks include:

* availability;
* installation success;
* runtime stability;
* compatibility;
* consumer errors.

This information may influence final completion or recovery.

---

# Distribution Freeze

A release may be published but distribution intentionally paused.

Reasons may include:

* external dependency;
* security coordination;
* maintenance window;
* consumer communication;
* final operational approval.

This must remain an explicit state.

---

# Publication Approval

Publication authority may be distinct from release validation authority.

For example:

```text id="j33ugr"
validator
→ validates candidate

release approver
→ approves release

publisher
→ performs publication
```

These roles may overlap in small workflows.

Their authority must remain explicit.

---

# Distribution Approval

Stable channel promotion may require separate authority from artifact publication.

This is especially useful where publication and consumer exposure carry different operational risks.

---

# Least Privilege

Publishing credentials should be separated by target where practical.

Example:

```text id="8wjdq3"
Git tag token
package registry token
documentation token
channel promotion token
```

This limits failure impact.

---

# Publication Security

Publishing systems are high-value supply-chain targets.

Controls may include:

* protected credentials;
* trusted runners;
* immutable versions;
* artifact integrity;
* approval gates;
* audit logs;
* tag protection.

Detailed requirements are defined in `19-Release-Security.md`.

---

# Consumer Trust

A consumer should eventually be able to determine:

```text id="lrju2q"
Is this release official?

Which version is it?

Which channel is it from?

Is the artifact authentic?

Is it still supported?

Has it been withdrawn?
```

Publication and distribution metadata should support these questions.

---

# Release Discovery

FamilyOS may eventually provide release discovery mechanisms.

Consumers may query:

* latest stable;
* latest maintenance;
* available candidate;
* plugin compatibility;
* release history.

Discovery aliases must resolve to explicit immutable versions.

---

# `latest` Alias

If FamilyOS uses `latest`, its semantics must be defined.

For example:

```text id="0eb1z2"
latest == latest stable version
```

is preferable to ambiguous interpretation.

---

# Current Release Alias

A mutable `current` or `stable` reference may identify the recommended release.

It must never replace explicit version history.

---

# Withdrawal

Withdrawal removes a release from normal consumption while preserving historical identity.

A withdrawn release may remain:

* tagged;
* recorded;
* historically visible.

Its distribution aliases should no longer promote it.

---

# Withdrawal Process

Conceptually:

```text id="oxc3ig"
defective release detected
      ↓
withdrawal authorized
      ↓
remove from active distribution
      ↓
mark release WITHDRAWN
      ↓
publish consumer guidance
```

---

# Artifact Withdrawal

Some registries may support:

* yanking;
* de-listing;
* deprecation;
* visibility removal.

These mechanisms should preserve version history where possible.

---

# Release Supersession

A release becomes `SUPERSEDED` when a newer release becomes preferred.

Example:

```text id="3nv0sc"
5.2.0
   ↓
5.2.1 published
   ↓
5.2.0 SUPERSEDED
```

Supersession is a normal historical transition.

---

# Supersession Is Not Deletion

Superseded releases may remain available for:

* historical analysis;
* debugging;
* compatibility;
* rollback;
* maintenance.

Support policy determines whether they remain recommended.

---

# Distribution Rollback

If the active stable release proves defective, distribution may be rolled back to a previous release.

Example:

```text id="9r09gp"
stable → 5.2.0
      ↓
defect detected
      ↓
stable → 5.1.4
```

Both explicit releases remain unchanged.

---

# Rollback Verification

After channel rollback, the workflow must verify:

* stable alias;
* artifact availability;
* consumer path;
* previous version validity.

Rollback itself is a release operation requiring evidence.

---

# Forward Recovery

If rollback is unsafe, distribution may instead move directly to a corrected release.

```text id="0xkb9b"
stable → 5.2.0
      ↓
problem
      ↓
5.2.1 corrective release
      ↓
stable → 5.2.1
```

This is often safer where data or compatibility changed irreversibly.

---

# Publication Recovery

Recovery from publication failure should begin from recorded actual state.

Example:

```text id="bblt46"
tag published
package published
documentation failed
```

A correct recovery process should attempt only missing or failed operations where safe.

---

# Cleanup

Some failed publication artifacts may need cleanup.

Cleanup may include:

* deleting draft release objects;
* removing incomplete temporary files;
* resetting mutable aliases.

Cleanup must not silently delete immutable official history.

---

# Publication Drafts

Where supported, draft release mechanisms are useful.

A possible flow is:

```text id="95smb1"
create draft
      ↓
upload artifacts
      ↓
verify
      ↓
activate release
```

This reduces consumer exposure to partially assembled releases.

---

# Staging Registry

Future release infrastructure may use staging registries.

Conceptually:

```text id="v23ndb"
candidate registry
      ↓
validation
      ↓
promotion
      ↓
stable registry
```

Promotion should preserve artifact identity.

---

# Multi-Target Integrity

When identical artifacts are published to several targets:

```text id="82k2uc"
artifact checksum
```

should remain identical across those targets.

Different transformations require distinct artifact identities.

---

# Mirror Distribution

Mirrors may distribute official artifacts.

Mirrors should preserve:

* version;
* checksum;
* identity;
* release status.

A mirror should not modify official content under the same identity.

---

# CDN Distribution

A content delivery network may cache release artifacts.

Cache invalidation must not create version ambiguity.

Immutable versioned artifact URLs reduce this risk.

---

# Immutable URLs

Where practical, distribution should prefer immutable versioned paths such as:

```text id="gc8ogp"
/releases/5.2.0/artifact
```

over mutable paths such as:

```text id="s7x92f"
/latest/artifact
```

Mutable aliases may exist separately for discovery.

---

# Publication Naming

Published release resources should use predictable naming aligned with official release identity.

Examples:

```text id="mshz53"
familyos-5.2.0
v5.2.0-release-framework
finance-plugin-3.2.0
```

Ambiguous names should be avoided.

---

# Publication Metadata Consistency

Published metadata must agree across all authoritative targets.

For example:

```text id="ksy68t"
Version           5.2.0
Source Commit     abc123
Artifact Checksum X
```

should remain consistent wherever repeated.

---

# Release Page

A repository release page may aggregate:

* tag;
* release title;
* release notes;
* artifacts;
* checksums;
* links;
* compatibility information.

The page is a presentation and publication mechanism.

It does not replace the underlying release evidence.

---

# Distribution Metadata

Distribution systems may maintain mutable data such as:

```text id="28zqaa"
stable → 5.2.0
candidate → 5.3.0-rc.1
maintenance → 5.1.6
```

Such metadata should be observable and auditable.

---

# Publication Event Model

Future FamilyOS release systems may emit events such as:

```text id="pfp9q5"
release.publication.started
release.target.published
release.target.failed
release.published
release.distribution.started
release.channel.promoted
release.distributed
```

The exact implementation is defined by observability architecture.

---

# Publication Auditability

Release history should eventually identify:

* who or what initiated publication;
* which candidate was used;
* which version was published;
* target results;
* artifact digests;
* timestamps;
* failures;
* retries.

---

# Distribution Auditability

Channel changes should record:

* previous version;
* new version;
* target channel;
* authority;
* reason;
* timestamp.

This is especially important for stable and maintenance channels.

---

# Publication Metrics

Future metrics may include:

* publication success rate;
* partial failure rate;
* publication duration;
* verification failure rate;
* retry frequency;
* artifact mismatch rate.

Metrics should support reliability improvement.

---

# Distribution Metrics

Possible distribution metrics include:

* channel promotion frequency;
* rollback frequency;
* time from publication to stable promotion;
* failed promotion rate;
* consumer verification failures.

---

# Framework Release Publication

For current FamilyOS framework releases, publication may be relatively simple.

A canonical flow may be:

```text id="txvw4s"
final commit
      ↓
push branch
      ↓
verify remote commit
      ↓
create annotated tag
      ↓
push tag
      ↓
verify remote tag
      ↓
release considered published
```

If no additional distribution target exists, `PUBLISHED` may transition directly toward `COMPLETED`.

---

# Plugin Release Publication

A plugin release may require:

```text id="o1f6dl"
Git publication
      ↓
plugin artifact publication
      ↓
plugin metadata publication
      ↓
registry verification
      ↓
stable plugin channel promotion
```

---

# Platform Release Publication

A platform release may involve:

```text id="9jgbj2"
Git tag
package artifacts
plugin compatibility metadata
documentation
release notes
distribution aliases
```

The release should become `PUBLISHED` only after all mandatory targets verify successfully.

---

# Documentation Release Publication

A documentation release may include:

* release commit;
* tag;
* generated documentation;
* documentation host activation.

Generated output should remain traceable to source revision.

---

# Security Release Publication

Security release publication may require coordination of:

```text id="51i3vp"
fixed artifacts
release notes
security advisory
public disclosure
stable channel promotion
```

Timing may be tightly controlled.

---

# Emergency Release Publication

Emergency publication may use an accelerated workflow.

It must retain:

* publication authorization;
* artifact identity;
* version integrity;
* target verification;
* recovery evidence.

Urgency must not justify uncontrolled artifact replacement.

---

# Publication Profiles

Release profiles should define mandatory targets.

Example conceptual profiles:

```text id="9844e7"
framework-release
  git_branch
  git_tag

plugin-release
  git_tag
  plugin_artifact
  plugin_registry

platform-release
  git_tag
  package_registry
  documentation
  release_notes
```

Profiles must be governed.

---

# Publication Invariants

The following invariants apply.

## PUB1 — Publication operates on an approved release identity.

## PUB2 — Mandatory publication targets are explicit.

## PUB3 — Published artifact identity matches the qualified candidate where practical.

## PUB4 — Publication results are verified.

## PUB5 — Partial publication remains visible.

## PUB6 — Immutable versions are not silently overwritten.

## PUB7 — Retry inspects existing target state.

## PUB8 — Publication evidence identifies target, version, result, and verification.

## PUB9 — Publication credentials remain governed and protected.

## PUB10 — Official published release history remains reconstructable.

---

# Distribution Invariants

## DST1 — Distribution aliases resolve to explicit release versions.

## DST2 — Stable promotion requires applicable qualification.

## DST3 — Promotion should preserve validated artifact identity.

## DST4 — Distribution state is independently observable from publication state.

## DST5 — Channel changes must remain governed.

## DST6 — Withdrawal does not erase historical release identity.

## DST7 — Supersession preserves previous release history.

## DST8 — Rollback or channel restoration is verified.

---

# Publishing Anti-Patterns

## Upload Equals Publish

Treating one successful upload as proof of complete release publication.

---

## Publish Before Approval

Executing external publication before applicable governance approval.

---

## Mutable Release Artifact

Replacing an existing package under the same official version.

---

## Blind Multi-Target Publication

Publishing to several systems without recording individual target state.

---

## Retry Without Query

Repeating a timed-out upload without checking whether the remote target already accepted it.

---

## Release Notes Later

Publishing the official stable release while mandatory release communication remains incomplete.

---

## Publish Unverified Rebuild

Rebuilding artifacts during publication and publishing them without renewed validation.

---

# Distribution Anti-Patterns

## Stable Before Verify

Updating the stable channel before publication verification completes.

---

## Channel as Version

Telling consumers only to use `latest` without preserving explicit release identity.

---

## Silent Stable Rollback

Changing stable to an older version without recording why.

---

## Delete Defective History

Removing all evidence of a bad release instead of marking it withdrawn.

---

## Rebuild on Promotion

Creating new artifact contents when moving a release from candidate to stable.

---

# Minimum Publishing Model

At minimum, a FamilyOS official release should know:

```text id="42q7bq"
release version
mandatory targets
publication result
verification result
```

For artifact releases, it should additionally know:

```text id="o5vh1i"
artifact identity
artifact checksum where practical
```

---

# Minimum Distribution Model

Where release channels exist, FamilyOS should know:

```text id="iqbcn6"
channel
explicit version
promotion result
verification result
```

---

# Target Publishing Experience

At higher maturity, FamilyOS tooling should provide:

```text id="qotvz0"
FamilyOS Publication

Release              6.0.0
Candidate            6.0.0-rc.2

Git Tag              VERIFIED
Package Registry     VERIFIED
Documentation        VERIFIED
Release Notes        VERIFIED

Mandatory Targets    4
Completed            4
Failed               0

PUBLICATION          COMPLETE
```

---

# Target Distribution Experience

After publication:

```text id="krpn4a"
FamilyOS Distribution

Release              6.0.0
Target Channel       Stable

Published Release    VERIFIED
Channel Update       PASS
Channel Version      6.0.0
Consumer Check       PASS

DISTRIBUTION         COMPLETE
```

---

# Target Failure Experience

If publication partially fails:

```text id="xzx2kt"
FamilyOS Publication

Release              6.0.0

Git Tag              PASS
Package Registry     PASS
Documentation        FAIL
Stable Channel       NOT STARTED

Release State        FAILED

Recovery:
Resume documentation publication,
verify all mandatory targets,
then continue distribution.
```

The operator should not have to infer this state manually.

---

# Relationship With Release Lifecycle

`05-Release-Lifecycle.md` defines:

```text id="7wfmuf"
RELEASED
PUBLISHED
DISTRIBUTED
COMPLETED
```

This document defines the operations and evidence behind those states.

---

# Relationship With Versioning

`06-Versioning-Strategy.md` defines immutable release versions.

Publishing must preserve those version semantics.

---

# Relationship With Release Types and Channels

`07-Release-Types-and-Channels.md` defines distribution channels and promotion semantics.

This document governs how publication and channel exposure are executed.

---

# Relationship With Release Planning

`08-Release-Planning.md` identifies publication targets and distribution intent before execution.

---

# Relationship With Artifacts and Provenance

`11-Artifacts-and-Provenance.md` defines the identity and integrity of published artifacts.

---

# Relationship With Release Automation

`13-Release-Automation.md` defines idempotent, stateful execution and safe retry.

Publication automation must follow those principles.

---

# Relationship With CI/CD Integration

`14-CI-CD-Integration.md` defines how privileged publication stages operate in trusted pipeline environments.

---

# Relationship With Changelog and Release Notes

`15-Changelog-and-Release-Notes.md` defines release communication that must accompany publication where required.

---

# Relationship With Tagging and Repository State

`16-Tagging-and-Repository-State.md` defines Git release anchors and remote tag verification.

Git publication may be one mandatory publication target.

---

# Relationship With Rollback and Recovery

`18-Rollback-and-Recovery.md` defines how failed or defective publication and distribution states are recovered.

---

# Relationship With Release Security

`19-Release-Security.md` defines protection of publishing authority, credentials, artifacts, targets, and consumer trust.

---

# Relationship With Release Observability

`20-Release-Observability.md` defines publication and distribution telemetry, state, evidence, and failures.

---

# Relationship With Release Governance

`21-Release-Governance.md` defines who may publish, promote, withdraw, supersede, or roll back official releases.

---

# Final Statement

The FamilyOS Publishing and Distribution model establishes the controlled transition between an approved release and an officially consumable release.

Publishing makes the qualified release authoritative across defined release targets.

Distribution exposes that published release through governed consumer channels.

By separating these responsibilities, verifying every mandatory target, preserving artifact identity, detecting partial publication, supporting safe retry, and treating channel promotion as an explicit governed operation, FamilyOS can publish and distribute releases without losing traceability, integrity, or recovery capability.

A release is not complete because an upload happened.

It becomes complete only when the required publication and distribution state has been deliberately achieved, verified, and recorded.
