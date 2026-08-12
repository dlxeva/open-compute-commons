# Open Compute Commons (OCC) — Candidate Discussion Draft

Open Compute Commons asks whether people can use AI tools they already control to help complete
small, verifiable pieces of a public-interest task. A requester would publish one authorized task
with explicit acceptance criteria. Contributors would claim pieces, use AI tools in environments
they control, review the output, and submit it for automated checks and requester-led acceptance.

The phase-one resource hypothesis is deliberately narrow: **participant-controlled personal usage
windows**. OCC would coordinate work, not pool subscriptions. It would never receive a contributor's
account, API key, login session, or quota. Allocated credits, API budgets, compute nodes, volunteer
labour, and redeemable tokens are different resources with different risks; they are separated in
[`docs/RESOURCE_HYPOTHESIS.md`](docs/RESOURCE_HYPOTHESIS.md).

> **Current reality:** this is a published candidate discussion draft, not a running project or an
> adopted standard. There is no organization, pilot, requester, participant pool, platform, or
> compute supply. All examples and fixtures are synthetic. The documents describe a mechanism that
> has not been tested.

## Who this is for

This draft is for people who can test its assumptions before anyone builds around them:

- public-interest project owners who understand what a useful, acceptable result would require;
- practitioners in volunteer computing, distributed systems, AI operations, safety, privacy, and
  open-source governance;
- people who use AI tools and can identify where participant-controlled execution would fail in practice.

At this stage, this is not a call to donate accounts, credentials, data, money, or compute. It is a
request for specific criticism of the proposed mechanism.

**[Challenge the draft](https://github.com/dlxeva/open-compute-commons/issues/new?template=design-critique.yml)**

## A hypothetical action

Imagine that a community archive has 60 public-domain photographs and wants accessible descriptions
for its website. The archive has confirmed that the images may be processed and published, and it
defines a checklist for length, factual grounding, and prohibited identity guesses.

An OCC action could split the collection into independently reviewable Units. A contributor might
claim five Units, use an AI tool through their own account, correct the drafts, and submit structured
results. File-level checks could reject malformed entries; the archive, or a reviewer it appoints,
would decide whether each description is acceptable. OCC would receive the submitted result and
minimal process evidence, but no login, API key, quota, private chat transcript, or device log.

**This action does not exist.** No archive has made this request, no images have been authorized, no
contributor has done the work, and no output has been accepted. The example only makes the proposed
flow concrete.

## What the repository contains

- a [public proposal](PROPOSAL.md);
- a [candidate object model and four state machines](spec/PROTOCOL_v0.2.md);
- a [task-splitting methodology](spec/TASK_SPLITTING_v0.1.md);
- a [contribution-accounting contract](spec/CONTRIBUTION_v0.1.md);
- [JSON Schemas for part of the object model](schemas/core/);
- [synthetic fixtures](conformance/) and a [standard-library checker](scripts/);
- a [resource hypothesis](docs/RESOURCE_HYPOTHESIS.md) and a [record of known v0.2 contradictions](docs/ERRATA_v0.2.md).

## What this is **not**

| Claim someone might make | Reality |
|---|---|
| "OCC is an organization / NGO" | **No.** No legal entity exists, none has been registered or applied for. |
| "There has been a pilot" | **No.** No pilot has run. No task has ever been claimed, executed, or accepted. |
| "There are operational participants" | **No.** Nobody has been recruited for an OCC action, no action has run, and no action-level contribution ledger exists. Repository authors and reviewers are documentation contributors only. |
| "There is a requester with real data" | **No.** No requester, no authorized dataset, no beneficiary. |
| "There is a Control Plane / API / Runner / MCP adapter" | **No.** None of these are implemented. The repository is files on disk. |
| "OCC provides compute" | **No.** No compute is provided, purchased, donated, or brokered. |
| "OCC can hold your account / subscription" | **Never.** Custody of third-party accounts, API keys, or subscription quota is a hard MUST NOT in the spec (`spec/PROTOCOL_v0.2.md` §9.3), not a feature to be added later. |
| "The examples are public-benefit output" | **No.** Every fixture and example is `synthetic: true` placeholder content with no use value to anyone. |
| "This is endorsed by some institution" | **No.** No institution has reviewed, approved, or endorsed any of this. |

The protocol labels the repository **C0 (document-conformant)**. This is a category defined by the
candidate draft, not an independent certification. C1–C3 are not claimed. Read
[`docs/ERRATA_v0.2.md`](docs/ERRATA_v0.2.md) before relying on any conformance language.

## Where to start reading

| Order | File | Why |
|---|---|---|
| 1 | [`docs/RESOURCE_HYPOTHESIS.md`](docs/RESOURCE_HYPOTHESIS.md) | What "contributing compute" could mean, and the one resource type considered in phase one. |
| 2 | [`PROPOSAL.md`](PROPOSAL.md) | The idea in plain terms, and its declared limits. |
| 3 | [`docs/ERRATA_v0.2.md`](docs/ERRATA_v0.2.md) | Confirmed contradictions in the current public draft. Read this before the protocol. |
| 4 | [`spec/PROTOCOL_v0.2.md`](spec/PROTOCOL_v0.2.md) | Candidate object model, state machines, validation layers, error codes, and security model. |
| 5 | [`spec/TASK_SPLITTING_v0.1.md`](spec/TASK_SPLITTING_v0.1.md) | Why Unit / Shard / Attempt are three separate atoms. |
| 6 | [`spec/CONTRIBUTION_v0.1.md`](spec/CONTRIBUTION_v0.1.md) | Why there is deliberately no unified score. |
| 7 | [`examples/synthetic-action/`](examples/synthetic-action/) | A file-only, synthetic illustration of a task package. |
| 8 | [`docs/CONFORMANCE_REPORT.md`](docs/CONFORMANCE_REPORT.md) | What the local checker does and, more importantly, what it does not do. |

Supporting documents: [contribution guide](CONTRIBUTING.md), [security policy](SECURITY.md),
[license decision record](LICENSE_OPTIONS.md), and [publication checklist](PUBLISH_CHECKLIST.md).

## Licensing — dual license, by file type

This repository is published under **two** licenses, split by file type. The
boundary is fixed and stated here so there is no ambiguity:

| License | Applies to |
|---|---|
| **CC BY 4.0** (documentation) | `README.md`, `PROPOSAL.md`, `spec/**/*.md`, `docs/**/*.md`, `CONTRIBUTING.md`, `SECURITY.md`, `PUBLISH_CHECKLIST.md`, `LICENSE_OPTIONS.md`, `LICENSE-DOCS.md`, `examples/synthetic-action/**/*.md`, `schemas/core/**/*.md` |
| **Apache-2.0** (code / schema / fixture) | `schemas/core/*.json`, `conformance/**/*.json`, `examples/synthetic-action/*.json`, `scripts/*.py` |

- Full text of Apache-2.0: `LICENSE`.
- Full text of CC BY 4.0: `LICENSE-DOCS.md`.
- The boundary is drawn by file extension, with no exception for Markdown: the Markdown files inside
  `examples/synthetic-action/` are documentation (CC BY 4.0) even where they also describe a data
  contract, and the JSON files there are fixtures (Apache-2.0). A file's own
  `SPDX-License-Identifier` header, if present, governs for that file.

Attribution under CC BY 4.0 should credit the repository (`dlxeva/open-compute-commons`) and must not
imply endorsement by, or affiliation with, any institution. No institution has reviewed or endorsed
this material, and no legal entity exists behind it. All examples and fixtures are `synthetic: true`
placeholder content.

## Language policy

**English is the authoritative public version of this repository.** The English documents at their
canonical paths are the versions to review, cite, and raise objections against. Chinese mirrors are
provided for readers who prefer Chinese; where a mirror and the English version diverge, the English
version governs.

The Chinese mirrors are copies of the pre-translation Chinese source text. They are not maintained
in lockstep and **MAY** lag behind the English version.

| English (authoritative) | 中文镜像 (Chinese mirror) |
|---|---|
| [`spec/PROTOCOL_v0.2.md`](spec/PROTOCOL_v0.2.md) | [`spec/i18n/zh-CN/PROTOCOL_v0.2.md`](spec/i18n/zh-CN/PROTOCOL_v0.2.md) |
| [`spec/TASK_SPLITTING_v0.1.md`](spec/TASK_SPLITTING_v0.1.md) | [`spec/i18n/zh-CN/TASK_SPLITTING_v0.1.md`](spec/i18n/zh-CN/TASK_SPLITTING_v0.1.md) |
| [`spec/CONTRIBUTION_v0.1.md`](spec/CONTRIBUTION_v0.1.md) | [`spec/i18n/zh-CN/CONTRIBUTION_v0.1.md`](spec/i18n/zh-CN/CONTRIBUTION_v0.1.md) |
| [`docs/CONFORMANCE_REPORT.md`](docs/CONFORMANCE_REPORT.md) | [`docs/i18n/zh-CN/CONFORMANCE_REPORT.md`](docs/i18n/zh-CN/CONFORMANCE_REPORT.md) |
| [`examples/synthetic-action/README.md`](examples/synthetic-action/README.md) | [`examples/synthetic-action/i18n/zh-CN/README.md`](examples/synthetic-action/i18n/zh-CN/README.md) |
| [`examples/synthetic-action/instructions.md`](examples/synthetic-action/instructions.md) | [`examples/synthetic-action/i18n/zh-CN/instructions.md`](examples/synthetic-action/i18n/zh-CN/instructions.md) |
| [`schemas/core/README.md`](schemas/core/README.md) | [`schemas/core/i18n/zh-CN/README.md`](schemas/core/i18n/zh-CN/README.md) |

Documents not listed above (`PROPOSAL.md`, `docs/RESOURCE_HYPOTHESIS.md`, `docs/ERRATA_v0.2.md`,
`CONTRIBUTING.md`, `SECURITY.md`, `LICENSE_OPTIONS.md`, and `PUBLISH_CHECKLIST.md`) have no Chinese
mirror. The "中文摘要" section at the end of this README is a summary, not a mirror of the full English
text above it. Translating the remaining documents is an open item; see `CONTRIBUTING.md`.

Licensing is unchanged by language: a Chinese mirror carries the same license as the English file it
mirrors (`i18n/zh-CN/*.md` are documentation, CC BY 4.0).

## Verify it locally

No network access, no dependencies, no install step. Python 3 standard library only.

```bash
# 1. Every JSON file parses
python3 -c "import json,pathlib,sys; [json.loads(p.read_text(encoding='utf-8')) for p in pathlib.Path('.').rglob('*.json')]; print('json ok')"

# 2. Fixtures match their expected.json (schema / state / invariant counts)
python3 scripts/validate_v02.py
echo "exit=$?"          # 0 = every fixture set matched expectations

# 3. List or run a single fixture set
python3 scripts/validate_v02.py --list
python3 scripts/validate_v02.py conformance/valid

# 4. Recompute the example package's file checksums
python3 -c "import hashlib,json,pathlib; d=pathlib.Path('examples/synthetic-action'); m=json.loads((d/'checksums.json').read_text(encoding='utf-8')); [print(('OK  ' if hashlib.sha256((d/f['path']).read_bytes()).hexdigest()==f['sha256'] else 'FAIL'), f['path']) for f in m['files']]"
```

What a passing run means: **the files on disk are internally consistent.** It does not mean a system
works, because there is no system. `conformance/invalid_redline/` is a deliberately non-compliant
fixture — for that set, "PASS" means "the checker correctly reported the expected violations".

Two kinds of hashes appear in `examples/synthetic-action/`, and they are not equally real:

- `checksums.json` → `files[].sha256` — **real** SHA-256 over file bytes, recomputable with step 4 above.
- `content_hash` / `input_hash` inside the JSON objects — **placeholder**, sixty-four zeros. The
  canonical-serialization algorithm in `spec/PROTOCOL_v0.2.md` §4.2 is specified but not implemented here.

## Open questions worth arguing about

1. Is Unit-level acceptance actually workable for a real public-interest task, or does it fragment the work past usefulness?
2. Self-reported usage cannot be verified. Is recording it at all a mistake?
3. Contribution accounting deliberately refuses a single score. Does anything remain that sustains participation?
4. Public-track execution offers no confidentiality. Which task types survive that constraint?
5. Do the terms of service of the model providers people would use actually permit this kind of collaboration? **This has not been checked with any provider** — see `spec/PROTOCOL_v0.2.md` §12.2.
6. Where is this design most likely to fail first?

---

## 中文摘要

> **语言政策**：本仓库以**英文为权威公开版本**。中文镜像见各文档的 `i18n/zh-CN/` 路径
> （对照表见上文 "Language policy"）。中文镜像是翻译前中文原文的副本，可能滞后于英文版；
> 两者不一致时**以英文版为准**。本节是摘要，不是上文英文正文的完整镜像。

**这是一份候选讨论稿，不是已运行的项目。**

Open Compute Commons（OCC）想验证：个人是否能在不交出账号、密钥或订阅额度的前提下，
用自己控制的 AI 工具完成公益任务中可独立验收的小单元。第一阶段只讨论这种
**个人自主控制的 AI 使用窗口**；credits / API 预算、算力节点、志愿劳动与可兑换 token 是不同资源，
不能混为一谈。本仓库只包含这个设想的**文档、JSON Schema 和合成样例**，用于在动手之前接受批评。

必须说清楚的边界：

- **不是组织**：没有注册任何实体，也没有提出过任何注册申请。
- **没有 Pilot**：没有真实需求方、没有授权数据、没有受益方、没有参与者、没有贡献账本。
- **没有运行时**：Control Plane、MCP adapter、Runner、账本服务**全部未实现**，仓库里只有文件。
- **不提供算力**：不采购、不募集、不中转任何算力。
- **不代管账号**：不收集、不存储、不代理任何第三方账号、API Key、OAuth token 或订阅额度。
  这是协议里的硬性 **MUST NOT**（`spec/PROTOCOL_v0.2.md` §9.3），不是"以后再做"的功能。
- **样例全是合成的**：`examples/` 与 `conformance/` 下所有内容标注 `synthetic: true`，
  是占位数据，对任何人都没有使用价值，**不构成公益成果**。
- **未获任何机构背书**。

协议把本仓库标为 **C0（文档一致）**；这是候选协议自行定义的类别，不是独立认证。
当前已确认的内部矛盾见 `docs/ERRATA_v0.2.md`，C1–C3 未被主张。

阅读顺序：`docs/RESOURCE_HYPOTHESIS.md` → `PROPOSAL.md` → `docs/ERRATA_v0.2.md`
→ `spec/PROTOCOL_v0.2.md` → `spec/TASK_SPLITTING_v0.1.md` → `spec/CONTRIBUTION_v0.1.md`
→ `examples/synthetic-action/` → `docs/CONFORMANCE_REPORT.md`。

本地验证命令见上文 "Verify it locally"。校验通过只说明**磁盘上的文件自洽**，
不说明任何系统正确运行——因为没有系统。

关于许可证：本仓库采用**双许可证**，按文件类型划分。文档（README、PROPOSAL、spec/\*.md、
docs/\*.md、CONTRIBUTING、SECURITY、PUBLISH_CHECKLIST、LICENSE_OPTIONS、examples/synthetic-action/\*.md）
适用 **CC BY 4.0**，全文见 `LICENSE-DOCS.md`；代码/Schema/fixture
（schemas/core/\*.json、conformance/\*\*/\*.json、examples/synthetic-action/\*.json、scripts/\*.py）
适用 **Apache-2.0**，全文见 `LICENSE`。

仓库 owner/slug 已确认为 `dlxeva/open-compute-commons`，公开（public），Issues 已启用，Discussions
已禁用，无公开邮箱。安全报告暂采用 public GitHub Issues only，保留以后启用 private reporting 的可能。
见 `PUBLISH_CHECKLIST.md` 与 `LICENSE_OPTIONS.md`。
