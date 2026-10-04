# Demand-Side Commitment Gate

> English is the authoritative public version of this document.
> Chinese mirror: [`docs/i18n/zh-CN/DEMAND_COMMITMENT.md`](i18n/zh-CN/DEMAND_COMMITMENT.md).

- **Status:** candidate selection rule for discussion. Not applied to any real case.
- **Evidence state:** no requester exists, so no commitment has been requested, given, or kept.
- **Relates to:** `PROPOSAL.md` §9 item 7; `docs/RESOURCE_HYPOTHESIS.md` falsification conditions 1,
  5, and 6; `spec/CONTRIBUTION_v0.1.md` §3.3 (impact evidence);
  `schemas/core/action.schema.json` (`adoption_commitment`).

## Why a gate before a pilot

A public-interest task is only worth cutting into units if the requester will actually use the
accepted results. "The requester does not adopt the accepted result" is already a falsification
condition (`docs/RESOURCE_HYPOTHESIS.md`, condition 5), but a falsification condition only detects
the failure after volunteers have done the work. This gate moves the question **before** any work:
a candidate need is selected for a pilot only if the requester commits, in advance, to how the
results will be used.

## The five commitment items

A requester would have to state all five items before a candidate need could be selected. Each item
is described **only at a publicly shareable level**: roles rather than personal names, and public
systems or pages rather than private links or internal locations.

| # | Item | What the requester states | Example of the expected level of detail (fictional) |
|---|---|---|---|
| 1 | **Where results land** | The specific system, page, catalogue, or dataset where accepted results will be published or used. | "The public online catalogue of the archive's photograph collection." |
| 2 | **Expected publication time** | When accepted results will be published or put into use, relative to acceptance. | "Within 4 weeks after the batch is accepted." |
| 3 | **Acceptance and adoption sign-off** | Which role accepts units, and which role is authorized to sign off that the results are adopted. | "Acceptance: collections reviewer. Adoption sign-off: head of digital collections." |
| 4 | **Output format sign-off** | The requester confirms the output schema the units will be checked against. | "Output schema reviewed and confirmed by the collections reviewer." |
| 5 | **Manual baseline** | How many minutes one unit takes the requester's own staff or volunteers by hand, as a range with a basis level (`measured`, `calibrated`, or `assumed`, as in `spec/TASK_SPLITTING_v0.1.md` §3.2). | "p50 8 minutes, p90 15 minutes, basis `assumed`." |

The manual baseline is what lets a pilot check verification-cost inversion
(`docs/RESOURCE_HYPOTHESIS.md`, condition 6): if review, arbitration, and rework cost about as much
requester time as doing the units by hand, the mechanism has not helped.

## The rule

**If any of the five items is missing, the candidate need is not selected.**

- "Unknown", "to be decided", or "we will see" counts as missing.
- A baseline with basis `unknown` counts as missing.
- A commitment cannot be filled in by OCC, a coordinator, or a volunteer on the requester's behalf.
- A need that is not selected may still be discussed in an Issue; it just does not enter an Action.

## What a commitment is and is not

- It is a **selection gate and a record**, not a contract. OCC has no means to enforce it and does not
  claim to.
- It is recorded before the Action opens, and it is not edited afterwards. A changed commitment is
  recorded as a new entry with the reason.
- After a pilot, the commitment is checked against what happened. If results were not published at
  the committed place within the committed time, the pilot is recorded as failing condition 5, and
  that failure is published like any other result.
- Adoption is **impact evidence** and can only be declared by the requester
  (`spec/CONTRIBUTION_v0.1.md` §3.3). The commitment states an intention; it is not itself evidence of
  adoption.

## Recording

- **Issue form:** `.github/ISSUE_TEMPLATE/candidate-public-need.yml` asks for items 1–3 at a publicly
  shareable level, so that a candidate need can be screened early. Answering "unknown" there is
  allowed for discussion, but such a need cannot be selected.
- **Action object:** `schemas/core/action.schema.json` has an optional `adoption_commitment` object.
  When present, all five items are required inside it. The schema cannot express "required before
  `open`" (the local validator does not support conditional keywords); the rule above states that
  requirement in prose.

## Current status

No requester has been approached, no commitment exists, and no candidate need has been selected. All
examples above are fictional and describe the expected level of detail only.
