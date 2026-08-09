# License Options — Decision Record

> **Decision made.** This repository is licensed under a **dual** arrangement, split by file type:
>
> - **Documentation / prose** → Creative Commons Attribution 4.0 International (`CC-BY-4.0`). Full text: `LICENSE-DOCS.md`.
> - **Code, JSON Schemas, fixtures** → Apache License 2.0 (`Apache-2.0`). Full text: `LICENSE`.
>
> The exact file boundary is fixed in `README.md`, and restated identically in `LICENSE` and
> `LICENSE-DOCS.md`. This file retains the options analysis so the rationale is auditable; the
> options are no longer open.

## What the decision had to resolve

Licensing has legal consequences that outlast the draft, so two questions were settled before it
was applied:

- **Who holds the rights.** The repository is published as `dlxeva/open-compute-commons`, and that
  account is the rights holder for the purpose of applying these licenses. No legal entity exists
  behind the project, and none is claimed; attribution runs to the repository, not to an institution.
- **The content is mixed.** Prose, schemas, and a script are conventionally licensed differently.
  Applying one license to everything would have been a choice, not a default — so the dual
  arrangement below was chosen deliberately.

## The material splits into two kinds

| Kind | Files | Applied license |
|---|---|---|
| **Documentation / prose** | `README.md`, `PROPOSAL.md`, `spec/**/*.md`, `docs/**/*.md`, `schemas/core/**/*.md`, `CONTRIBUTING.md`, `SECURITY.md`, this file, `PUBLISH_CHECKLIST.md`, `LICENSE-DOCS.md`, `examples/synthetic-action/**/*.md` | CC BY 4.0 |
| **Code, schemas, fixtures** | `scripts/*.py`, `schemas/core/*.json`, `conformance/**/*.json`, `examples/synthetic-action/*.json` | Apache-2.0 |

A dual arrangement — one license for prose, one for code — is common for specification repositories.
A single permissive license for everything would have been viable and simpler; the dual split was
chosen anyway, and the sections below record why. They describe the reasoning behind a decision that
has been made, not a menu of choices still open.

## Option A — Documentation

### CC BY 4.0 (`SPDX-License-Identifier: CC-BY-4.0`)

- Allows reuse, adaptation, and commercial use with attribution.
- Widely understood for specifications and written material.
- Attribution is exactly what a draft seeking criticism benefits from.
- Consideration: CC licenses are not designed for software, which is why the split exists.

### Alternatives, if CC BY is not wanted

- **CC BY-SA 4.0** — adds copyleft on adaptations. Keeps derivative specs open; also constrains who
  can incorporate the text.
- **CC0 1.0** — public-domain dedication, no attribution requirement. Maximum reuse, no credit trail.
- **CC BY-NC** — **not recommended.** "Non-commercial" is ambiguous in practice and is not considered
  an open license; it would block legitimate use by the very organizations this proposal wants to
  reach.

## Option B — Code, schemas, and fixtures

### Apache-2.0 (`SPDX-License-Identifier: Apache-2.0`)

- Permissive, with an **express patent grant** and a contributor patent-retaliation clause.
- Includes an explicit warranty disclaimer and a `NOTICE` mechanism.
- Preferred where implementations might be built by companies; the patent grant is the main reason to
  choose it over MIT for a protocol specification.
- Consideration: longer, and requires preserving notices.

### MIT (`SPDX-License-Identifier: MIT`)

- Permissive and very short; near-universally recognized.
- Consideration: **no explicit patent grant.** For a specification that others may implement, that
  gap is the usual argument for Apache-2.0.

### Alternatives

- **BSD-3-Clause** — comparable to MIT, adds a no-endorsement clause.
- **Apache-2.0 OR MIT** (dual, contributor's choice) — common in some ecosystems; maximizes downstream
  compatibility at the cost of explanation.

## How the decision resolved each point

1. **Should implementers get a patent grant?** Yes — the goal is for other people to build systems
   from this protocol, so Apache-2.0 was chosen over MIT for the express patent grant.
2. **Should derivative specifications stay open?** CC BY was chosen over CC BY-SA: attribution is
   required, copyleft on adaptations is not.
3. **Does attribution matter?** Yes — hence CC BY rather than CC0.
4. **Is the split worth the complexity?** Judged yes, on condition that the boundary is stated
   identically in `README.md`, `LICENSE`, and `LICENSE-DOCS.md` so the added complexity costs the
   reader one lookup and no ambiguity.
5. **Is licensing across the file boundary clear?** Yes. The boundary is drawn by file extension:
   `*.md` is CC BY 4.0 everywhere, including inside `examples/synthetic-action/`; `*.json` and
   `*.py` are Apache-2.0. Only a file's own SPDX header overrides that.
6. **Are contributions covered?** The applicable file license is stated in `CONTRIBUTING.md`.
   The choice between plain inbound=outbound, a DCO, or a CLA has not been made. This is the main
   remaining follow-up.
7. **Does the owner actually hold the rights?** Resolved for publication purposes: the repository is
   published as `dlxeva/open-compute-commons` and the licenses are applied on that basis.

## Applied — and what is left

Done:

1. Full license texts are present: `LICENSE` (Apache-2.0) and `LICENSE-DOCS.md` (CC BY 4.0).
2. The split is stated explicitly in `README.md`, with the same path table in `LICENSE-DOCS.md`.
3. `SPDX-License-Identifier:` headers are present in both license files; a per-file header, where
   one exists, overrides the path tables.

Remaining follow-ups:

4. State the inbound contribution terms (DCO / CLA / inbound=outbound) in `CONTRIBUTING.md` once a
   decision is made. The applicable file licenses are already stated there; no license decision is
   pending.
5. **Long-term maintenance responsibility is unassigned.** No maintainer has been named, so there is
   currently no one designated to answer license questions, accept a CLA, or relicense. This does not
   affect the licenses already applied, which stand as published.

This file is kept as the decision record. It should be superseded only once items 4 and 5 are
resolved.

## Status

| Item | Status |
|---|---|
| Documentation license | **CC BY 4.0** (decided) — `LICENSE-DOCS.md` |
| Code / schema / fixture license | **Apache-2.0** (decided) — `LICENSE` |
| Single vs. dual license | **Dual, split by file type** (decided) — boundary fixed in `README.md` |
| File boundary (`*.md` vs `*.json` / `*.py`) | **Fixed** (decided) — identical in `README.md`, `LICENSE`, `LICENSE-DOCS.md` |
| Rights holder | **dlxeva/open-compute-commons** (confirmed) — owner/slug for publication |
| Inbound contribution terms (DCO / CLA / inbound=outbound) | **Open follow-up** — no DCO, CLA, or inbound=outbound policy has been finalized |
| Long-term maintenance responsibility | **Open follow-up** — no maintainer named |

The licensing decision itself is closed: the dual arrangement, the file boundary, and the rights
holder are all settled and applied, and item 4 in `PUBLISH_CHECKLIST.md` is closed with them. The two
open follow-ups above concern contribution process and maintenance, not which licenses apply.

*License names and SPDX identifiers referenced here are standard identifiers from the SPDX license
list; consult the authoritative license texts before adopting one. This file is not legal advice.*
