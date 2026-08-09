# SYNTHETIC task instructions (target of instructions_ref)

> English is the authoritative public version of this document.
> Chinese mirror: [`examples/synthetic-action/i18n/zh-CN/instructions.md`](i18n/zh-CN/instructions.md).

> **This file is a synthetic demonstration.** It is what `instructions_ref` in `task_definition.json` points at, and it illustrates what "frozen task semantics" look like at the file level.
> It is **not** a real task instruction, there is **no** real task owner, and it **cannot** substitute for working guidance under real authorized data.

## Task goal (synthetic)

Write an objective description for each Unit's input (the synthetic placeholder that `input_ref` points at).

## Output requirements

| Item | Requirement |
|---|---|
| Format | A single paragraph of plain text, written into `unit_result.output` |
| Length | 40–200 characters (inclusive) |
| Tone | Objective description; MUST NOT invent facts that are not present in the input |
| Sensitive content | MUST NOT contain PII, credentials or L1+ sensitive content (redline rule) |

## When it cannot be completed

MUST NOT silently omit it. Set that Unit's `outcome` to `skipped` and attach a `skip_reason_code` (format `E_[A-Z_]+`).
A Submission MUST cover all Units of the Shard it belongs to.

## Rework

If a Unit fails acceptance, the original Shard moves to `rework_required` and a derived rework Shard takes over, and that rework Shard **contains only the Units that did not pass**. Units that already have a CanonicalResult MUST NOT be re-included.

## Boundary

- These instructions create no obligation for anyone.
- There is no claiming entry point, no submission entry point and no reviewer. This package is not executable.
