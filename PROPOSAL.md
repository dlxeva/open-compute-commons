# Open Compute Commons — Open Proposal

- **Status**: candidate discussion draft. Not published as a decision, not adopted by any organization.
- **Derived from**: an internal draft dated 2026-08-08, extracted here for public discussion.
- **Nothing in this document is a commitment.** The project name, any organizational relationship,
  the first case, and long-term operation are all **undecided**.

> Read `README.md` first for the boundary table. Short version: no organization, no pilot,
> no participants, no requester, no runtime, no compute.

---

## 1. The idea in one sentence

Organize AI usage windows that people are willing to contribute — plus model quota and compute that
institutions might donate — into periodic **public actions**, where each action handles exactly one
concrete, splittable, checkable, publishable public-interest task.

## 2. Why propose it

Many people hold recurring quota on AI products. The quota rules and renewal windows differ per
person; no project can assume everyone's allowance expires on the same calendar boundary.

Meanwhile education, open research, public culture, accessibility, and public knowledge projects
contain a lot of work that AI assistance suits, and that often lacks budget, tooling, or hands.

The proposal is to test one organizing pattern: concentrate scattered usage windows and donatable
quota onto **one** public task at a time.

**This is a hypothesis to be tested, not a claim that it works.** It has not been tested.

## 3. How an action would work

```text
Organizer and requester co-design the split and write concrete acceptance criteria
  → collect a real public need, confirm the beneficiary and the data authorization
  → open one action, publish standard shards
  → participants claim work and execute it in an environment they themselves control
  → participants self-audit against the acceptance checklist
  → participants deliver, with whatever usage evidence they can provide
  → automatic checks + human spot-checking
  → publish results, progress, and a contribution ledger
```

The unit of coordination is **one public action**, not everyone's billing cycle. Participants join or
pause according to their own available time, quota, and equipment.

Note that every arrow above describes intended behaviour of a system that **does not exist**.

## 4. What would never be collected

These are hard limits, expressed as `MUST NOT` in `spec/PROTOCOL_v0.2.md` §9.3:

- No passwords or API keys for anyone's ChatGPT / Claude / Gemini / other accounts.
- No transfer of a participant's subscription quota to the project.
- No repackaging of ordinary subscription quota as tradeable token balances.
- No collection of participants' chat transcripts, full account details, or device logs.
- No identity documents as a precondition for participating.
- Participant identity is a project-internal pseudonym (`contributor_ref`).

Individual participants keep their own accounts and execution environments. **The project takes no
custody of any account** — `execution_policy.account_custody` is fixed to the single value
`participant_self_custody`, enforced at the schema level, and there is no mechanism, planned or
otherwise, for the project to call anyone's personal subscription.

If an institution or cloud provider ever contributed credits, an API budget, or compute nodes, that
would run through a separate authorization and ledger track — **no such institution has been
approached**.

## 5. Three execution modes

### 5.1 Public co-creation mode

The only mode contemplated for a first phase.

Participants see the input they claimed, see the model's output, run the basic checks, and submit.
Inputs must be public, authorized, and permitted for participants to view and process. Execution is
initiated in the browser, a local client, or the participant's own compute environment; **model
inference may happen on a third-party service**. Participants must confirm the terms of service,
data policy, and quota rules of whatever they use themselves. The project does not hold accounts and
does not call anyone's personal subscription.

Task types that would fit: organizing and translating public educational material; accessibility
descriptions for public-domain images; OCR correction and structuring of public-domain archives;
classification, indexing, and summarization of open research material.

These are illustrations of task *shape*. **No such task has been found, offered, or agreed to.**

### 5.2 Restricted hosted mode

A hypothetical future where contributors provide API credits, cloud quota, or nodes, and tasks run in
a controlled environment. This needs access control, logging, encryption, deletion mechanisms, and a
party legally responsible for data processing. **Not in a first phase. Currently blocked** — none of
those capabilities exist.

### 5.3 In-institution mode

Medical, minors', trade-secret, unpublished-research, and other sensitive tasks would stay inside the
data owner's environment. External participants would only sponsor compute or technical help and
would not touch the data. **Also blocked**, for the same reason.

## 6. Data boundary for a first phase

A first action would accept **L0 only**:

| Level | Nature of data | Open to public claiming |
|---|---|---|
| L0 | Public, authorized, participants permitted to view and process | Yes |
| L1 | Visible to restricted members, appropriately anonymized | Not yet |
| L2 | Unpublished research or institution-internal data | Prohibited |
| L3 | Personal privacy, medical, minors, trade secrets | Prohibited |

**Public execution offers no confidentiality.** Once data reaches a participant's device or their
model service, one must assume both can see the inputs and outputs.

This proposal does **not** assume any model provider has permitted this kind of collaboration, and
does **not** claim different subscription products share usage rules. Any real action would have to
check the applicable terms of service and data policies **before** launching.
Current status of that check: **not done for any provider** (`spec/PROTOCOL_v0.2.md` §12.2).

## 7. Protocol layer

Operational specifics live in `spec/PROTOCOL_v0.2.md`, with splitting in
`spec/TASK_SPLITTING_v0.1.md` and accounting in `spec/CONTRIBUTION_v0.1.md`. Core principles:

- How a task is split and how acceptance criteria are written is **co-designed by organizer and
  requester**, not dictated by one side.
- Execution includes a mandatory participant **self-audit** step against the concrete checklist.
- The ledger records the process of giving and delivering. **It does not prove social impact.**

## 8. Standard task package

Each shard should carry roughly these fields:

```yaml
task_id:            unique identifier
purpose:            public purpose
input:              input content or public address
instructions:       execution instructions
output_schema:      output structure
acceptance_criteria: acceptance criteria
recommended_models: suggested model or capability tier
estimated_workload: estimated rounds, time, or call volume
privacy_level:      L0 / L1 / L2 / L3
timeout:            execution deadline
retry_policy:       handling after failure
result_license:     license of the output
```

A worked example in file form is `examples/synthetic-action/`. It is **synthetic**: placeholder
strings, `synthetic://` input references, no real authorization, no output of value to anyone.

## 9. Minimum preconditions before any action could start

A requester would have to supply:

1. a real need and an identified beneficiary;
2. the data source and proof of authorization;
3. a small sample batch;
4. fixed execution instructions;
5. quantifiable acceptance criteria;
6. total and per-shard workload estimates;
7. how results are owned and published;
8. how failure, rework, and disputes are handled.

Until these exist, the project stays at "collecting candidate cases" and does **not** enter an action.
**It is at that stage now.** None of the eight items exists for any case.

## 10. How contribution would be recorded

A public ledger would record only what the action needs: task identifier, shard status, execution time
window, contribution type, estimated or actual usage range, submission / rework / acceptance status,
and a link to the final output.

It would **not** publish accounts, keys, full transcripts, or personal identity information without
consent. There is deliberately **no unified score, no ranking, and no token-to-impact conversion**
(`spec/CONTRIBUTION_v0.1.md`).

The ledger is process evidence. It does not by itself demonstrate social impact and does not speak for
beneficiaries. **No ledger exists and no contribution has ever been recorded.**

## 11. Roles

Initiator, requester, action coordinator, acceptor, contributor, protocol co-designer.

These are role *descriptions* for a single action, not appointments. **No one currently holds any of
them, and no formal organizational appointments exist or are planned in a first phase.**

## 12. What a first action would try to learn

Not scale. Whether a real, concrete public need can be found; whether ordinary participants will
complete one standard task; whether the task package is clear enough; whether results from different
models can be accepted against one standard; whether participants understand their own contribution;
whether output is worth publishing; how close actual usage is to the estimate; and what the rework,
rejection, and dispute rates are.

A first round might involve 10–30 participants, one task type, one batch of public data.
The actual size would depend on a real case and sample testing. **No such round is scheduled.**

## 13. Known unsolved problems

- Participants' devices, model services, and execution paths differ; splitting needs a minimum
  capability floor, and quality will vary.
- Whether participants follow acceptance criteria strictly depends on self-audit plus spot-checking;
  it cannot be verified 100%.
- Usage evidence may be entirely self-reported and is not verifiable.
- Automatic acceptance cannot cover domain judgment.
- Copyright, attribution, and maintenance of published results remain the requester's responsibility.
- Incentives cannot rest on leaderboards — and this proposal deliberately removes leaderboards.
- Institutional credits may carry region, purpose, branding, and data conditions.
- Long-term operation, funding, and the responsible legal entity are **undetermined**.
- Sybil resistance for pseudonymous participants is unsolved.

These need real cases, public discussion, and small trials to work through, one at a time.

## 14. What kind of collaborators this is looking for

At this stage the useful contribution is **criticism of the design**, not labour on a platform:

- people with a real public need in education, research, accessibility, or public culture, who can
  say whether this structure would help or get in the way;
- people who can judge whether the splitting model survives contact with real work;
- people who know data authorization, privacy, and security boundaries;
- people willing to say where this fails first.

See `CONTRIBUTING.md`. Note that this repository accepts **documentation, schema, and fixture
discussion only** — it cannot accept real data, accounts, or credentials, and it offers no platform
service in return.

## 15. Roadmap (aspirational, none of it scheduled)

| Stage | Content | Status |
|---|---|---|
| Proposal v0.1 | Open questions, mechanism, data boundary, unsolved problems | this document |
| Protocol v0.2 | Object model and data contract candidate | `spec/PROTOCOL_v0.2.md` |
| Pilot Brief | Pick a real case; produce sample, estimates, task package, acceptance criteria | **blocked** — no real case |
| Manual Pilot | One small action run with forms, shared files, simple scripts | **blocked** |
| Protocol v1.0 | Decide what deserves standardizing, *after* a real action leaves evidence | **blocked** |

## 16. Current status — explicit

- No organization registered, and no registration applied for.
- No formal platform built; no Control Plane, MCP adapter, Runner, or ledger service implemented.
- No first requester confirmed.
- No participants recruited.
- No real or sensitive data received.
- No long-term operation promised.
- No commitment made on behalf of any institution.
- No compute purchased, donated, or provided.

If you want to engage: propose a real public need, or point out where this mechanism is most likely
to break.
