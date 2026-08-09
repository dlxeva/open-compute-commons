# schemas/core/ — OCC v0.2 core object schemas

> English is the authoritative public version of this document.
> Chinese mirror: [`schemas/core/i18n/zh-CN/README.md`](i18n/zh-CN/README.md).

- **Status**: candidate draft, 2026-08-09.
- **Corresponding documents**: `spec/PROTOCOL_v0.2.md`, `spec/TASK_SPLITTING_v0.1.md`, `spec/CONTRIBUTION_v0.1.md`.

## Scope

This directory is the **only** schema collection in this repository, corresponding to the core object model of protocol v0.2.

Earlier experiments also produced another batch of schemas oriented toward "institutional applications and compute allocation" (application / review / allocation /
execution_record / acceptance_record) together with their simulation scripts. They are **not included in this repository**: that material belongs to
the v0.1 period of exploration, has not been reviewed, and is not suitable as a starting point for public discussion. The schemas in this directory do not overlap with them.

## Files in this directory

| File | Object | Role |
|---|---|---|
| `action.schema.json` | Action | Action container; contains data_policy / execution_policy |
| `task_definition.schema.json` | TaskDefinition | Frozen task semantics and acceptance_policy |
| `unit.schema.json` | Unit | **Acceptance atom** |
| `shard.schema.json` | Shard | **Claim atom** |
| `claim.schema.json` | Claim | Lease (lease / timeout) |
| `attempt.schema.json` | Attempt | **Execution-metering atom** |
| `submission.schema.json` | Submission | Delivery; contains `definitions/unit_result` |
| `validation.schema.json` | Validation | One layer of the four-layer validation |
| `contribution_record.schema.json` | ContributionRecord | Accounting entry |
| `event.schema.json` | Event | Append-only state change |

Objects with no separate schema: `CanonicalResult`, `Release`, `Dispute` — their semantics are already defined in `spec/PROTOCOL_v0.2.md` §2.10 / §2.12 / §7, and their schemas are listed as deferred (this round's fixtures do not cover validating them separately).

## How to validate

```bash
python3 scripts/validate_v02.py
```

That script uses **only the Python standard library** and embeds a **subset** validator for JSON Schema draft-07 (supporting type / required / enum / pattern / minimum / maximum / minLength / minItems / additionalProperties / properties / items / local `$ref` references).

**Limitation**: it is not a complete draft-07 implementation. `format` semantic validation, `allOf`/`anyOf`/`oneOf`/`not`, remote `$ref`, `patternProperties` and others are not implemented. If `jsonschema` is installed in the environment, full validation can be run separately; this repository **does not depend on** it and **does not install** it.

## Design constraints (enforced in the schemas)

- `additionalProperties: false` appears throughout the objects, to prevent unified-score and conversion fields such as `score` / `points` / `rank` / `token_equivalent` from entering a ContributionRecord.
- `contributor_ref` / `actor_ref` use the `^pseudo-` pattern, which blocks email addresses, real names and third-party account IDs.
- `execution_policy.account_custody` is a single-value enum, `participant_self_custody`, which fixes "the project does not take custody of accounts" at the structural level.
- `self_reported` is the constant `true`, preventing self-reported usage from being disguised as verified metering.
- Every object supports a `synthetic: true` marker, used to distinguish demonstration data from real data (which does not yet exist).

## Boundary

These schemas are a **candidate data contract**. No live service consumes them; there is no Control Plane, no API and no Runner. Their only current use is local file validation and discussion.
