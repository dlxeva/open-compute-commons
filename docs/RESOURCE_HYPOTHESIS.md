# Resource Hypothesis — What Could Be Contributed?

- **Status:** candidate framing note for discussion.
- **Evidence state:** untested. No resource has been donated, pooled, brokered, or used through OCC.
- **Phase-one scope:** volunteers' own judgement and time, spent on small, independently verifiable
  units. How a volunteer gets a unit done is their own choice. OCC receives and verifies results only.

"Contributing to OCC" can describe several materially different arrangements. Treating them as one
resource would hide questions about custody, provider terms, data control, security, cost, and human
work. This note separates those arrangements before any implementation or pilot is proposed.

## The phase-one hypothesis

The narrow hypothesis is:

> A public-interest task can be cut into small units that can each be verified independently, and
> volunteers, working with whatever tools they choose for themselves, can complete enough of those
> units at acceptable quality that the accepted results are more useful to the requester than the
> coordination, review, and rework they require.

Under this hypothesis:

- **OCC cuts tasks into units and verifies results.** It would publish task instructions and
  acceptance criteria, receive submitted results, verify them, and record minimal process evidence.
- **OCC does not care how a unit was produced.** A volunteer may use their own local model, an API or
  compute they have bought for themselves, other software, or no tool at all. All of these are
  acceptable; a unit is judged on its result, not on the tool.
- **OCC never pools, collects, or transfers anyone's quota, accounts, keys, or compute.** It does not
  receive, meter, operate, or call any volunteer's tools. A volunteer's tool use is an
  **opportunity to perform work**, not a balance transferred to the project.
- **Terms-of-service responsibility stays with the volunteer.** Whether a given tool's terms permit a
  given use is a matter between the volunteer and the provider of that tool. That responsibility is
  not part of OCC's protocol layer, and OCC makes no claim either way about any provider's terms.
- **Record, never restrict.** OCC only asks volunteers to record honestly what they used, so that a
  reviewer can judge whether two runs of the same unit were really independent. The record is not a
  restriction: no tool choice is required, ranked, or excluded because of it. What is recorded is
  defined in `spec/PROTOCOL_v0.2.md` §8.2 and `schemas/core/attempt.schema.json`.

This is the only resource model considered for a first phase. Even this model is not authorized to
run: there is no requester, eligible task, participant pool, or pilot decision.

## Resources that must not be conflated

| Resource | What it means | Custody and execution | Status in this draft |
|---|---|---|---|
| **Volunteer labour and judgement** | A person reads the instructions, completes a unit, checks and corrects output, reviews submissions, or resolves disputes. | The person contributes judgement and time. It is recorded separately from any tool use. | **The core phase-one resource. Untested.** No volunteer work has occurred. |
| **Volunteer-chosen tools** | Whatever the volunteer decides to use on their own unit: a local model, an API or compute they pay for themselves, other software, or nothing (manual work). | The volunteer keeps and controls the tool, any account, and the execution environment, and is responsible for that tool's terms. OCC sees only the submitted result and an honest record of what was used. Nothing is transferred. | **Allowed, and not a resource OCC receives.** Recorded, never restricted. Untested. |
| **Pooled personal subscription quota** | Organizing consumer AI subscription allowances so that their quota is collectively directed at third-party work, or treating unused allowance as something to contribute. | Would put many personal plans to work for a third party under OCC's coordination. | **Stopped. Out of scope.** Prior research reported that major providers' consumer terms prohibit this kind of use (`TODO: unverified`; see "Provider terms" below). OCC will not design, promote, or coordinate it. |
| **Allocated credits or API budget** | A requester, provider, organization, or account owner deliberately allocates paid credits, a billing limit, or an API budget to approved work. A requester-funded API budget would belong to this track. | An accountable budget owner or operator would control credentials, billing, permitted purposes, regions, logs, and revocation. Personal self-custody rules do not solve these obligations. | **Separate future track. Optional, blocked, and undesigned.** Who would hold keys and carry billing and data responsibility is undecided. No requester, institution, or provider has been approached. |
| **Compute node** | A contributor makes a machine, GPU, cluster partition, or hosted runtime available for jobs. | The node operator would need workload isolation, scheduling, software and model provenance, network policy, abuse controls, energy accounting, logging, and deletion. | **Separate future track. Blocked and undesigned.** No node has been offered. |
| **Redeemable token** | A transferable unit that can be exchanged for compute, money, access, governance, reputation, or another benefit. This is different from an API credential or a provider's internal usage counter. | Transferability creates financial, legal, governance, custody, fraud, and valuation questions that this draft does not address. | **Out of scope.** OCC v0.2 prohibits packaging subscription quota as a tradeable balance and prohibits token-to-impact conversion. |

A volunteer running their own tool on their own unit is not the same thing as pooled subscription
quota. In the first case OCC receives only a result; in the second, OCC would be organizing other
people's plans to do work for a third party. Only the first is part of the phase-one hypothesis.

The word **token** is especially ambiguous. An API access token is a credential and must never enter
OCC. A provider credit or API budget is a billing resource and belongs to a separate credit track. A redeemable or
tradeable token is an asset design and is out of scope. None of these is the volunteer labour or
volunteer-chosen tooling described here.

## Provider terms

- **Pooled personal subscription quota: stopped.** Prior research, relayed to this repository but not
  included in it, reported that the consumer terms of OpenAI, Anthropic, Google, DeepSeek, and xAI
  prohibit this kind of use, and that enforcement has been reported for Anthropic and Google.
  `TODO: unverified`: none of these conclusions has been checked against the providers' primary
  sources in this repository, and no term links are given because none have been verified here. The
  stop decision does not depend on that verification: under the tool-agnostic model above, OCC has no
  need for this path.
- **Volunteers' own tools: the volunteer's responsibility.** OCC does not review, certify, or assume
  permission under any provider's terms for a volunteer's own use of their own tools.

## What is known

The following statements are supported by the current repository:

- The proposed first mode uses only public, authorized L0 data.
- Volunteers would complete units with tools they choose and control themselves, or by hand; OCC would
  receive results only.
- OCC must not collect passwords, API keys, OAuth tokens, session cookies, account email addresses,
  full conversation transcripts, or device fingerprints.
- Usage evidence and tool records would be self-reported and could not be presented as verified
  metering.
- No provider's terms have been checked against primary sources in this repository.
- No requester, beneficiary, task, participant, donated resource, or accepted result exists.

## What remains unknown

The draft has no evidence for the following questions:

- Will people with the right skills spend their own time on small public-interest units without
  payment, points, or ranking?
- Can a real requester supply an L0 task that is public, authorized, divisible, and independently
  acceptable?
- Will a requester adopt the accepted output, rather than merely agree that it matches a schema?
- How much contributor time is spent on reading instructions, doing the unit, checking, correcting,
  and submitting?
- How much requester and coordinator time is spent on splitting, support, review, disputes, and rework?
- Is the resulting quality consistent enough to justify repeated execution or human review?
- Which tools do volunteers actually use, and is an honest self-reported record enough to judge
  whether two runs were independent?

No resource volume, cost saving, impact, participation rate, or quality rate should be estimated from
the synthetic fixtures.

## Conditions that would falsify or stop the phase-one hypothesis

A future, separately authorized test should stop or count against the hypothesis if any of the
following occurs:

1. No requester can provide an authorized L0 task with an accountable acceptance owner and useful output.
2. **Triggered for pooled subscriptions; that path is stopped.** Prior research reported that provider
   terms do not permit pooling personal subscription quota (`TODO: unverified`; see "Provider terms").
   The hypothesis also fails if completing units turns out to require OCC to pool, direct, or rely on
   anyone's quota, accounts, keys, or compute.
3. Participation requires transferring an account, credential, session, subscription quota, compute,
   or private input to OCC or another contributor.
4. Units cannot be judged independently with acceptable agreement between the contributor and the
   requester's reviewer.
5. The requester does not adopt the accepted result for its stated use.
6. Preparation, coordination, review, and rework consume at least as much scarce human effort as the
   accepted output saves for the requester.
7. Required quality can be reached only by hiding failure rates, treating self-reported usage as
   verified, or converting activity into an unsupported impact claim.
8. Preventing foreseeable abuse would require a hosted runtime, identity collection, or sensitive
   data handling that the phase-one model does not provide.

These are failure conditions, not success claims or target values. The repository currently has no
measurement against any of them.

## No-go boundaries

The phase-one hypothesis does not authorize OCC to:

- receive or operate a contributor's account or credential;
- pool, collect, resell, transfer, or promise anyone's subscription quota, accounts, keys, or compute;
- require, restrict, or rank volunteers by the tools they choose (tool use is recorded, never restricted);
- accept money, institutional credits, API budgets, or compute nodes;
- create a redeemable token, exchange rate, leaderboard, or token-to-impact formula;
- process non-public or sensitive data;
- recruit participants or launch a pilot without a separate decision and evidence gate.

Any proposal that crosses one of these boundaries is a different resource model and needs its own
threat model, terms review, accountable operator, and explicit authorization.
