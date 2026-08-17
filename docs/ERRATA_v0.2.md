# Known Contradictions in OCC v0.2

- **Status:** candidate errata note, 2026-08-12.
- **Scope:** confirmed contradictions in the files currently published in this repository.
- **Effect:** this note does not amend the protocol, repair the fixtures, or certify conformance.

The items below can be established directly from the repository. They are recorded so reviewers do
not have to infer a resolution that the draft has not made.

## E-001 — Publication status is stale

`spec/PROTOCOL_v0.2.md` describes itself as "unpublished" in its header and honest disclosure. Its
blocked-items table also says that publishing the repository is out of scope. The protocol is now in
this public repository.

**Confirmed effect:** "unpublished" is no longer an accurate repository-status statement. Publication
does not imply adoption, implementation, deployment, endorsement, or a completed pilot; none of those
has occurred.

## E-002 — v0.2 delegates material to an unavailable v0.1

Section 0 of `spec/PROTOCOL_v0.2.md` says that role definitions, the institutional supplementary
track, and a co-design question list continue to be governed by v0.1. Section 13 says v0.1 is not in
this repository and has not been reviewed for publication.

**Confirmed effect:** a public reader cannot inspect the document that v0.2 names as governing this
material. Those areas are not reviewable as part of the public v0.2 package.

## E-003 — Object counts and schema coverage do not match

The v0.2 revision table says that the protocol contains 11 first-class objects. Section 2 names 12:
Action, TaskDefinition, Unit, Shard, Claim, Attempt, Submission, Validation, CanonicalResult,
ContributionRecord, Release, and Event.

`schemas/core/` contains schemas for 10 of those types. It has no separate schema for
CanonicalResult or Release. `schemas/core/README.md` also lists Dispute as a defined object without a
schema. At the same time, the C1 profile says that all core objects validate against `schemas/core/`,
and `docs/CONFORMANCE_REPORT.md` says that "all 11 objects" conform.

**Confirmed effect:** the published files do not define one consistent object count or complete schema
coverage for the named core model. The current checker cannot establish the C1 statement that all
core objects validate.

## E-004 — The idempotency fixture creates the second record that the protocol forbids

Sections 3.4 and 4.3 of `spec/PROTOCOL_v0.2.md` say that a repeated Submission with the same
`idempotency_key` must return the first result and must not create a second record.

`conformance/duplicate_idempotency/submissions.json` nevertheless contains a second Submission,
`sub-synthetic-dup-2`, with `status=duplicate`. Its events file also contains a transition for that
second Submission. The checker only verifies that the duplicate did not produce a second active
ContributionRecord, so the fixture still reports PASS.

**Confirmed effect:** PASS for this fixture does not demonstrate the idempotency behavior required by
the protocol. It demonstrates the narrower behavior implemented by the checker.

## E-005 — A "fully compliant" completed Shard has no CanonicalResult

Section 3.5 of `spec/PROTOCOL_v0.2.md` requires every Unit in a completed Shard to have an active
CanonicalResult. The `conformance/valid/` fixture marks its Shard `completed` but contains no
`canonical_results.json`. `docs/CONFORMANCE_REPORT.md` calls that fixture a "fully compliant path"
and reports zero invariant errors, while its known-gaps section correctly states that the checker
cannot express this invariant.

**Confirmed effect:** the zero-error result is only a result from the checker's implemented subset. It
does not establish that the fixture satisfies all protocol invariants.

## How to read validation results until these contradictions are resolved

A PASS means that the checker produced the counts recorded in that fixture's `expected.json`. It
must not be read as proof that the fixture conforms to every normative statement in v0.2, that the
protocol is internally complete, or that a runtime works. No runtime exists.

This errata note records the contradictions only. A later, separately reviewed change may decide
whether to revise the protocol, schemas, fixtures, checker, conformance terminology, or versioning.
