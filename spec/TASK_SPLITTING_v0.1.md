# Open Compute Commons: Task Splitting Specification v0.1 (candidate draft)

> English is the authoritative public version of this document.
> Chinese mirror: [`spec/i18n/zh-CN/TASK_SPLITTING_v0.1.md`](i18n/zh-CN/TASK_SPLITTING_v0.1.md).

- **Status**: candidate draft — unpublished, unimplemented.
- **Date**: 2026-08-09.
- **Depends on**: `spec/PROTOCOL_v0.2.md` (object model and state machines).
- **Nature**: a candidate splitting methodology and data contract. Every number, sample task and workload estimate in this document is **synthetic** and **not the output of a real pilot**.

---

## 1. The three atoms (the core distinction of this specification)

The v0.1 protocol had only a vague notion of a "shard", which welded together three separate concerns: acceptance, claiming and metering. v0.2 splits them into three independent atoms:

| Atom | Question it answers | Who cares | Cardinality |
|---|---|---|---|
| **Unit** | Was this small piece **done correctly**? | Acceptors, requesters | 1 Unit = 1 independent pass/fail judgement |
| **Shard** | **Who takes** this batch? | Participants, coordinators | 1 Shard = 1..N Units |
| **Attempt** | **How much did** this execution cost? | Metering, ledger | 1 Claim = 1..N Attempts |

### 1.1 Unit is the acceptance atom

- A Unit is the smallest work that can be judged pass or fail **independently**.
- Judging Unit A **MUST NOT** depend on the result of Unit B.
- A Unit **MUST** ultimately correspond to at most one active CanonicalResult.
- Partial acceptance, rework and consensus all happen at **Unit granularity**.

**Why this matters**: if acceptance can only be done over a whole batch, then 1 error out of 100 forces the entire batch into rework, wasting the participant's other 99 pieces of work. Unit granularity makes partial acceptance a first-class outcome.

### 1.2 Shard is the claim atom

- A Shard is the thing a participant "takes" in the interface.
- The size of a Shard is determined by **how much a person can finish in one sitting**, not by acceptance logic.
- A Shard **MUST NOT** affect acceptance granularity: bundling 20 Units into one Shard still means 20 independent judgements.

**Why this matters**: claim granularity is an ergonomics problem (too small and interaction cost dominates; too large and nobody dares take it and timeout rates rise), while acceptance granularity is a quality problem. Their optimal values are almost never the same.

### 1.3 Attempt is the execution-metering atom

- One Claim can have several Attempts: the first model output was inadequate, a retry with a different model, a restart after an interruption.
- Usage, duration and model information are recorded on the Attempt, **not on the Shard**.
- Attempt records **MUST** be labelled `self_reported`.

**Why this matters**: recording usage on the Shard would let retries pollute the workload baseline. Recording it on the Attempt is what yields the genuinely useful calibration figure: "how many attempts does completing one Shard take on average".

### 1.4 Relationship diagram

```text
TaskDefinition (frozen)
   │
   ├── Unit u1 ─┐
   ├── Unit u2 ─┼── Shard s1 ── Claim c1 ── Attempt a1 (failed)
   ├── Unit u3 ─┘              └─ Attempt a2 (succeeded) ── Submission sub1
   │                                                      ├── u1: pass  → CanonicalResult
   │                                                      ├── u2: pass  → CanonicalResult
   │                                                      └── u3: fail  → rework
   ├── Unit u4 ─┐
   └── Unit u5 ─┴── Shard s2 ── Claim c2 ── ...

   Unit u3 → Shard s3 (rework, parent_shard_id = s1)   ← contains only the failed u3
```

---

## 2. Splitting Constraints

### 2.1 Unit-level constraints

| # | Constraint | Strength |
|---|---|---|
| U1 | A Unit **MUST** be independently acceptable, without depending on other Units' results in the same batch | MUST |
| U2 | A Unit **MUST** have a stable identifier `unit_id` and an input `content_hash` | MUST |
| U3 | A Unit **MUST NOT** span different `sensitivity_level` values | MUST |
| U4 | A Unit's acceptance criteria **MUST** already be fixed when the TaskDefinition is frozen | MUST |
| U5 | A Unit **SHOULD** be small enough that a single judgement fits within a person's tolerable attention span | SHOULD |
| U6 | A Unit **SHOULD NOT** require the participant to obtain additional external material on their own | SHOULD |
| U7 | A Unit **MAY** carry a difficulty marker for later calibration | MAY |

### 2.2 Shard-level constraints

| # | Constraint | Strength |
|---|---|---|
| S1 | A Shard **MUST** be non-empty (at least one Unit) | MUST |
| S2 | Units within a Shard **MUST** belong to the same TaskDefinition at the same version | MUST |
| S3 | Units within a Shard **MUST** share the same `data_policy` sensitivity level | MUST |
| S4 | A Shard **MUST** declare `lease_duration_seconds` | MUST |
| S5 | A rework Shard **MUST** contain only Units that did not pass, and **MUST** set `parent_shard_id` | MUST |
| S6 | Shard size **SHOULD** keep the upper bound of `workload_envelope` within what one sitting can complete | SHOULD |
| S7 | The same Unit appearing in multiple parallel Shards **MUST** be only because of replication or rework | MUST |
| S8 | A Shard **SHOULD NOT** mix Units of wildly differing difficulty (it breaks workload estimation) | SHOULD |
| S9 | A Shard **MAY** declare `max_concurrent_claims` and `replication_factor` | MAY |

### 2.3 Attempt-level constraints

| # | Constraint | Strength |
|---|---|---|
| A1 | An Attempt **MUST** be associated with one Claim | MUST |
| A2 | Usage fields **MUST** be labelled `self_reported: true` | MUST |
| A3 | An Attempt **MUST NOT** record credentials, accounts or complete conversation transcripts | MUST |
| A4 | Failed Attempts **MUST NOT** be deleted (they are calibration data) | MUST |
| A5 | An Attempt **SHOULD** record the model category / capability tier, not a specific account | SHOULD |

---

## 3. workload_envelope

Do not use point estimates; use a **range plus a basis level**. A point estimate gets treated as a commitment; only a range is honest.

### 3.1 Structure

```yaml
workload_envelope:
  unit_of_measure: "unit"          # unit | shard | attempt
  human_minutes:                   # human attention time
    p50: 3
    p90: 8
    basis: "assumed"               # measured | calibrated | assumed | unknown
  model_calls:                     # number of model calls
    p50: 1
    p90: 3
    basis: "assumed"
  expected_attempts_per_claim:
    p50: 1
    p90: 2
    basis: "assumed"
  notes: "All values are synthetic assumptions with no real execution data behind them"
```

### 3.2 basis levels (must be labelled honestly)

| basis | Meaning | Usable for |
|---|---|---|
| `measured` | From real execution data for this task | Formal estimation |
| `calibrated` | From a calibration batch (similar task, sample size ≥ the calibration requirement) | Formal estimation |
| `assumed` | Guesswork / reasoning by analogy | **Discussion only**; MUST be labelled |
| `unknown` | No basis at all | MUST be labelled; MUST NOT be used in any external commitment |

Rules:
- Before an Action is published, `workload_envelope.basis` **SHOULD** reach at least `calibrated`.
- If it is `assumed` or `unknown`, the published material **MUST** state explicitly that "the workload estimate has no measured basis".
- **Every workload_envelope in this repository is `assumed`** (there is no real execution data whatsoever).

### 3.3 Why not a point value

Self-reported usage + a point estimate = participants treat the estimate as an upper bound, and either conclude they did something wrong when they exceed it or give up early. A range plus p90 makes "this one took 7 minutes" normal rather than anomalous.

---

## 4. From calibration to frozen release

```text
[1] draft_split        Splitting draft: define Unit boundaries and acceptance rules
       ↓
[2] dry_review         Requester + coordinator review: are Units independently acceptable?
       ↓
[3] calibration_batch  Calibration batch: small-sample execution, measure workload and error rate
       ↓
[4] revise             Adjust Unit granularity / Shard size / acceptance thresholds per calibration
       ↓
[5] freeze             Freeze TaskDefinition: fix version + content_hash
       ↓
[6] publish_shards     Generate and publish Shards for claiming
       ↓
[7] recalibrate        Periodic review during execution: timeout rate, rework rate, actual attempt count
```

### 4.1 Gates between stages

| Stage | Condition for entering the next stage | Strength |
|---|---|---|
| [1]→[2] | Every Unit has explicit acceptance rules | MUST |
| [2]→[3] | The requester has confirmed the domain acceptance criteria | MUST |
| [3]→[4] | The calibration batch is complete, with measured workload and error rate | SHOULD |
| [4]→[5] | Acceptance thresholds fixed; `data_policy`/`execution_policy` confirmed | MUST |
| [5]→[6] | `content_hash` generated, version fixed | MUST |
| During [6] | After freezing, semantics **MUST NOT** be changed in place; changes go through a new version | MUST |

### 4.2 What a calibration batch should measure

- The distribution of actual time per Unit (p50 / p90);
- The actual number of Attempts per Claim;
- The pass rate of the L1/L2 automated checks (a measure of whether the instructions are clear enough);
- The agreement between L4 human judgement and L1/L2 (a measure of whether the automated checks are sufficient);
- The rate of divergence between different participants' results (which determines `replication_factor`);
- The timeout rate (which determines `lease_duration_seconds`).

> **Current status: unknown.** No calibration batch has ever been run. This repository has no data for any of the metrics above.

### 4.3 What freezing means

After freezing, the following **MUST NOT** change: Unit boundaries, acceptance rules, output schema, redline definitions.

After freezing, the following **MAY** change (they do not affect the semantics of results already submitted): `lease_duration_seconds`, `max_concurrent_claims`, and how Shards are bundled (for Shards not yet claimed).

Any change to a frozen item **MUST** produce a new version, and Submissions already based on the old version **MUST** be accepted under the old version (§PROTOCOL_v0.2 2.3).

---

## 5. Public task example (**SYNTHETIC — a synthetic example, not a real task**)

> ⚠️ **This example is entirely synthetic.** There is no real requester, no real images, no real authorization and no real beneficiary. All IDs, values and hashes are for demonstration. It **MUST NOT** be cited as public-benefit output completed by OCC or as a pilot that has been carried out.

### 5.1 Scenario (synthetic)

Generating accessibility descriptions (alt text) for a batch of **hypothetical** publicly licensed educational illustrations.

```yaml
action_id: "act-synthetic-alttext-001"
title: "[SYNTHETIC] Accessibility descriptions for publicly licensed educational illustrations"
synthetic: true
data_policy:
  sensitivity_level: "L0"
  license: "SYNTHETIC-PLACEHOLDER"     # not a real license
  authorization_ref: "synthetic://no-real-authorization"
  redistribution_allowed: true
  pii_present: false
execution_policy:
  execution_locus: "participant_self_controlled"
  third_party_inference_possible: true
  account_custody: "participant_self_custody"
```

### 5.2 Unit definition (synthetic)

One Unit = one accessibility description for one image.

This satisfies U1 (independent acceptance): judging "is the description for this image adequate" does not require looking at any other image.

```yaml
unit_template:
  input_ref: "synthetic://image/{n}"
  output_schema_ref: "schemas/core/submission.schema.json#/definitions/unit_result"
  acceptance_rules:
    - id: "len"
      layer: "L2"
      rule: "Description length 40–200 characters"
      error_code: "E_RULE_LENGTH_OUT_OF_RANGE"
    - id: "no_speculation"
      layer: "L2"
      rule: "MUST NOT speculate about information not shown in the image (identity of people, location, period)"
      error_code: "E_RULE_SPECULATION_DETECTED"
    - id: "no_redundant_prefix"
      layer: "L2"
      rule: "MUST NOT begin with a redundant prefix such as \"an image shows\""
      error_code: "E_RULE_FORBIDDEN_CONTENT"
    - id: "domain_adequacy"
      layer: "L4"
      rule: "Informational adequacy in an educational context is judged by the requester"
      error_code: "E_HUMAN_DOMAIN_REJECT"
```

### 5.3 Three synthetic Units

| unit_id | Input (synthetic) | Difficulty marker |
|---|---|---|
| `unit-synthetic-001` | `synthetic://image/001` simple diagram | easy |
| `unit-synthetic-002` | `synthetic://image/002` illustration containing a chart | medium |
| `unit-synthetic-003` | `synthetic://image/003` multi-element scene | hard |

### 5.4 Two synthetic Shards

```yaml
- shard_id: "shard-synthetic-a"
  unit_ids: ["unit-synthetic-001", "unit-synthetic-002"]
  lease_duration_seconds: 3600
  replication_factor: 1
  max_concurrent_claims: 1

- shard_id: "shard-synthetic-b"
  unit_ids: ["unit-synthetic-003"]
  lease_duration_seconds: 3600
  replication_factor: 2        # high difficulty, take two independent results
  max_concurrent_claims: 2
```

Note that shard-b demonstrates the decoupling of Shard from Unit: a single high-difficulty Unit forms its own Shard and requires repeated execution.

### 5.5 Synthetic workload_envelope

```yaml
workload_envelope:
  unit_of_measure: "unit"
  human_minutes: { p50: 3, p90: 8, basis: "assumed" }
  model_calls:   { p50: 1, p90: 3, basis: "assumed" }
  expected_attempts_per_claim: { p50: 1, p90: 2, basis: "assumed" }
  notes: "SYNTHETIC: no real execution data of any kind; basis is uniformly assumed"
```

---

## 6. Partial Acceptance

### 6.1 Rules

- Judgement **MUST** be made per Unit.
- When there is a mix of passes and failures, the overall status of the Submission **MUST** be `partially_accepted` and **MUST NOT** be judged `rejected` as a whole.
- Units that passed **MUST** immediately produce a CanonicalResult and become accountable.
- Units that did not pass **MUST** enter the rework process and **MUST NOT** block settlement of the portion that passed.

### 6.2 Synthetic walkthrough

`shard-synthetic-a` contains u001 and u002:

```text
Submission sub-synthetic-a-1
  ├── unit-synthetic-001 → L1 pass, L2 pass, L4 pass  → accepted
  └── unit-synthetic-002 → L1 pass, L2 fail (E_RULE_LENGTH_OUT_OF_RANGE) → rejected

Submission status = partially_accepted
  → unit-synthetic-001: CanonicalResult established; participant records 1 accepted unit
  → unit-synthetic-002: enters rework
```

---

## 7. Rework

### 7.1 Rules

- Rework **MUST** be expressed through a **new Shard** and **MUST NOT** reopen the old Shard in place.
- A rework Shard **MUST** set `parent_shard_id` and **MUST** contain only Units that did not pass.
- A rework Shard **MUST NOT** contain Units that already have an active CanonicalResult.
- A rework Shard **SHOULD** carry the error codes from the previous round, so participants know what to change.
- Rework **MAY** be claimed by the original participant, and **MAY** also be opened to others; the policy **MUST** be declared in `acceptance_policy`.
- The number of rework rounds **SHOULD** be capped; once the cap is reached the Unit **SHOULD** move to `human_arbitration` or be marked `unresolvable`, and **MUST NOT** loop indefinitely.

### 7.2 Synthetic walkthrough (continuing from §6.2)

```yaml
- shard_id: "shard-synthetic-a-rework-1"
  parent_shard_id: "shard-synthetic-a"
  unit_ids: ["unit-synthetic-002"]        # only the one that failed
  rework_round: 1
  prior_error_codes: ["E_RULE_LENGTH_OUT_OF_RANGE"]
  lease_duration_seconds: 3600
```

`unit-synthetic-001` is **not** in the rework shard — this is the most important behavioural demonstration in this specification, and it is the point that `examples/synthetic-action/` and the conformance fixtures are meant to verify.

---

## 8. Replication and merging

### 8.1 Difference from idempotency

| | Replication | Idempotency |
|---|---|---|
| Intent | Deliberate multiple independent executions | Unintentional repeated submission |
| Result | Multiple **different** Submissions | Deduplicated into **one** |
| Mechanism | Different `claim_id` + different `contributor_ref` | Same `idempotency_key` |
| Accounting | Each participant records their own activity evidence | Recorded only once |

The two **MUST NOT** be handled by the same mechanism.

### 8.2 Merge rules (consensus_rule)

When `replication_factor > 1`, `acceptance_policy.consensus_rule` **MUST** be declared explicitly:

| Rule | Meaning | Applicable to |
|---|---|---|
| `unanimous` | Adopted only when all agree | High risk, low error tolerance |
| `majority` | Adopted on majority agreement (N ≥ 3) | Classification tasks with objective answers |
| `highest_l3_score` | Take the one with the highest L3 cross-check score | When a gold set exists |
| `human_arbitration` | A human selects among the several results | Open-ended generation tasks |

Rules:
- When not declared, it **MUST** default to `human_arbitration` and **MUST NOT** default to the first arrival.
- `majority` **MUST NOT** be used when N = 2 (no majority can be formed) and **MUST** be downgraded to `human_arbitration`.
- A Submission that is not selected **MUST NOT** be judged "wrong"; it **MUST** be recorded as `not_selected`, and its participant's activity evidence is recorded as usual (see `spec/CONTRIBUTION_v0.1.md`).

### 8.3 Synthetic walkthrough

`shard-synthetic-b` (u003, `replication_factor: 2`):

```text
Claim c-b-1 (contributor alpha) → sub-b-1 → L1/L2 pass
Claim c-b-2 (contributor beta)  → sub-b-2 → L1/L2 pass
L3 crosscheck: divergence (the two descriptions emphasize different things)
consensus_rule: human_arbitration (N=2, majority unusable)
  → arbitration selects sub-b-1 → CanonicalResult(u003) ← sub-b-1
  → sub-b-2 marked not_selected (not an error)
  → alpha records 1 accepted unit; beta records 1 completed attempt + not_selected
```

### 8.4 Collision between late submission and duplication

If a Unit already has an active CanonicalResult and a Submission targeting it arrives afterwards:

- The CanonicalResult **MUST NOT** be overwritten automatically;
- The Submission **MUST** be recorded and marked `late=true` / `E_UNIT_ALREADY_CANONICAL`;
- That participant's activity evidence **MUST** be recorded (the work really happened);
- It **MAY** be used as an additional cross-check sample in quality spot checks.

---

## 9. Deferred / Unknown / Blocked

**Deferred**: automatic splitting tools, automatic difficulty grading of Units, dynamic Shard bundling, a cross-Action workload baseline library.

**Unknown**: reasonable Unit granularity for a real task; the real human_minutes distribution; a reasonable `replication_factor`; a reasonable cap on rework rounds; how large a calibration batch needs to be; the real magnitude of result divergence between different models.

**Blocked**: any real calibration batch (no real requester or authorized data); splitting L1+ tasks (no controlled environment); cross-institution task splitting (no institutional contact).

---

## 10. Honest disclosure

- This document is a candidate draft: **unimplemented, never run, unverified**.
- The §5 example is explicitly marked `synthetic: true`; it is **not a real task, not pilot output, and does not represent any real requester or authorized data**.
- All workload figures are `basis: assumed`, with **no measured basis**.
- The calibration process has never been executed; this repository has no data for any of the metrics listed in §4.2.
