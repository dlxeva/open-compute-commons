# Open Compute Commons: Contribution Record Specification v0.1 (candidate draft)

> English is the authoritative public version of this document.
> Chinese mirror: [`spec/i18n/zh-CN/CONTRIBUTION_v0.1.md`](i18n/zh-CN/CONTRIBUTION_v0.1.md).

- **Status**: candidate draft — unpublished, unimplemented, and no real contribution record exists.
- **Date**: 2026-08-09.
- **Depends on**: `spec/PROTOCOL_v0.2.md` (§2.11, §11), `spec/TASK_SPLITTING_v0.1.md`.
- **Nature**: a candidate accounting-semantics contract. At present there are **no real participants, no real contributions and no real ledger**.

---

## 1. Design position

Three things this specification deliberately does not do, stated up front:

1. **No unified score.** There is no total, no level, and no leaderboard as a primary presentation. Contributions on different tracks are incommensurable in kind; forcing them into a single number manufactures false comparability.
2. **No token-to-impact conversion.** There is no formula converting contribution into influence, money, tokens or redeemable entitlements. What the ledger records is **process evidence**, not a certificate of impact.
3. **Activity volume is not treated as quality or impact.** Submitting 100 Units does not mean doing well, and doing well does not mean social impact was produced. These three things are recorded separately and read separately.

The reason: once a unified score exists, participants' behaviour optimizes toward the score, and the score is necessarily a poor proxy for every real goal. In a public-interest context this distortion is especially dangerous — it replaces "who was helped" with "how much was farmed".

---

## 2. Five contribution tracks

The tracks are **parallel**; there **MUST NOT** be any ranking of merit or conversion relationship between them.

### 2.1 Track R — Requirement & Domain

Providing real public requirements, data authorization, and domain acceptance criteria.

- Typical activities: raising a requirement, providing proof of authorization, defining domain acceptance rules, making L4 domain judgements, confirming that results are usable.
- Confirming events: the requirement is accepted into an Action, the TaskDefinition is frozen, an L4 judgement is completed.
- **This track is currently entirely empty**: there is no real requester (blocked).

### 2.2 Track E — Execution

Claiming Shards, executing, delivering.

- Typical activities: Claim, Attempt, Submission.
- Confirming events: a Submission reaches `accepted` or `partially_accepted`.
- Units of measure: number of accepted units, number of completed attempts (recorded separately).

### 2.3 Track Q — Quality

Review, spot checking, cross-checking, dispute arbitration.

- Typical activities: L3 cross-checking, L4 spot checking, participating in dispute arbitration, reporting defects.
- Confirming events: a Validation record is produced and adopted; a dispute conclusion is reached.
- Constraint: **MUST NOT** record Track Q accounting for one's own Submission (self-validation is forbidden).

### 2.4 Track P — Protocol Engineering

Improving the protocol, schemas, tooling, documentation and splitting methodology.

- Typical activities: proposing protocol revisions, writing/correcting schemas, writing validation tools, writing task package templates.
- Confirming events: a revision is merged into a version and frozen.
- Note: if the work in this repository in this round were to be accounted, it would belong to this track, and it is currently **not accounted** (there is no ledger).

### 2.5 Track S — Resource / Sponsorship

Providing credits, API budget, compute nodes, controlled execution environments.

- Typical activities: an institution donating quota, providing a controlled environment, bearing infrastructure costs.
- Confirming events: the resource is in place and usable, or controlled execution is completed.
- Constraint: **MUST NOT** record a personal subscription quota as a "donated resource" — personal subscriptions are held and used by the participant themselves (`account_custody: participant_self_custody`) and do not constitute a transfer of resources to the project.
- **This track is currently entirely empty**: there is no institutional contact (blocked).

### 2.6 Track comparison table

| Track | What is recorded | Confirmation prerequisite | Current status |
|---|---|---|---|
| R Requirement/Domain | Requirements, authorization, domain judgements | Requirement enters Action / L4 completed | blocked (no real requester) |
| E Execution | accepted units, attempts | Submission accepted/partially | none (no real execution) |
| Q Quality | Validations, arbitration | Validation adopted | none |
| P Protocol Engineering | Protocol/schema/tooling revisions | Revision merged and frozen | none (no ledger established) |
| S Resource | Credits, nodes, environments | Resource in place and usable | blocked (no institution) |

---

## 3. The three classes of evidence must stay separate

This is the core structural constraint of this specification. The three classes of evidence **MUST** be stored separately and presented separately, and **MUST NOT** be merged into a single number.

### 3.1 Activity Evidence

**What was done, and how much.**

- Examples: completed 12 Attempts; submitted 4 Submissions; participated in 3 spot checks; submitted 2 protocol revisions.
- Nature: **objective, countable, containing no judgement**.
- Recording prerequisite: the corresponding object exists and its state has been confirmed.
- **MUST NOT** be described as "size of contribution" or as "quality".
- Results of repeated execution that were not adopted (`not_selected`) **MUST** count toward activity evidence — the work really happened.

### 3.2 Quality Evidence

**How well it was done.**

- Examples: first-pass rate through L1/L2; L4 spot-check pass rate; distribution of rework rounds; number of judgements overturned in disputes.
- Nature: **relative, conditional, dependent on sample size**.
- Constraints:
  - Sample size **MUST** be attached. When the sample is too small it **MUST** be labelled `insufficient_sample`, and a ratio **MUST NOT** be presented.
  - **MUST NOT** be used to rank participants.
  - **MUST NOT** be derived from activity evidence (doing more ≠ doing better).
  - A single failure **MUST NOT** produce a persistent negative label; quality evidence is a distribution, not a rating.

### 3.3 Impact Evidence

**What actual effect was produced.**

- Examples: results adopted by the requester; cited by a downstream project; feedback from beneficiaries.
- Nature: **can only be confirmed by an external party; cannot be self-certified by the project**.
- Constraints:
  - Impact evidence **MUST** be declared by the requester or beneficiary, and **MUST NOT** be filled in by the project side or by participants themselves.
  - **MUST NOT** be derived from activity or quality evidence. Delivering 100 Units constitutes no impact claim whatsoever.
  - When there is no external confirmation it **MUST** be left empty and marked `unclaimed`, and output volume **MUST NOT** be substituted for it.
- **Current status: entirely empty.** There are no real results, no real adoption and no beneficiaries (blocked).

### 3.4 Why they must stay separate

Merging the three produces specific distortions:
- Activity + quality merged → a high-output, low-quality participant looks better than a low-output, high-quality one;
- Quality + impact merged → the project issues itself a certificate of influence;
- All three composed into one score → participants optimize the score rather than public value.

The cost of keeping them separate is that the ledger looks unattractive and cannot be ranked at a glance. This is intentional.

---

## 4. Minimum fields of a ContributionRecord

### 4.1 Field table

| Field | Strength | Type | Description |
|---|---|---|---|
| `record_id` | MUST | string | Unique identifier |
| `action_id` | MUST | string | The Action it belongs to |
| `contributor_ref` | MUST | string | **Pseudonymous identifier**; MUST NOT be an email, account or real name |
| `track` | MUST | enum | `R`\|`E`\|`Q`\|`P`\|`S` |
| `evidence_class` | MUST | enum | `activity`\|`quality`\|`impact` |
| `subject_type` | MUST | enum | Type of the associated object (submission / validation / unit, etc.) |
| `subject_id` | MUST | string | ID of the associated object |
| `confirming_event_id` | MUST | string | **The confirming event that triggered accounting** (§5) |
| `recorded_at` | MUST | date-time | Time of accounting |
| `status` | MUST | enum | `active`\|`revoked`\|`superseded` |
| `activity_measures` | SHOULD | object | Activity measures (only when evidence_class=activity) |
| `quality_measures` | SHOULD | object | Quality measures + the required `sample_size` |
| `impact_claim` | MAY | object | Impact claim + the required `claimed_by` (an external party) |
| `self_reported_usage` | MAY | object | Self-reported usage; MUST carry `self_reported: true` |
| `notes` | MAY | string | Notes |
| `revocation_reason_code` | conditional MUST | string | Required when status=revoked |

### 4.2 Forbidden fields (MUST NOT appear)

- `score` / `points` / `total` / `rank` / `level` / `tier` (any unified score or level)
- `impact_value` / `token_equivalent` / `credit_value` (any conversion)
- Any third-party account identifier, email address, API key or device fingerprint
- Any complete conversation transcript or PII without consent

These prohibitions are enforced by `additionalProperties: false` in `schemas/core/contribution_record.schema.json` and checked by the conformance fixtures.

### 4.3 Example (synthetic)

```json
{
  "record_id": "cr-synthetic-0001",
  "action_id": "act-synthetic-alttext-001",
  "contributor_ref": "pseudo-alpha",
  "track": "E",
  "evidence_class": "activity",
  "subject_type": "submission",
  "subject_id": "sub-synthetic-a-1",
  "confirming_event_id": "evt-synthetic-0007",
  "recorded_at": "2026-08-09T10:00:00+08:00",
  "status": "active",
  "activity_measures": {
    "accepted_units": 1,
    "rejected_units": 1,
    "completed_attempts": 1
  },
  "self_reported_usage": {
    "self_reported": true,
    "model_calls_range": "1-3"
  },
  "notes": "SYNTHETIC demonstration record; not a real contribution"
}
```

Note that `accepted_units: 1` and `rejected_units: 1` coexist — this is the normal accounting shape for partial acceptance, not an anomaly.

---

## 5. Accounting only after state confirmation

### 5.1 Rules

- A ContributionRecord **MUST** reference a `confirming_event_id`.
- That Event **MUST** already exist in the Event log, and **MUST** be one of the confirming events permitted in the table below.
- **MUST NOT** account while a Submission is in `received` / `validating`.
- **MUST NOT** account when a Claim is established (claiming is not a contribution).
- **MUST NOT** pre-record, provisionally record, or maintain "pending confirmation" accounting.

### 5.2 Confirming events per track

| Track | Permitted confirming events |
|---|---|
| R | `requirement.accepted`, `task_definition.frozen`, `validation.recorded`(L4) |
| E | `submission.accepted`, `submission.partially_accepted` |
| Q | `validation.recorded`(L3/L4), `dispute.resolved` |
| P | `protocol.version_frozen`, `schema.version_frozen` |
| S | `resource.available`, `controlled_execution.completed` |

### 5.3 Accounting under partial acceptance

- Record only the Units that **passed** as `accepted_units`.
- Units that did not pass are recorded as `rejected_units` (this is activity evidence, not a penalty).
- After successful rework, a **new** ContributionRecord **MUST** be produced; the original record **MUST NOT** be modified to change rejected into accepted.

### 5.4 Idempotency and accounting

- Repeated submission with the same `idempotency_key` **MUST NOT** produce a second ContributionRecord.
- The same `(subject_id, contributor_ref, evidence_class)` **MUST** have at most one `active` record.

### 5.5 Revocation

- When a problem is discovered afterwards (cheating, misjudgement, a dispute overturned), the original record **MUST** be set to `revoked` with `revocation_reason_code` filled in, and a new Event **MUST** be written at the same time.
- Records **MUST NOT** be deleted.
- Historical measures **MUST NOT** be modified silently.

---

## 6. Presentation constraints

If a public ledger interface exists in future:

- It **MUST** present content partitioned by track and evidence class;
- It **MUST NOT** offer a cross-track total or a global leaderboard as the main view;
- It **MUST** display the sample size next to quality evidence;
- It **MUST** display the declaring party next to impact evidence; where there is none, display `unclaimed`;
- It **MUST** display the `self_reported` marker on self-reported usage;
- It **MAY** provide a private view for participants to see their own history;
- It **MUST NOT** publish an individual participant's quality ratios by default.

---

## 7. Deferred / Unknown / Blocked

**Deferred**: the ledger interface, participants' private views, contribution export formats, cross-Action contribution aggregation, the concrete form of honours/acknowledgements.

**Unknown**: whether non-score incentives are enough to sustain participation (no participants, no data); a reasonable minimum sample size for quality evidence; whether the collection method for impact evidence is feasible; the Sybil resistance of pseudonymous identifiers.

**Blocked**: Track R (no real requester); Track S (no institutional contact); impact evidence (no real results and no beneficiaries); any real accounting (no ledger, no participants).

---

## 8. Honest disclosure

- This specification is a candidate draft and is **unimplemented**.
- **No real ContributionRecord, real participant or real ledger currently exists.**
- The examples in this document are marked SYNTHETIC; they are **not real contributions and not pilot output**.
- This specification makes no promise of entitlements to any participant — it explicitly stipulates that redeemable entitlements **do not exist**.
