# examples/synthetic-action — SYNTHETIC sample task package

> English is the authoritative public version of this document.
> Chinese mirror: [`examples/synthetic-action/i18n/zh-CN/README.md`](i18n/zh-CN/README.md).

> **Status**: synthetic demonstration, 2026-08-09. Corresponds to `spec/PROTOCOL_v0.2.md` (candidate draft) and `schemas/core/`.

## In one sentence

This is a set of **declarative files** showing what an OCC Action Package looks like **at the file level**. It **cannot be executed**, has **no real task owner**, and **produces no results**.

## What it explicitly is not

| It is not | Explanation |
|---|---|
| A real pilot | No pilot has happened. No participants, no claims, no submissions, no acceptance. |
| Public-benefit output | The content is entirely placeholder strings with no use value to anyone. |
| A substitute for real authorized data | `input_ref` points at a `synthetic://` placeholder, not at any real file. A real task MUST have a real `authorization_ref`. |
| Runnable software | This directory **contains no executable code**, and by convention **none may be placed here**. Integrity checks are run with an external ad-hoc command. |
| Evidence of workload | Every `workload_envelope.basis` is `assumed`, `calibration_status=not_started`, with no measurements at all. |

## File list

| File | Role | Corresponding schema |
|---|---|---|
| `README.md` | This file | — |
| `manifest.json` | Package manifest and boundary declarations | — |
| `action.json` | Action container (data_policy / execution_policy) | `schemas/core/action.schema.json` |
| `task_definition.json` | Frozen task semantics and acceptance_policy | `schemas/core/task_definition.schema.json` |
| `units.json` | 3 synthetic Units (acceptance atoms) | `schemas/core/unit.schema.json` |
| `shards.json` | 2 Shards (claim atoms), including 1 rework Shard | `schemas/core/shard.schema.json` |
| `acceptance_policy.json` | A readable copy of the acceptance policy | — |
| `instructions.md` | The task instructions that `instructions_ref` points at | — |
| `checksums.json` | Integrity manifest | — |

## The path being demonstrated

```
shard-synthetic-sample-a  (unit-001, unit-002, unit-003)
        │
        ├── unit-001  passed
        ├── unit-002  failed  → E_RULE_LENGTH_OUT_OF_RANGE
        └── unit-003  passed
        │
        ▼  the original Shard MUST NOT be reopened in place; it moves to rework_required
shard-synthetic-sample-a-rework-1  (contains only unit-002)
        parent_shard_id = shard-synthetic-sample-a
        rework_round    = 1
```

The key point: **a rework Shard contains only the Units that did not pass.** unit-001 and unit-003, which passed, already have CanonicalResults and MUST NOT be re-included — otherwise the same work would be metered twice.

The verdicts on this path were **worked out by hand and written into the files**; they were not computed by any program. No validation service has read these files.

## Integrity check

The entries under `algorithm=sha256` in `checksums.json` are **real computed hashes**, and can be recomputed and checked with the Python standard library:

```
python3 -c "import hashlib,json,pathlib; d=pathlib.Path('examples/synthetic-action'); m=json.loads((d/'checksums.json').read_text()); [print(('OK  ' if hashlib.sha256((d/f['path']).read_bytes()).hexdigest()==f['sha256'] else 'FAIL'), f['path']) for f in m['files']]"
```

(Run from the repository root. `checksums.json` itself is not in the list being checked — it cannot contain its own hash.)

### Which values are demonstration placeholders

Two classes of hash must be kept distinct:

| Class | Location | Real or not |
|---|---|---|
| **File hashes** | `files[].sha256` in `checksums.json` | **Real.** sha256 over the file bytes; recomputable and checkable. |
| **Object content_hash** | The `content_hash` / `input_hash` fields inside each JSON, all sixty-four `0`s | **Demonstration placeholders.** A real implementation MUST compute them over the canonical serialization (sorted keys, UTF-8, excluding `content_hash` itself); this sample **does not implement that canonicalization**. |

In other words: the file-level integrity mechanism is **genuinely checkable**; the object-level `content_hash` is only a **placeholder in field shape**. `spec/PROTOCOL_v0.2.md` §4.2 describes the correct algorithm, and this package does not implement it.

## Boundary

- This package contains no external links. All references are repository-relative paths or `synthetic://` placeholders.
- This package requires no network access.
- Sensitivity level L0, no PII. The project **does not process L1+ data** and **does not take custody of accounts**.
- After modifying any file in this package, the corresponding hash in `checksums.json` becomes invalid and must be recomputed.
