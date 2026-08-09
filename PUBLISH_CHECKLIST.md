# Publish Checklist — Confirmed Publication Settings

This repository candidate was assembled from a local draft. The publication settings below have been
**confirmed by the user**. This checklist records them so the repository is internally consistent; it
does not itself create the remote repository, commit, or push. Those release-operator actions are
handled separately after this content review.

Publishing to a public host is irreversible in practice — content gets indexed, mirrored, and cached
even if a repository is later deleted or made private. Treat these as gates, not suggestions.

---

## Gate 1 — Repository name

**Decided: `open-compute-commons`.** Owner/slug = `dlxeva/open-compute-commons`.

- "Open Compute Commons" is the working title; it is now confirmed as the repository name for
  publication. "Open Compute" is close to established industry names — the README disclaims any
  affiliation that does not exist, and no institution has reviewed or endorsed this.

## Gate 2 — Owner / namespace

**Decided: `dlxeva` (personal account).**

- Published under a personal account. No legal entity exists; the publisher acts personally.
- The README disclaims institutional backing and endorsement.

## Gate 3 — Public or private

**Decided: public (open source).**

- The draft is intended for pre-build criticism, which a public repository serves. Publication is
  effectively permanent (indexed, mirrored, cached), which the publisher has accepted.

## Gate 4 — License

**Decided: dual license, split by file type.** See `LICENSE_OPTIONS.md` for the decision record and
`README.md` for the fixed boundary.

- Documentation / prose → **CC BY 4.0** (`LICENSE-DOCS.md`).
- Code / JSON Schemas / fixtures → **Apache-2.0** (`LICENSE`).
- Inbound contribution terms (DCO / CLA / inbound=outbound) remain an open follow-up.

## Gate 5 — Maintainers and contact point

**Decided: no public email / no named public contact email.**

- No public mailbox is published. The README and this checklist state there is no public email
  address. Security reports go to public Issues (see Gate 6); no private contact channel is exposed.

## Gate 6 — Security reporting route

**Decided: public GitHub Issues only (for now).**

- Private vulnerability reporting / GitHub security advisories are **not** enabled at this time.
- `SECURITY.md` states plainly that there is no private channel and that reporters should use public
  Issues, describing the type and location of any issue without pasting secrets.
- Enabling private reporting later remains a possibility and would be reflected in `SECURITY.md` if
  adopted.

## Gate 7 — Issues and discussions

**Decided:**

- Issues: **enabled.**
- Discussions: **disabled.**
- Pull requests: accepted at this stage (review draft), subject to the no-secret / synthetic-only
  rules.
- Issue templates should repeat the "no real data, no credentials, no PII" rule at submission.

`CONTRIBUTING.md` tells readers to open issues, which is consistent with Issues being enabled.

---

## Pre-publication content review

Independent of the gates, a human should confirm:

- [x] No absolute local paths (`/Users/…`, `/private/tmp/…`, `/home/…`), machine names, or internal
  infrastructure references.
- [x] No credentials, API keys, tokens, passwords, or third-party account identifiers.
- [x] No real personal data; all `contributor_ref` values remain `pseudo-` pseudonyms.
- [x] All example and fixture content is marked `synthetic: true`; nothing real or unauthorized.
- [x] No claim implying an organization, pilot, participant, requester, endorsement, funding, or
  delivered compute exists. Spot-check `README.md`, `PROPOSAL.md`, and `spec/PROTOCOL_v0.2.md`.
- [x] No external links beyond license/SPDX references and standards citations the spec needs.
- [x] Unverified research or prior-art claims are marked `TODO: unverified` (none are asserted in
  this candidate).
- [x] `spec/PROTOCOL_v0.2.md` §13 correctly describes which earlier files are *absent* from this
  repository — v0.1 protocol, institutional-allocation schemas, cases, and the simulation script were
  deliberately excluded and were **not** copied here.
- [x] Confirm this repository omits internal experiment records by design; if anyone wants them
  published, that is a separate review.
- [x] No `node_modules/`, virtualenv, `__pycache__/`, build output, or lockfiles.
- [x] `.gitignore` is included before the first commit.

## Verification to re-run immediately before publishing

```bash
python3 -c "import json,pathlib; [json.loads(p.read_text(encoding='utf-8')) for p in pathlib.Path('.').rglob('*.json')]; print('json ok')"
python3 scripts/validate_v02.py; echo "exit=$?"
python3 -c "import hashlib,json,pathlib; d=pathlib.Path('examples/synthetic-action'); m=json.loads((d/'checksums.json').read_text(encoding='utf-8')); [print(('OK  ' if hashlib.sha256((d/f['path']).read_bytes()).hexdigest()==f['sha256'] else 'FAIL'), f['path']) for f in m['files']]"
```

All three must be clean. If any file under `examples/synthetic-action/` was edited during review,
`checksums.json` must be regenerated — the `files[].sha256` values are real file hashes, while the
`content_hash` / `input_hash` fields inside the JSON objects remain intentional zero placeholders.

## Not in scope for this checklist

The repository content does not authorize or perform deployment, contacting any person or
institution, posting to any community, registering an entity, or spending money. Creating the
GitHub remote, committing, pushing, and (if needed) opening a pull request are release-operator
actions handled outside this checklist; they do not imply that any organization, pilot, recruitment,
or external execution exists.
