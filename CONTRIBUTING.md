# Contributing

Thanks for looking. Please read `README.md` first — in particular the boundary table.

## What this repository currently is

A **candidate discussion draft**. Documents, JSON Schemas, and synthetic fixtures. There is no
platform, no pilot, no participants, and no runtime. Contributing here means **helping criticize and
improve a specification**, nothing more.

## What is in scope

Only these:

1. **Specification discussion** — `PROPOSAL.md`, `spec/PROTOCOL_v0.2.md`,
   `spec/TASK_SPLITTING_v0.1.md`, `spec/CONTRIBUTION_v0.1.md`.
   Especially valuable: where the model breaks under real workloads, where a `MUST` is unenforceable,
   where a state machine has a missing edge, where a boundary claim is overstated.
2. **JSON Schema corrections** — `schemas/core/`. Wrong types, missing constraints, over-strict
   patterns, fields that should be forbidden but aren't.
3. **Conformance fixtures** — `conformance/`. New synthetic fixture sets, especially negative ones
   that the current checker fails to catch. Each set needs an `expected.json`.
4. **The local checker** — `scripts/validate_v02.py`. Bug fixes and honest additions. It must stay
   **Python standard library only**, with no install step and no network access.
5. **Documentation and translation** — the canonical `spec/`, `docs/`, schema README, and example
   documents are in English; their pre-translation Chinese source is preserved under `i18n/zh-CN/`.
   Corrections to the English documents and review of the Chinese mirrors are welcome.
6. **Telling us this is a bad idea** — with a reason. That is a legitimate contribution.

## What is out of scope

- **Any real data.** Do not submit real datasets, real documents, real images, or anything covered by
  someone else's authorization. All example content must be synthetic and marked `synthetic: true`.
- **Any credential.** No API keys, tokens, passwords, OAuth secrets, session cookies, `.env` files,
  connection strings, or account identifiers — not in code, not in fixtures, not in issue text, not
  in a screenshot. See `SECURITY.md`.
- **Personal information.** No names, emails, phone numbers, addresses, identifiers, or chat
  transcripts — yours or anyone else's. Participant references in fixtures use the `pseudo-` prefix
  and must stay pseudonymous.
- **Anything that presumes the project is real.** Please do not add organization registration details,
  sponsors, funding claims, real participants, real tasks, real beneficiaries, endorsements, service
  levels, or roadmap dates. If a change would make a reader believe OCC exists as an operating entity,
  it will be rejected.
- **Runtime implementation.** Control Plane, API, Runner, MCP adapter, ledger service, web UI. These
  are deliberately deferred (`spec/PROTOCOL_v0.2.md` §12.1). A specification with no implementation is
  the current point, not an oversight to fix.
- **Dependencies.** No `node_modules`, no virtualenvs, no lockfiles, no package manifests. The
  verification path must remain "clone and run `python3`".
- **External links**, except SPDX / license references and standards citations that the spec actually
  needs (e.g. RFC 2119). If you cite research or prior art, mark it `TODO: unverified` unless you have
  checked the primary source yourself, and record what you checked.

## How to raise something

**Issues** — for questions, design objections, spec ambiguities, and reports of overstated claims.
State which file and section, what you think is wrong, and what you would expect instead. If the
maintainers have not yet enabled issues (see `PUBLISH_CHECKLIST.md`), that decision is pending.

**Pull requests** — for concrete edits. Keep them small and single-purpose. Before opening one:

```bash
python3 -c "import json,pathlib; [json.loads(p.read_text(encoding='utf-8')) for p in pathlib.Path('.').rglob('*.json')]; print('json ok')"
python3 scripts/validate_v02.py
echo "exit=$?"
```

If you change anything under `examples/synthetic-action/`, recompute `checksums.json` — the file
hashes there are real and will otherwise be wrong. Note in your PR which hashes are real file hashes
and which fields remain object-level placeholders (the `content_hash` / `input_hash` zeros).

## Honesty conventions

The specs label every claim. Please keep this discipline in anything you add:

| Label | Meaning |
|---|---|
| `confirmed` | Supported directly by a primary source. |
| `observed` | Third-party report or measurement, not contradicted by the source. |
| `inferred` | Reasonably derived from facts, but derived. |
| `assumed` | A working assumption. Not established. |
| `unknown` | Not obtainable. Say so rather than guessing. |
| `deferred` | Intentionally postponed, direction known. |
| `blocked` | Has a specific unmet precondition. |

Synthetic data must be marked `synthetic: true`. Self-reported measurements must be marked
`self_reported: true`. Never present either as verified.

## What is not promised in return

No service, no compute, no platform access, no quota, no points, no ranking, no badge, no payment, no
guarantee that a proposal is adopted, and no guarantee of a response time. There is no maintainer
roster yet (see `PUBLISH_CHECKLIST.md`).

## Licensing of contributions

**The repository is licensed uniformly under the MIT License**. It applies to all documentation,
code, JSON Schemas, machine-readable fixtures, validation scripts, examples, and language mirrors.
See [`LICENSE`](LICENSE) for the full text.

By submitting a contribution you agree it may be distributed under the MIT License. Please do not
submit anything you would not be comfortable releasing under that license, and say in your PR if you
have licensing constraints.

**Inbound contribution terms are still pending.** The exact mechanism for accepting contributions —
DCO sign-off, a CLA, or inbound=outbound — is **not yet decided** (see `LICENSE_OPTIONS.md`). Until
that is finalized, contributions are understood as inbound=outbound by default pending a formal
decision, but no DCO or CLA requirement is in force yet.
