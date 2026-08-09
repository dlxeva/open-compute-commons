# Security

## Scope

This repository contains documents, JSON Schemas, synthetic fixtures, and one standard-library Python
script. **There is no service, no API, no server, no runtime, and no user data.** So there is no
production system to attack and no incident response to run.

What *can* still go wrong here is worth reporting, and falls into two groups:

1. **Content risks** — something in this repository that would cause harm if a reader acted on it,
   or that should never have been committed.
2. **Design risks** — a flaw in the specification that would create a real vulnerability in any
   system built to it. Since the point of a draft is to be attacked before implementation, this is
   the most useful kind of report.

## Do not upload secrets — ever

This is the single most important rule for this repository.

Never include, in a commit, a fixture, an issue, a pull request, a comment, a log paste, or a
screenshot:

- API keys, access tokens, OAuth tokens, refresh tokens, session cookies, bearer tokens;
- passwords, passphrases, private keys, certificates, SSH keys, `.env` files;
- database connection strings, internal hostnames, internal URLs;
- third-party account identifiers or emails;
- personal data of any kind — yours or anyone else's.

The specification forbids the project from ever holding these
(`spec/PROTOCOL_v0.2.md` §9.3, `account_custody: participant_self_custody`). That constraint is
worthless if credentials leak into the repository through a fixture or a bug report.

**If you have already pushed a secret**: treat it as compromised. Rotate or revoke it immediately at
the issuing provider — that is the only action that actually helps. Rewriting git history does not
un-leak a value. Then tell the maintainers so the content can be removed, and say **what kind** of
credential it was without pasting it again.

## Report these

### In repository content
- A credential, token, key, or password of any kind.
- Real personal data (PII) in a fixture, example, or document — including anything that de-anonymizes
  a `pseudo-` identifier.
- Real, non-public, or unauthorized data used as example content. Everything here must be synthetic.
- Absolute filesystem paths, machine names, internal infrastructure details, or anything else leaking
  a private working environment.
- Executable code in a place where the documents promise there is none — notably
  `examples/synthetic-action/`, which declares `executable_code_present: false`.
- Any claim that overstates reality: implying a pilot happened, participants exist, compute is
  provided, an organization is registered, or an institution endorsed this. Report these as security
  issues, because false trust is the harm this project is most likely to cause.

### In the specification design
- **Prompt injection.** A task package's `instructions.md`, an `input_ref` target, or a unit's input
  is untrusted content that will be fed to a model. Where does the spec fail to require treating it
  as data rather than instructions? Where could injected text cause a participant to exfiltrate
  something, alter their submission, or attack the validation layers?
- **Malicious task packages.** A hostile Action or TaskDefinition designed to trick participants into
  processing prohibited data, running code, visiting a hostile endpoint, or leaking their own
  environment. Where do the L1/L2 checks and the `data_policy` / `execution_policy` fields fail to
  catch this?
- **PII and sensitivity leaks.** Paths by which L1+ data could reach the public claiming track despite
  §8.1, or by which Events / the public ledger could accumulate PII despite §9.4.
- **Credential exposure paths.** Any place the object model, an adapter, or a workflow could end up
  requesting, storing, proxying, or logging a participant's third-party credentials — violating §9.3.
- **Supply chain.** `scripts/validate_v02.py` must remain standard-library-only. Report any
  introduced dependency, any instruction that would have a reader install or execute untrusted code,
  and any schema `$ref` that resolves off-repository.
- **Integrity and accounting.** Ways to forge, replay, or double-count: idempotency bypass (§4.3),
  duplicate contribution records (§11), silent rewrite of append-only records (§4.4), lease hoarding
  (§5), self-validation (§7.2), or Sybil identities behind `contributor_ref`.

## Already-known residual risks

These are documented, not accepted as fixed (`spec/PROTOCOL_v0.2.md` §9.2). Reports that go beyond
restating them are welcome:

- Whether participants actually follow instructions can only be checked by self-audit and sampling.
- Self-reported usage is unverifiable by construction.
- Sybil attacks / multiple pseudonyms are not defended against.
- A participant's own environment may be compromised; the project cannot see or control it.
- Data handling on the third-party model service side is outside the project's control.
- The local checker implements only a **subset** of JSON Schema draft-07 — it will not catch
  everything (`docs/CONFORMANCE_REPORT.md`).

## How to report

**Security reports: public GitHub Issues only (for now).** This was decided for publication
(see `PUBLISH_CHECKLIST.md`). There is **no private channel** and no GitHub security advisory enabled
at this time. If private vulnerability reporting is enabled later, this file will be updated to match.

Do not send anything you would not be willing to have read publicly, and above all do not paste a
secret into a public issue in order to report it — describe its type and location instead. Enabling
private reporting later remains a possibility; the absence of a private channel today is a deliberate
current choice, not a permanent constraint.

There is no bug bounty, no severity SLA, and no guaranteed response time.
