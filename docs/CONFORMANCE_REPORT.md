# OCC v0.2 Conformance Report (v0.1, candidate draft)

> English is the authoritative public version of this document.
> Chinese mirror: [`docs/i18n/zh-CN/CONFORMANCE_REPORT.md`](i18n/zh-CN/CONFORMANCE_REPORT.md).

- **Generated on**: 2026-08-09 (from `date` at run time, not hard-coded)
- **Validator**: `scripts/validate_v02.py` (Python standard library only; no `jsonschema` dependency)
- **Python version**: 3.11.15 (runtime environment)
- **Commands**:

```bash
python3 scripts/validate_v02.py            # validate every fixture set under conformance/
python3 scripts/validate_v02.py conformance/valid   # validate a single set only
python3 scripts/validate_v02.py --list      # list the fixture sets
echo "exit=$?"                              # 0 if everything passed; 1 if anything mismatched
```

Exit code convention: returns **1** when a mismatch against `expected.json` is found (schema / state / invariant error counts differ, or an expected error code did not appear), and **0** when everything matches.

---

## Important statement: this is file-level candidate validation, not a live service certification

This repository is at the **C0 stage (no runtime implementation)** (see `spec/PROTOCOL_v0.2.md` §10/§12). `scripts/validate_v02.py`
is a **local, file-level data contract validator**. It:

- only checks whether the JSON fixtures on disk conform to the **statically checkable subset** of `schemas/core/*.schema.json`;
- only checks whether the fixtures are internally consistent (state transitions, key invariants, whether error codes are explicitly referenced);
- involves **no** Control Plane / API / Runner whatsoever, and therefore constitutes **no** service conformance certification (OCC C1–C3 are all unmet).

Any "pass" means only this: on the given fixtures, the local subset validation and invariant checks agree with that fixture's `expected.json`. It does **not** prove that a real system behaves correctly.

---

## Validator capabilities and honest limitations (built-in subset validator)

`scripts/validate_v02.py` embeds a **subset of JSON Schema draft-07**. Explicitly supported keywords:

| Keyword | Supported |
|---|---|
| `type` | ✅ |
| `required` | ✅ |
| `enum` | ✅ |
| `pattern` | ✅ (Python `re`; edge-case differences from ECMA-262 exist and are not normalized) |
| `minimum` / `maximum` | ✅ |
| `minLength` | ✅ |
| `minItems` | ✅ |
| `additionalProperties: false` | ✅ (this is the core mechanism preventing conversion fields such as `score`/`points`/`rank`/`token_equivalent` from entering a ContributionRecord) |
| `properties` | ✅ |
| `items` | ✅ |
| `$ref` to local `#/definitions/...` | ✅ |

**Explicitly unsupported (which must be stated honestly)**:

- `format` semantic validation (for example `date-time` and `sha256` are validated only by `pattern`; time validity is not checked).
- `allOf` / `anyOf` / `oneOf` / `not`.
- Remote `$ref` (cross-file / cross-URL).
- `patternProperties`, and `additionalProperties` as a schema object (only booleans are supported).
- `if` / `then` / `else`, `dependentRequired`, `dependencies`, `uniqueItems` and the remaining draft-07 keywords.
- Numeric precision / integer bounds, Unicode normalization and other fine details.

If `jsonschema` is installed in the environment, full draft-07 validation can be performed separately; this repository **neither depends on nor installs** it.

**Boundary on handling business error codes**: `expected_error_codes` compares against the codes **explicitly referenced** in the fixture data
(from `events.error_codes`, `validations.error_codes`, `submission.status_reason_code`,
`shard.prior_error_codes`), not against a re-derivation of semantic outcomes by the validator. That is: the validator verifies that these codes
"do appear in the data and were not silently removed", but does not independently judge "whether the code is correct". This is the honest boundary of a subset implementation.

---

## Results per fixture set

| Fixture set | schema | state | invariant | Result | Notes |
|---|---|---|---|---|---|
| `valid` | 0 | 0 | 0 | PASS | Fully compliant path; all objects pass |
| `partial_acceptance_rework` | 0 | 0 | 0 | PASS | Partial acceptance + rework; references `E_RULE_LENGTH_OUT_OF_RANGE` |
| `duplicate_idempotency` | 0 | 0 | 0 | PASS | Idempotent deduplication + replication distinction; references `E_DUPLICATE_SUBMISSION` |
| `invalid_redline` (negative) | 3 | 0 | 1 | PASS | Deliberately non-compliant; expected to report `E_SCHEMA_EXTRA_FIELD` ×2 and `E_INV_MISSING_CONFIRMING_EVENT` |

Exit code result: **all PASS (exit 0)**.

### Details

**valid** — all 11 objects conform to the schemas, with no state or invariant errors. The `ContributionRecord` references
`evt-synthetic-valid-004` (the submission.accepted confirming event).

**partial_acceptance_rework** — schema fully passes. The rework Shard `shard-synthetic-pa-a-rework-1`
contains only the failed Unit `unit-synthetic-012`, sets `parent_shard_id` pointing at the source Shard, and contains no Units that already passed
(invariant I-3 passes). `E_RULE_LENGTH_OUT_OF_RANGE` is explicitly referenced in `validations` and `events`.

**duplicate_idempotency** — schema fully passes. Core invariants verified:
- `sub-synthetic-dup-2` hits the same `idempotency_key` (`idem-sub-dup-0001`), with status `duplicate` and
  `duplicate_of = sub-synthetic-dup-1`, and **produces no second active ContributionRecord** (pseudo-alpha
  has only one active record, `cr-synthetic-dup-0001`, on track E).
- `sub-synthetic-dup-3` is produced by a different contributor (`pseudo-beta`) with a different `idempotency_key`
  (`idem-sub-dup-0003`); it is replication (repeated execution by design), produces its own valid CR, and is distinguished from idempotent
  deduplication (invariant I-2 passes).
- `E_DUPLICATE_SUBMISSION` is explicitly referenced in `events` / `submission.status_reason_code`.

**invalid_redline (negative test)** — deliberately non-compliant: the ContributionRecord carries the forbidden fields `score` and `points`
(caught by `additionalProperties:false`, `E_SCHEMA_EXTRA_FIELD` ×2), and lacks `confirming_event_id`
(`E_SCHEMA_MISSING_FIELD` + invariant `E_INV_MISSING_CONFIRMING_EVENT`). This fixture is marked
`negative_test: true`; it **enters no real-results or contribution narrative** and serves only to confirm that the validator can catch redlines and illegal states.

---

## Covered and not covered

### Covered (after the additions/fixes made in this wrap-up)

- required / type / enum / pattern / minimum / maximum / minLength /
  minItems / additionalProperties / properties / items / local $ref for the core schemas.
- State machine invariants:
  - Partial acceptance reworks only the failed Units (the rework Shard contains only failed Units and points at its parent).
  - A repeated idempotency key produces no second active ContributionRecord.
  - Replication is distinguished from duplicate (a different contributor/key is treated as legitimate replication).
  - A ContributionRecord must reference an existing `confirming_event_id`.

### Not covered / known gaps (listed honestly)

- **The CanonicalResult object**: `spec/PROTOCOL_v0.2.md` references it repeatedly, but `schemas/core/` has no separate schema for it,
  and the fixtures contain no `canonical_results.json`. Consequently invariant #4, "the number of active CanonicalResults for any Unit is ≤ 1",
  and "Shard completed ⇒ all Units have an active CanonicalResult" **cannot be expressed in this validator**, and are listed as deferred.
- **Format validation**: `date-time`, content validity and other `format` aspects are not validated (subset limitation).
- **Full draft-07**: `allOf/anyOf/oneOf/not/patternProperties/if-then-else` and similar are not implemented.
- **Exhaustive process-layer state machines**: only the statically decidable invariants above are checked; the full state transition table (for example, all edges other than `received → duplicate`) is not exhaustively validated.
- **Correctness of consensus/extrapolation**: the semantic correctness of `consensus_rule` and of the `extrapolated` marker is not judged automatically.
- **Real runtime behaviour**: this repository has no runtime, so every "pass" is only file-level internal consistency.

---

## Files covered by this report

- `scripts/validate_v02.py` — the validator itself.
- `schemas/core/*.schema.json` — the schemas applied.
- `conformance/valid/`, `conformance/partial_acceptance_rework/`,
  `conformance/duplicate_idempotency/`, `conformance/invalid_redline/` — the four fixture sets.

All fixtures are **synthetic**. `invalid_redline` is a **deliberately non-compliant negative set**; its "PASS" means
"the validator reported these errors as expected", not that the fixture is compliant.

---

## Reproducibility of a re-run

```bash
python3 scripts/validate_v02.py && echo "ALL PASS"
```

If `jsonschema` is installed in the environment, a full draft-07 comparison can be run in addition (it is not a dependency of this repository and is not executed in this report).
