<!-- SPDX-License-Identifier: CC-BY-4.0 -->

## Purpose

<!-- Explain one concrete change. For a substantial change, link the design Issue opened first. -->

Related Issue:

## Scope

<!-- List the files or sections changed and what is intentionally unchanged. -->

## Public-safety check

- [ ] This PR contains no real task inputs, datasets, documents, images, or beneficiary records.
- [ ] This PR contains no PII, names, emails, account identifiers, or private transcripts.
- [ ] This PR contains no credentials, secrets, tokens, private links, access-granting URLs, or unpublished material.
- [ ] Every fixture or example is synthetic and marked `synthetic: true` where the format supports it.
- [ ] The PR does not imply that a pilot, platform, participant group, compute allocation, registered organization, or endorsement exists.

## Licensing and provenance

- [ ] I am authorized to submit this material under the applicable file license described in `CONTRIBUTING.md`.
- [ ] I understand that submission does not guarantee review, acceptance, or merge, and that no DCO or CLA requirement is currently in force.

## Verification

- [ ] All JSON files parse.
- [ ] `python3 scripts/validate_v02.py` passes.
- [ ] If `examples/synthetic-action/` changed, its listed file checksums were recomputed and verified.

Commands run and relevant output:

```text

```
