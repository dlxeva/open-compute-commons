# Resource Hypothesis — What Could Be Contributed?

- **Status:** candidate framing note for discussion.
- **Evidence state:** untested. No resource has been donated, pooled, brokered, or used through OCC.
- **Phase-one scope:** personal AI usage windows under the participant's sole control.

"Donate AI compute" can describe several materially different arrangements. Treating them as one
resource would hide questions about custody, provider terms, data control, security, cost, and human
work. This note separates those arrangements before any implementation or pilot is proposed.

## The phase-one hypothesis

The narrow hypothesis is:

> People can use AI tools they already control to complete independently acceptable pieces of one
> authorized, public-data task, and the accepted results can be more useful to the requester than the
> coordination, review, and rework they require.

Under this hypothesis, a contributor keeps custody of their account and chooses whether to use it.
OCC would publish task instructions and acceptance criteria, receive submitted artifacts, and record
minimal process evidence. OCC would not receive, pool, transfer, meter, or call the contributor's
subscription. A personal usage window is therefore an **opportunity to perform work**, not a balance
transferred to the project.

This is the only resource model considered for a first phase. Even this model is not authorized to
run: there is no requester, eligible task, participant pool, or provider-terms review.

## Five resources that must not be conflated

| Resource | What it means | Custody and execution | Status in this draft |
|---|---|---|---|
| **Personal usage window** | A person has access to an AI product or local model and is willing to use some of that access on a task. It may be rate-limited, subscription-based, or simply available at that moment; OCC has no evidence that it would otherwise expire or go unused. | The person keeps the account, tool, and execution environment. They initiate every use and review what they submit. No credential or quota is transferred. | **The only phase-one hypothesis. Untested.** |
| **Allocated credits or API budget** | A provider, organization, or account owner deliberately allocates paid credits, a billing limit, or an API budget to approved work. | An accountable budget owner or operator would control credentials, billing, permitted purposes, regions, logs, and revocation. Personal self-custody rules do not solve these obligations. | **Separate future track. Blocked and undesigned.** No institution or provider has been approached. |
| **Compute node** | A contributor makes a machine, GPU, cluster partition, or hosted runtime available for jobs. | The node operator would need workload isolation, scheduling, software and model provenance, network policy, abuse controls, energy accounting, logging, and deletion. | **Separate future track. Blocked and undesigned.** No node has been offered. |
| **Volunteer labour** | A person finds a task, prepares inputs, writes prompts, checks outputs, corrects errors, reviews submissions, or resolves disputes. | The person contributes judgement and time. AI use may support the work, but the labour is not compute and should be recorded separately. | **Necessary to the proposed mechanism, but unmeasured.** No volunteer work has occurred. |
| **Redeemable token** | A transferable unit that can be exchanged for compute, money, access, governance, reputation, or another benefit. This is different from an API credential or a provider's internal usage counter. | Transferability creates financial, legal, governance, custody, fraud, and valuation questions that this draft does not address. | **Out of scope.** OCC v0.2 prohibits packaging subscription quota as a tradeable balance and prohibits token-to-impact conversion. |

The word **token** is especially ambiguous. An API access token is a credential and must never enter
OCC. A provider credit or API budget is a billing resource and belongs to a separate credit track. A redeemable or
tradeable token is an asset design and is out of scope. None of these is the phase-one personal usage
window described here.

## What is known

The following statements are supported by the current repository:

- The proposed first mode uses only public, authorized L0 data.
- Participants would execute through accounts or tools they control themselves.
- OCC must not collect passwords, API keys, OAuth tokens, session cookies, account email addresses,
  full conversation transcripts, or device fingerprints.
- Usage evidence would be self-reported and could not be presented as verified metering.
- No provider's terms have been checked for this use.
- No requester, beneficiary, task, participant, donated resource, or accepted result exists.

## What remains unknown

The draft has no evidence for the following questions:

- Do people have meaningful personal usage windows they are willing and permitted to use this way?
- Would provider terms allow a participant to use a personal plan for a third party's public-interest
  task, and would those terms differ by product, region, or account type?
- Can a real requester supply an L0 task that is public, authorized, divisible, and independently
  acceptable?
- Will a requester adopt the accepted output, rather than merely agree that it matches a schema?
- How much contributor time is spent on preparation, prompting, checking, correction, and submission?
- How much requester and coordinator time is spent on splitting, support, review, disputes, and rework?
- Is the resulting quality consistent enough to justify repeated execution or human review?
- Is any claimed AI usage genuinely incremental or otherwise unavailable to the requester?

No resource volume, cost saving, impact, participation rate, or quality rate should be estimated from
the synthetic fixtures.

## Conditions that would falsify or stop the phase-one hypothesis

A future, separately authorized test should stop or count against the hypothesis if any of the
following occurs:

1. No requester can provide an authorized L0 task with an accountable acceptance owner and useful output.
2. The applicable provider terms cannot be checked or do not permit the proposed use.
3. Participation requires transferring an account, credential, session, subscription quota, or
   private input to OCC or another contributor.
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
- pool, resell, transfer, or promise subscription quota;
- accept money, institutional credits, API budgets, or compute nodes;
- create a redeemable token, exchange rate, leaderboard, or token-to-impact formula;
- process non-public or sensitive data;
- recruit participants or launch a pilot without a separate decision and evidence gate.

Any proposal that crosses one of these boundaries is a different resource model and needs its own
threat model, terms review, accountable operator, and explicit authorization.
