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
- **Anything that presents OCC as an operating project.** Please do not add organization registration
  details, sponsors, funding claims, operational participants, accepted requesters, active tasks,
  claimed beneficiaries, endorsements, service levels, or roadmap dates. A safely abstracted
  candidate public need may be discussed through the Issue form below, but it must not be described
  as accepted, scheduled, supplied, or served by OCC. If a change would make a reader believe OCC
  exists as an operating entity, it will be rejected.
- **Runtime implementation.** Control Plane, API, Runner, MCP adapter, ledger service, web UI. These
  are deliberately deferred (`spec/PROTOCOL_v0.2.md` §12.1). A specification with no implementation is
  the current point, not an oversight to fix.
- **Dependencies.** No `node_modules`, no virtualenvs, no lockfiles, no package manifests. The
  verification path must remain "clone and run `python3`".
- **Unnecessary or unsafe external links.** Repository-owned Issue-form links, SPDX / license
  references, and standards citations that the spec actually needs are allowed. A candidate-need
  Issue may also cite a directly relevant primary source that is public and accessible without login.
  Private shares, access-granting URLs, unpublished material, and links that merely replace a safe
  description are prohibited. If you cite other research or prior art, mark it `TODO: unverified`
  unless you have checked the primary source yourself and record what you checked.

## How to raise something

**Issues are the primary discussion channel.** Use the
[design critique form](https://github.com/dlxeva/open-compute-commons/issues/new?template=design-critique.yml)
for questions, design objections, spec ambiguities, and reports of overstated claims. Use the
[candidate public need form](https://github.com/dlxeva/open-compute-commons/issues/new?template=candidate-public-need.yml)
to test the draft against a safely described, public-interest need. State which file and section you
are responding to, what you think is wrong or missing, and what result you would expect instead.

Do not put real task inputs, personal information, credentials, private links, or unpublished
material in an Issue. Candidate needs must be described at a level that is safe to publish. A public,
no-login primary-source link may be included only when it is necessary to explain an already-public
need; never use a private share link or a link that grants access.

**Pull requests** — for concrete edits. Keep them small and single-purpose. For any substantial
change — including a new protocol mechanism, governance rule, schema family, or change to a safety
boundary — open an Issue first and wait for the design direction to be discussed. External pull
requests may be submitted, but submission does not imply review, acceptance, or merge. Before
opening one:

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
DCO sign-off, a CLA, or a formally adopted inbound=outbound policy — is **not yet decided** (see
`LICENSE_OPTIONS.md`). Until that is finalized, the repository's working treatment is
inbound=outbound for the applicable file license above, and no DCO or CLA requirement is in force.
This working treatment does not promise that a contribution will be accepted or merged. If those
terms are not acceptable to you, open an Issue describing the concern without submitting proposed
text or code.
