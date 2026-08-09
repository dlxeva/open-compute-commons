# Open Compute Commons: Protocol v0.2 (candidate draft)

> English is the authoritative public version of this document.
> Chinese mirror: [`spec/i18n/zh-CN/PROTOCOL_v0.2.md`](i18n/zh-CN/PROTOCOL_v0.2.md).

- **Status**: candidate draft — unpublished, unimplemented, not deployed.
- **Date**: 2026-08-09.
- **Previous version**: v0.1 (kept in an unpublished local experiment directory, **not in this repository**; see §13).
- **Nature of this version**: **semantic & data contract candidate**. This document defines objects, states, fields and error semantics. It does **not** define a live system.

> **The boundary in one sentence**: v0.2 is only a contract draft describing "what the objects and states should look like *if* this were built". The online Control Plane, MCP adapter, Runner and ledger service are **all unimplemented**. Every fixture, example and task package in this document is **synthetic** — not the output of a real pilot, and not representative of any real requester, real authorized data, or real public-benefit output.

---

## 0. Scope of this revision (v0.1 → v0.2)

This revision responds to engineering feedback. Its scope:

| # | Item | v0.1 state | v0.2 state |
|---|---|---|---|
| 1 | Object model | Only an implicit "task / shard" notion | 11 first-class objects filled in (§2) |
| 2 | State machines | A single task state machine mixing several lifecycles | Split into four: Action / Shard / Claim / Submission (§3) |
| 3 | Versioning and immutability | None | version / content_hash / freeze semantics (§4) |
| 4 | Idempotency | None | idempotency_key + replay semantics (§4.3) |
| 5 | Claim semantics | One sentence: "take a task" | lease / timeout / renewal / preemption / replication (§5) |
| 6 | Acceptance | Single layer: "automated check + human spot check" | Four validation layers L1–L4 (§6) |
| 7 | Disputes and errors | One `DISPUTED` status | Dispute process + structured error code table (§7) |
| 8 | Data / execution policy | Scattered through the proposal | Explicit `data_policy` / `execution_policy` objects (§8) |
| 9 | Security model | Scattered assertions | Explicit threat model and constraints (§9) |
| 10 | Normative strength | None | MUST / SHOULD / MAY + conformance profiles (§10, §11) |
| 11 | Entry point | Undefined | Web/CLI as the base entry point, MCP only as an optional adapter (§8.3) |
| 12 | Control plane / execution plane | Not separated | Control Plane separated from Execution Plane (§9.1) |

Material in v0.1 that this document does not cover (role definitions, the institutional supplementary-track narrative, the co-design question list) continues to be governed by v0.1.

**For what this revision did not resolve, see §12 deferred / unknown / blocked.**

---

## 1. Keywords and normative strength

The keywords **MUST / MUST NOT / SHOULD / SHOULD NOT / MAY** in this document are to be interpreted per RFC 2119 / RFC 8174, and carry normative meaning only when in all capitals.

Because **there is no implementation yet**, the current force of every MUST is: **any implementation claiming compatibility with OCC v0.2 must satisfy it**. These requirements do not create obligations for this repository or for anyone.

---

## 2. Object Model

### 2.1 Object overview

```text
Action  (one public action; the outermost container)
  └── TaskDefinition  (frozen task semantics: what to do, how it is accepted)
        └── Unit      (acceptance atom: the smallest work that can be judged pass/fail independently)
              └── Shard  (claim atom: a bundle of one or more Units)
                    └── Claim  (one participant's lease on one Shard)
                          └── Attempt  (one actual execution; the metering atom)
                                └── Submission  (one delivery)
                                      └── Validation  (one layer of judgement on a Submission)

CanonicalResult      (the single result finally adopted for a Unit)
ContributionRecord   (a contribution accounting entry)
Release              (a frozen, published set of results)
Event                (append-only record of every state change)
```

The division into three atoms is described in `spec/TASK_SPLITTING_v0.1.md`: **Unit is the acceptance atom, Shard is the claim atom, Attempt is the execution-metering atom.**

### 2.2 Action

One public action. It is the boundary for budget, policy, release and accounting.

Required fields (MUST): `action_id`, `version`, `status`, `title`, `purpose`, `data_policy`, `execution_policy`, `created_at`.

SHOULD: `requester_ref`, `coordinator_ref`, `acceptance_policy_ref`, `result_license`, `content_hash`.

MUST NOT: contain any participant account identifier, API key, token, cookie or credential reference (§9.3).

### 2.3 TaskDefinition

The **frozen semantics** of one class of task under an Action: input shape, execution instructions, output schema, acceptance rules.

Required (MUST): `task_definition_id`, `action_id`, `version`, `status`, `instructions_ref`, `output_schema_ref`, `acceptance_policy`, `content_hash`.

Key rules:
- Once a TaskDefinition reaches `status=frozen`, its semantics **MUST NOT** be modified in place; any modification MUST produce a new `version` and a new `content_hash` (§4).
- Claims and Submissions already produced against an older version **MUST** continue to be accepted under that older version, unless explicitly invalidated (`superseded`).

### 2.4 Unit

The **acceptance atom**. A Unit is the smallest amount of work that can be judged `pass` / `fail` independently.

Required (MUST): `unit_id`, `task_definition_id`, `input_ref`, `content_hash`.

SHOULD: `workload_envelope` (estimated workload range), `sensitivity_level` (L0–L3).

Rules:
- A Unit **MUST** be independently acceptable, without depending on the results of other Units in the same batch.
- A Unit **MUST NOT** span different sensitivity levels within `data_policy`.

### 2.5 Shard

The **claim atom**. A Shard bundles 1..N Units and is the thing a participant can "take".

Required (MUST): `shard_id`, `task_definition_id`, `unit_ids` (non-empty), `status`, `version`, `content_hash`.

SHOULD: `lease_duration_seconds`, `max_concurrent_claims`, `replication_factor`, `parent_shard_id` (a rework shard points at the original shard).

Rules:
- The same Unit **MAY** appear in more than one Shard if and only if this is for `replication` (repeated execution reconciled by consensus) or `rework`.
- A rework Shard **MUST** contain only Units that did not pass, and **MUST NOT** re-include Units that already have a CanonicalResult (§6.5).

### 2.6 Claim

A participant's **exclusive or boundedly concurrent lease** on a Shard within a time window.

Required (MUST): `claim_id`, `shard_id`, `contributor_ref`, `status`, `leased_at`, `lease_expires_at`, `idempotency_key`.

MUST NOT: contain the participant's third-party account ID, email address or API key. `contributor_ref` **MUST** be a project-internal pseudonymous handle.

### 2.7 Attempt

The **execution-metering atom**. One actual execution attempt. A single Claim **MAY** have multiple Attempts (retry after failure, switching models).

Required (MUST): `attempt_id`, `claim_id`, `status`, `started_at`.

SHOULD: `finished_at`, `self_reported_usage` (self-reported usage; see §8.4), `execution_environment` (self-reported category of execution environment, not a device fingerprint).

Rule: usage data **MUST** be labelled `self_reported`, and implementations **MUST NOT** present it as verified metering.

### 2.8 Submission

One delivery. It points at concrete artifacts and their hashes.

Required (MUST): `submission_id`, `claim_id`, `unit_results` (one entry per Unit), `status`, `submitted_at`, `content_hash`, `idempotency_key`.

Rules:
- A Submission **MUST** cover **all** Units of the Shard corresponding to its Claim; Units that were not completed **MUST** be explicitly marked `skipped` with a reason code. Silent omission is not allowed.
- Once submitted, a Submission **MUST** be immutable; corrections **MUST** be expressed through a new Submission (a new `submission_id`).

### 2.9 Validation

**One layer** of judgement on a Submission. Each of the four layers produces one Validation (§6).

Required (MUST): `validation_id`, `submission_id`, `layer` (`L1_schema`|`L2_rule`|`L3_crosscheck`|`L4_human`), `verdict`, `decided_at`.

SHOULD: `per_unit_verdicts`, `error_codes`, `sample_ratio` (L4 sampling ratio), `validator_ref`.

Rule: Validations **MUST** be append-only; a reversal **MUST** be expressed through a new Validation record (referencing the reversed one in `supersedes`) and **MUST NOT** overwrite in place.

### 2.10 CanonicalResult

The single result **finally adopted** for a Unit. This is the one authoritative answer to "who actually completed this Unit, and what is the result".

Required (MUST): `unit_id`, `source_submission_id`, `content_hash`, `accepted_at`.

Rules:
- A Unit **MUST** have at most one `active` CanonicalResult.
- When `replication_factor > 1`, the CanonicalResult **MUST** be determined by `acceptance_policy.consensus_rule` (§6.4), and **MUST NOT** simply be the first arrival.
- Revoking a CanonicalResult **MUST** be done through a new record marked `revoked` with a reason code; history **MUST** be retained.

### 2.11 ContributionRecord

A contribution accounting entry. See `spec/CONTRIBUTION_v0.1.md` for details.

Key rule: **accounting is only allowed after the relevant state has been confirmed** (the Submission is accepted, or the confirming event for the corresponding track has occurred). There **MUST NOT** be any unified score, level rating, or token-to-impact conversion.

### 2.12 Release

A frozen, published set of results.

Required (MUST): `release_id`, `action_id`, `canonical_result_refs`, `content_hash`, `license`, `released_at`.

Rule: a Release **MUST** be immutable. Corrections **MUST** be issued as a new version.

### 2.13 Event

An append-only record of every state change.

Required (MUST): `event_id`, `event_type`, `subject_type`, `subject_id`, `occurred_at`.

Rules:
- Every state transition in §3 **MUST** produce at least one Event.
- The Event log **MUST** be append-only; entries **MUST NOT** be deleted or modified in place.
- An Event **MUST NOT** contain credentials, complete conversation transcripts, or PII without consent.

---

## 3. Four state machines (separate, not shared)

v0.1 forced everything into a single `DRAFT → … → COMPLETED` chain, which is unusable in engineering terms: the lifecycle of an action, the claimability of a shard, one person's lease, and the processing progress of one delivery are **four different things** that run concurrently and interleave. v0.2 separates them.

### 3.1 Action state machine

```text
draft → review → open → executing → validating → releasing → closed
```

Exceptional / terminal: `suspended` (recoverable), `cancelled` (terminal), `archived`.

- `draft → review`: requirements and authorization materials are complete.
- `review → open`: `data_policy` and `execution_policy` are confirmed, and the TaskDefinition is frozen.
- `open → executing`: the first Claim is established.
- Any state → `suspended`: a reason code MUST be recorded. While `suspended`, new Claims **MUST NOT** be accepted; existing Claims **MAY** continue until expiry.
- `→ cancelled`: existing Events and ContributionRecords **MUST** be retained; confirmed contributions **MUST NOT** be retroactively deleted.

### 3.2 Shard state machine

```text
draft → open → partially_claimed → fully_claimed → completed
```

Exceptional: `blocked`, `expired`, `rework_required`, `retired`.

- `open ↔ partially_claimed ↔ fully_claimed`: **reversible**. Lease expiry or release returns the Shard to being claimable. This is the key point that v0.1's single-chain model could not express.
- `→ rework_required`: some Units did not pass. A new rework Shard **MUST** be derived (with `parent_shard_id` pointing at this Shard); this Shard **MUST NOT** be "reopened" in place.
- `→ completed`: all of its Units have an active CanonicalResult.
- `→ retired`: the TaskDefinition has been superseded and this Shard is no longer valid.

### 3.3 Claim state machine

```text
requested → active → submitted → closed
```

Exceptional: `expired`, `released` (participant gives up voluntarily), `revoked` (reclaimed by the coordinator), `superseded`.

- An `active` Claim **MUST** carry `lease_expires_at`.
- `active → expired`: the lease expired without submission or renewal. Expiry **MUST** return that share of the corresponding Shard to a claimable state.
- If a Submission arrives **later** under an `expired` Claim: the implementation **MUST** accept that Submission into validation (work already done is not discarded), but **MUST** mark it `late=true`; and when the Unit already has an active CanonicalResult, it **MUST** be handled under the duplicate-handling rules of §6.4 and **MUST NOT** overwrite automatically.
- `revoked` **MUST** carry a reason code (§7.3).

### 3.4 Submission state machine

```text
received → validating → accepted
                     ↘ partially_accepted
                     ↘ rejected
                     ↘ needs_rework
```

Exceptional: `duplicate`, `invalid`, `disputed`, `withdrawn`.

- `received → duplicate`: the `idempotency_key` matched an existing record (§4.3). The original record **MUST** be returned, and a second record **MUST NOT** be created.
- `partially_accepted`: **some Units passed**. This is a first-class status in v0.2, not a variant of `rejected`. Units that passed **MUST** normally produce a CanonicalResult and be accounted; Units that did not pass **MUST** enter the rework process.
- `disputed`: enters the dispute process in §7. A new CanonicalResult **MUST NOT** be produced that overrides the disputed subject before the dispute is resolved.

### 3.5 Relationships between state machines (invariants)

The following invariants **MUST** hold:

1. A Claim is `active` ⇒ its Shard is `partially_claimed` or `fully_claimed`.
2. A Shard is `completed` ⇒ all of its Units have an active CanonicalResult.
3. A Submission is `accepted` ⇒ its Claim is `submitted` or `closed`.
4. The number of active CanonicalResults for any Unit is ≤ 1.
5. An Action is `closed` ⇒ there is no `active` Claim.

`scripts/validate_v02.py` checks the statically checkable subset of these.

---

## 4. Versions, hashes and immutability

### 4.1 Versions

- All freezable objects (Action, TaskDefinition, Shard, Release) **MUST** have a `version`, formatted either as an incrementing integer or as a semver string; the style **MUST** be consistent within one Action.
- Changing semantics after freezing **MUST** increment the version and generate a new `content_hash`.
- Older versions **MUST** remain readable and **MUST NOT** be deleted.

### 4.2 content_hash

- The algorithm **MUST** be stated explicitly; `sha256` is recommended.
- The hashed object **MUST** be the **canonical serialization** of the object (canonical JSON: sorted keys, UTF-8, no superfluous whitespace), and **MUST** exclude the `content_hash` field itself as well as purely runtime fields (such as `received_at`).
- The field format **SHOULD** be `sha256:<64 hex>`.
- Input data (whatever a Unit's `input_ref` points to) **SHOULD** also carry a hash, so that it can be verified that participants processed the same input.

> The `examples/synthetic-action/checksums.json` in this repository is a **synthetic demonstration**: the hash values in it can be recomputed and checked locally, but what it demonstrates is the mechanism, not an integrity proof for a real release artifact.

### 4.3 Idempotency

- Creation of Claims and Submissions **MUST** carry an `idempotency_key` (client-generated; UUIDv4 or a hash of the content is suggested).
- Repeated submission with the same `idempotency_key` **MUST** return the **first** result, and **MUST NOT** produce a second record, a second ContributionRecord, or a second metering entry.
- The scope of an `idempotency_key` **MUST** be limited to `(action_id, contributor_ref, object_type)` and **MUST NOT** be shared globally.
- If the same key carries **different content**: the implementation **MUST** reject it and return `E_IDEMPOTENCY_CONFLICT` (§7.3), and **MUST NOT** silently adopt either version.
- The retention period **SHOULD** be ≥ the Action lifecycle + 30 days.

### 4.4 List of immutable objects

The following objects **MUST NOT** be modified in place once created: Submission, Validation, Event, CanonicalResult (revocation goes through a new record), Release, and a frozen TaskDefinition.

---

## 5. Claiming: leases, timeouts and repeated execution

### 5.1 Lease

- A Claim **MUST** have an explicit `lease_expires_at`.
- The default lease term **SHOULD** be determined by the Shard's `lease_duration_seconds`, and **SHOULD** be set with reference to 2–3× the upper bound of that Shard's `workload_envelope`.
- A participant **MAY** renew before expiry. A renewal **MUST** produce an Event, and **SHOULD** be subject to a cap on the number of renewals to avoid indefinite occupation.

### 5.2 Timeout

- Lease expiry **MUST** move the Claim into `expired` and release the Shard share.
- Release **MUST NOT** penalize the participant, and **MUST NOT** automatically delete the Attempt records they have already produced.
- For late submission after expiry, see §3.3.

### 5.3 Replication

Repeated execution is a **quality mechanism**, not waste:

- `replication_factor = N` means that the same Unit needs N independent results.
- When `N > 1`, `max_concurrent_claims` **MUST** be ≥ N, and different Claims **MUST** belong to different `contributor_ref` values.
- Participants **SHOULD NOT** be able to see other people's results for the same Unit (to avoid convergence). If an implementation cannot guarantee this, it **MUST** declare in the Action that this restriction is not met.
- For consensus rules, see §6.4.

### 5.4 Difference from idempotency (a common confusion)

- **Replication**: *intentional* multiple independent executions, producing multiple **different** Submissions. This is by design.
- **Idempotency**: *unintentional* repeated submission (network retry, double click, script rerun), which **MUST** be deduplicated into one.

The two **MUST NOT** be handled by the same mechanism: replication relies on different `claim_id` values; idempotency relies on the same `idempotency_key`.

---

## 6. Four-Layer Validation

Each layer produces its own independent Validation record. The layers **MUST** be executed in order; when an earlier layer returns `fail`, later layers **MAY** be skipped (a skip **MUST** be recorded as `skipped`, not as `pass`).

### 6.1 L1 — Schema / structural validation (automated, MUST)

Checks whether the deliverable conforms to `output_schema_ref`: fields present, types correct, enums legal, required fields complete.

- **MUST** be fully automated and **MUST** be reproducible offline.
- Failures **MUST** produce an `E_SCHEMA_*` error code and a JSON path.

### 6.2 L2 — Rule / redline validation (automated, MUST)

Checks the machine-decidable rules in `acceptance_policy`: length ranges, forbidden fields, forbidden speculation markers, format constraints, sensitive-content redlines.

- A redline hit **MUST** be judged `fail` outright and **MUST NOT** be overridden to pass by L3/L4 (a redline cannot be appealed into a pass; only the dispute process can establish that "the redline judgement itself was wrong").

### 6.3 L3 — Cross-checking (automated or semi-automated, SHOULD)

- When `replication_factor > 1`: compare the consistency of multiple independent results.
- When a gold set exists (calibration samples with known answers): compare accuracy.
- The output **SHOULD** be a score and the points of divergence, rather than a bare pass/fail.

### 6.4 L4 — Human spot check and domain judgement (human; MUST for tasks above L0)

- The `sample_ratio` and sampling method **MUST** be declared.
- Spot-check results **MAY** be extrapolated to the unsampled portion, but the extrapolation **MUST** be explicitly labelled as extrapolation and **MUST NOT** be recorded as item-by-item verification.
- Domain-correctness judgements **MUST** be made by the requester or an acceptor they delegate, and **MUST NOT** be made unilaterally by the coordinator.

### 6.5 Verdict composition and partial acceptance

- The final conclusion for a Submission **MUST** be composed from the four layers' results according to `acceptance_policy.combination_rule`.
- **Partial acceptance is a supported outcome by default**: judgement is per Unit; those that pass go to CanonicalResult, those that do not go to rework.
- Rework **MUST** target only the Units that did not pass (generating a new Shard whose `parent_shard_id` points at the original Shard).
- The consensus rule for repeated execution (`consensus_rule`) **MUST** be declared explicitly; options are `unanimous`, `majority`, `highest_l3_score`, `human_arbitration`. When not declared, it **MUST** default to `human_arbitration` and **MUST NOT** default to taking the first arrival.

---

## 7. Disputes and error codes

### 7.1 Who may raise a dispute

Participants (about judgements on their own Submissions), requesters (about the quality of accepted results), acceptors (about others' judgements), and coordinators (about process anomalies).

### 7.2 Dispute process

```text
raised → triage → (resolved_upheld | resolved_overturned | resolved_partial | withdrawn | unresolvable)
```

- A dispute **MUST** have a `dispute_id`, a reference to the subject object, a reason code, and an originator.
- During a dispute the subject object **MUST** be frozen (no new CanonicalResult may be produced that overrides it).
- Conclusions **MUST** be expressed through **new** Validation / CanonicalResult records and **MUST NOT** rewrite history in place.
- The arbitrator **MUST NOT** be the person who made the disputed judgement.
- `unresolvable`: when no judgement can be reached, it **MUST** be marked unresolvable with both sides' records retained, and a conclusion **MUST NOT** be forced.

> **unknown**: how arbitrators are selected, whether a third party is required, and whether disputes have a time limit — with no real operating experience, this version leaves these **undecided** (§12).

### 7.3 Error code table

Structured error codes, referenced by L1–L4 and by the process layer. Format: `E_<domain>_<reason>`.

| Error code | Domain | Meaning | Typical layer |
|---|---|---|---|
| `E_SCHEMA_MISSING_FIELD` | schema | Required field missing | L1 |
| `E_SCHEMA_TYPE_MISMATCH` | schema | Type mismatch | L1 |
| `E_SCHEMA_ENUM_INVALID` | schema | Illegal enum value | L1 |
| `E_SCHEMA_EXTRA_FIELD` | schema | Extra field not allowed | L1 |
| `E_RULE_LENGTH_OUT_OF_RANGE` | rule | Length out of range | L2 |
| `E_RULE_FORBIDDEN_CONTENT` | rule | Forbidden content present | L2 |
| `E_RULE_SPECULATION_DETECTED` | rule | Speculated information that was not provided | L2 |
| `E_RULE_SOURCE_MODIFIED` | rule | Modified source data that must not be changed | L2 |
| `E_REDLINE_SENSITIVE_DATA` | redline | Involves data at a forbidden level | L2 |
| `E_REDLINE_POLICY_VIOLATION` | redline | Violates data/execution policy | L2 |
| `E_CROSSCHECK_DIVERGENCE` | crosscheck | Divergence between results exceeds threshold | L3 |
| `E_CROSSCHECK_GOLD_MISMATCH` | crosscheck | Calibration samples below standard | L3 |
| `E_HUMAN_DOMAIN_REJECT` | human | Failed domain judgement | L4 |
| `E_HUMAN_INCONCLUSIVE` | human | Human reviewer could not decide | L4 |
| `E_CLAIM_LEASE_EXPIRED` | claim | Lease has expired | process |
| `E_CLAIM_LIMIT_EXCEEDED` | claim | Concurrent claim limit exceeded | process |
| `E_CLAIM_NOT_OWNER` | claim | Not the lease holder | process |
| `E_IDEMPOTENCY_CONFLICT` | idempotency | Same key, different content | process |
| `E_DUPLICATE_SUBMISSION` | idempotency | Idempotency hit; original record returned | process |
| `E_VERSION_SUPERSEDED` | version | Submitted against a superseded version | process |
| `E_HASH_MISMATCH` | version | content_hash does not match | process |
| `E_STATE_ILLEGAL_TRANSITION` | state | Illegal state transition | process |
| `E_UNIT_ALREADY_CANONICAL` | state | Unit already has an active result | process |

Implementations **MAY** extend the error codes; extensions **MUST** follow the same naming format and **MUST NOT** reuse a code already defined above with a different meaning.

---

## 8. data_policy and execution_policy

### 8.1 data_policy

An explicit object; MUST appear on the Action. Fields:

| Field | Strength | Description |
|---|---|---|
| `sensitivity_level` | MUST | `L0` publicly licensed / `L1` restricted / `L2` institution-internal / `L3` personal privacy, etc. |
| `license` | MUST | License of the input data |
| `authorization_ref` | MUST | Reference to the proof of authorization |
| `redistribution_allowed` | MUST | Whether participants may redistribute |
| `pii_present` | MUST | Whether PII is present |
| `retention_policy` | SHOULD | Requirements on local retention by participants |
| `egress_constraints` | SHOULD | Which classes of service data may or may not be sent to |

Rules:
- The first phase **MUST** accept only `sensitivity_level = L0`.
- `L1` and above **MUST NOT** enter the public claiming track (current status: **blocked**, see §12).
- The public track **MUST NOT** offer any confidentiality guarantee: once data is sent to a participant's environment and the model service they use, both **MUST** be assumed to be able to see it.

### 8.2 execution_policy

| Field | Strength | Description |
|---|---|---|
| `execution_locus` | MUST | Category of where execution is initiated (participant's own environment / institution-controlled environment) |
| `third_party_inference_possible` | MUST | Whether a third-party model service may be called |
| `account_custody` | MUST | Fixed value `participant_self_custody` (see §9.3) |
| `allowed_tooling` | SHOULD | Permitted categories of tooling |
| `reproducibility_requirements` | SHOULD | Whether model/parameters must be recorded |
| `usage_reporting` | SHOULD | Granularity of self-reported usage |

**Key clarification (carried over from and strengthened relative to v0.1)**: participants initiate execution in **environments they themselves control**. Model inference **may take place on third-party servers**. Participants **MUST** verify for themselves the terms of service, data policies and quota limits of the third-party services they use. The project **MUST NOT** take custody of accounts, **MUST NOT** automatically invoke personal subscriptions, and **MUST NOT** claim "local inference".

### 8.3 Entry point: Web/CLI as the base, MCP optional

- The base entry point **MUST** be Web and/or CLI. Any participant **MUST** be able to complete the full flow (browse → claim → execute → submit) without using MCP.
- MCP **MAY** exist as an **optional adapter**; it **MUST NOT** become a required dependency and **MUST NOT** carry privileged capabilities that Web/CLI lack.
- An adapter **MUST NOT** request, store or proxy a participant's third-party account credentials.

> **Current status**: Web, CLI and the MCP adapter are **all unimplemented** (§12). What this section defines is "what must be satisfied if they are implemented".

### 8.4 Self-reported usage

Usage fields **MUST** be labelled `self_reported: true`. Implementations **MUST NOT** present self-reported usage as verified metering, and **MUST NOT** compute any redeemable entitlement from it.

---

## 9. Security model

### 9.1 Separation of Control Plane and Execution Plane

```text
┌─────────────────────── Control Plane ───────────────────────┐
│ Action / TaskDefinition / Unit / Shard / Claim              │
│ Validation / CanonicalResult / ContributionRecord / Event   │
│ Handles only: metadata, state, hashes, verdicts, ledger     │
│ MUST NOT hold: participant credentials, third-party accounts│
│ or raw sensitive data                                       │
└──────────────────────────────────────────────────────────────┘
        ▲ Exchanges only (input refs, results, hashes, self-reported usage)
        ▼
┌────────────────────── Execution Plane ──────────────────────┐
│ Participant's own environment / institution-controlled env  │
│ Holds: participant's own accounts and quota, actual calls   │
│ MUST be controlled by participant or institution;           │
│ MUST NOT be held in custody by the project                  │
└──────────────────────────────────────────────────────────────┘
```

Rules:
- The Control Plane **MUST NOT** have the ability to execute code in the Execution Plane.
- The Execution Plane **MUST NOT** transmit credentials, complete conversation transcripts, or content beyond what `data_policy` permits to the Control Plane.
- The interface between the two planes **MUST** be data exchange and **MUST NOT** be remote execution.

### 9.2 Threat model (covered / not covered in this version)

Covered, with countermeasures:

| Threat | Countermeasure |
|---|---|
| Repeated submission to farm contributions | Idempotency key + accounting only after state confirmation (§4.3, §11) |
| Bulk low-quality delivery | L1/L2 automated + L3 cross-check + L4 spot check (§6) |
| Results silently rewritten | Immutable objects + append-only Events (§4.4) |
| Shard grabbing / hoarding | Lease + timeout + concurrency cap (§5) |
| Credential leakage | Credentials never enter the project (§9.3) |
| A judge validating their own work | The arbitrator may not be the original judge (§7.2) |

**Not covered (acknowledged as residual risk)**: whether participants actually follow the instructions (only self-auditing plus spot checks address this); the truthfulness of self-reported usage; Sybil attacks / sockpuppets; compromise of a participant's environment; data handling on the third-party model service side. These **MUST** be explicitly disclosed to participants before any real pilot.

### 9.3 Credential and identity constraints (hard constraints)

The following are **MUST NOT**, without exception:

- **MUST NOT** collect, store, proxy or forward participants' third-party account passwords, API keys, OAuth tokens or session cookies.
- **MUST NOT** require participants to transfer subscription quota to the project.
- **MUST NOT** package subscription quota as a tradeable balance or token.
- **MUST NOT** collect participants' complete conversation transcripts, device fingerprints or account email addresses as required fields.
- **MUST NOT** require uploading identity documents as a precondition for participation.
- Participant identifiers **MUST** be project-internal pseudonyms (`contributor_ref`).

### 9.4 Minimization in the public ledger

Events and the public ledger **MUST** follow minimization: record only task numbers, states, time ranges, contribution types, self-reported usage ranges, verdicts and result references. They **MUST NOT** record credentials, PII, or complete raw delivery content (unless `data_policy` explicitly permits publication).

---

## 10. Conformance Levels

An implementation may claim one of the following profiles. A claim **MUST** state the profile and any unmet items.

### Profile C0 — Document-Conformant

- Uses the v0.2 object names and state names;
- Provides static definitions of TaskDefinition, Unit and Shard;
- Requires no runtime system.

**This repository is at C0.** See `docs/CONFORMANCE_REPORT.md` for details.

### Profile C1 — Schema-Conformant

- All of C0, plus
- All core objects validate against `schemas/core/`;
- Provides content_hash values that can be recomputed locally;
- Provides valid / invalid fixtures and can distinguish between them.

### Profile C2 — Lifecycle-Conformant

- All of C1, plus
- Implements the four state machines and all invariants in §3.5;
- Implements idempotency (§4.3) and lease/timeout (§5);
- Implements L1+L2 automated validation;
- Supports partial acceptance and derivation of rework.

### Profile C3 — Operationally-Conformant

- All of C2, plus
- Implements L3, L4 and the dispute process;
- Control and Execution Planes actually deployed separately;
- A public append-only ledger;
- A usable Web/CLI base entry point.

> **C1–C3 are currently all unmet**: there is no runtime implementation. The static part of C1 is checked locally against the fixtures by `scripts/validate_v02.py`, but that is only **file-level validation**, not a service conformance certification.

---

## 11. Accounting constraints (echoing spec/CONTRIBUTION_v0.1.md)

- A ContributionRecord **MUST** be created only **after the state has been confirmed**: the Submission has reached `accepted` or `partially_accepted` (in the latter case only the passing portion is recorded), or the confirming event for the corresponding track has occurred.
- **MUST NOT** be pre-recorded while in the `received` / `validating` stage.
- There **MUST NOT** be any cross-track unified score, total, level or leaderboard as a primary presentation.
- There **MUST NOT** be any token-to-impact conversion or any formula converting contribution into influence or money.
- Activity evidence, quality evidence and impact evidence **MUST** be presented separately and **MUST NOT** be merged into a single number.
- Revoking a contribution (for example when cheating is discovered afterwards) **MUST** be done by marking a new record, and history **MUST NOT** be deleted.

---

## 12. Deferred / Unknown / Blocked

Three categories, distinguished clearly and without hedging.

### 12.1 Deferred (intentionally postponed; direction known)

| Item | Description |
|---|---|
| Web / CLI implementation | Not implemented in this round; only the contract is defined |
| MCP adapter | Optional adapter; not implemented in this round |
| Runner / executor | Not implemented; execution stays in the participant's environment |
| Ledger service and public site | Not being built |
| Notification / reminder mechanisms | Not designed |
| Multilingual task packages | Not designed |
| Refinement of the institutional supplementary track | Continues to follow v0.1 §7; not refined into the v0.2 object model |

### 12.2 Unknown (no evidence; no guessing)

| Item | Why it is unknown |
|---|---|
| Reasonable Unit granularity for a real task | No real task, no real timing data |
| Actual values for `workload_envelope` | All values in the examples are synthetic assumptions |
| A reasonable `replication_factor` | Depends on task type and quality distribution; no data |
| What the L4 sampling ratio should be | No real error-rate data |
| Real dispute rates and arbitration mechanisms | No operating experience |
| Participant retention and scale | Nobody has been recruited |
| What proportion automated acceptance can cover | Depends on task type; no data |
| Whether third-party terms of service permit this kind of collaboration | **Not verified with any provider**; permission is not assumed |
| How arbitrators are selected | Undecided |

### 12.3 Blocked (clear preconditions, unmet)

| Item | Blocked on |
|---|---|
| Any real pilot | No real requester, no real authorized data |
| L1+ data processing | No controlled environment, no accountable data-processing entity, no legal entity |
| Restricted hosting mode | No permission / encryption / deletion / audit capability |
| Institutional credits track | No institutional contact, no terms |
| Publishing the repository / community posts | Explicitly out of scope for this round |
| Organization / legal entity | Not registered |
| Licensing and attribution for real results | Requires confirmation from a real task owner |

---

## 13. Files in this repository that accompany this protocol

- `spec/TASK_SPLITTING_v0.1.md`: the splitting methodology for the three atoms Unit / Shard / Attempt.
- `spec/CONTRIBUTION_v0.1.md`: accounting semantics and forbidden fields.
- `schemas/core/`: JSON Schemas for the v0.2 core objects (candidate data contract).
- `conformance/`: synthetic fixture sets (including one negative set).
- `scripts/validate_v02.py`: local file-level validator (standard library only).
- `examples/synthetic-action/`: synthetic sample task package.
- `docs/CONFORMANCE_REPORT.md`: local validation results and the validator's capability boundaries.

> **About v0.1**: the previous version of this protocol, `PROTOCOL_v0.1.md`, along with a batch of early institutional allocation-track schemas, cases and simulation scripts,
> remain in an **unpublished local experiment directory** and are **not included in this repository**. References to v0.1 in this document are only version-history notes;
> they do not indicate that those files exist in this repository. If they are to enter public discussion, they need separate review before any decision to publish (see `PUBLISH_CHECKLIST.md`).

---

## 14. Honest disclosure (restated)

- This protocol is a **candidate draft**: unpublished, no organization registered, no platform deployed, no real data received, and no commitment made on behalf of any institution.
- The online **Control Plane, MCP adapter, Runner and ledger service are all unimplemented**.
- All fixtures, sample task packages, units and shards are **synthetic**; they are **not the output of a real pilot** and do not constitute public-benefit output.
- Participants execute in **environments they control themselves**; third-party terms of service, data policies and quotas are **for participants to verify themselves**; **the project does not take custody of accounts**.
- This protocol creates no obligation for any participant, and constitutes no endorsement by any institution.
