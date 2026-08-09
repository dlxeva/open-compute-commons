# Open Compute Commons：贡献记录规范 v0.1（候选草案 / candidate draft）

- **状态**：candidate draft，未发布、未实现、无任何真实贡献记录存在。
- **日期**：2026-08-09。
- **依赖**：`spec/PROTOCOL_v0.2.md`（§2.11、§11）、`spec/TASK_SPLITTING_v0.1.md`。
- **性质**：记账语义契约候选。当前**没有任何真实参与者、真实贡献或真实账本**。

---

## 1. 设计立场

三条不做的事，先说清楚：

1. **不设统一积分。** 没有总分、没有等级、没有排行榜作为主要呈现。不同轨道的贡献在性质上不可通约，强行折算成一个数字会制造虚假的可比性。
2. **不做 token-to-impact 换算。** 不存在任何把贡献折算为影响力、金额、代币或可兑换权益的公式。账本记录的是**过程证据**，不是影响力凭证。
3. **不把活动量当质量或影响。** 提交了 100 个 Unit 不等于做得好，做得好不等于产生了社会影响。这三件事分开记、分开看。

理由：一旦有统一分数，参与者的行为就会向分数优化，而分数必然是所有真实目标的劣质代理。公益语境下这个失真尤其危险 —— 它会把"帮到了谁"替换成"刷到了多少"。

---

## 2. 五条贡献轨道（Contribution Tracks）

轨道之间**平行**，**MUST NOT** 有优劣排序或换算关系。

### 2.1 Track R — 需求与领域（Requirement & Domain）

提供真实公共需求、数据授权、领域验收标准。

- 典型活动：提出需求、提供授权证明、定义领域验收规则、做 L4 领域判定、确认成果可用。
- 确认事件：需求被接受进入 Action、TaskDefinition 冻结、L4 判定完成。
- **这条轨道当前完全为空**：无真实需求方（blocked）。

### 2.2 Track E — 执行（Execution）

认领 Shard、执行、交付。

- 典型活动：Claim、Attempt、Submission。
- 确认事件：Submission 达 `accepted` 或 `partially_accepted`。
- 计量单位：accepted unit 数、completed attempt 数（分开记）。

### 2.3 Track Q — 质量（Quality）

复核、抽检、交叉核对、争议仲裁。

- 典型活动：L3 交叉核对、L4 抽检、参与争议仲裁、报告缺陷。
- 确认事件：Validation 记录产生并被采纳；争议结论作出。
- 约束：**MUST NOT** 对自己的 Submission 做 Q 轨道记账（自证禁止）。

### 2.4 Track P — 协议工程（Protocol Engineering）

改进协议、schema、工具、文档、切分方法。

- 典型活动：提出协议修订、编写/修正 schema、编写校验工具、编写任务包模板。
- 确认事件：修订被合入某个 version 并冻结。
- 说明：本轮仓库内的所有工作若要记账，属于此轨道，且当前**未记账**（无账本）。

### 2.5 Track S — 资源（Resource / Sponsorship）

提供 Credits、API 预算、计算节点、受控执行环境。

- 典型活动：机构捐出额度、提供受控环境、承担基础设施。
- 确认事件：资源到位并可用，或受控执行完成。
- 约束：**MUST NOT** 记录个人订阅额度为"捐出的资源"—— 个人订阅由参与者自持自用（`account_custody: participant_self_custody`），不构成向项目的资源转移。
- **这条轨道当前完全为空**：无机构接洽（blocked）。

### 2.6 轨道对照表

| 轨道 | 记什么 | 确认前提 | 当前状态 |
|---|---|---|---|
| R 需求/领域 | 需求、授权、领域判定 | 需求进入 Action / L4 完成 | blocked（无真实需求方） |
| E 执行 | accepted unit、attempt | Submission accepted/partially | 无（无真实执行） |
| Q 质量 | Validation、仲裁 | Validation 采纳 | 无 |
| P 协议工程 | 协议/schema/工具修订 | 修订合入并冻结 | 无（未建账本） |
| S 资源 | Credits、节点、环境 | 资源到位可用 | blocked（无机构） |

---

## 3. 三类证据必须分开

这是本规范的核心结构约束。三类证据 **MUST** 分开存储、分开呈现，**MUST NOT** 合并为单一数字。

### 3.1 活动证据（Activity Evidence）

**做了什么，做了多少。**

- 例：完成 12 个 Attempt；提交 4 个 Submission；参与 3 次抽检；提交 2 项协议修订。
- 性质：**客观、可数、不含判断**。
- 记录前提：对应对象存在且状态已确认。
- **MUST NOT** 被表述为"贡献大小"或"质量"。
- 未被采纳的重复执行结果（`not_selected`）**MUST** 计入活动证据 —— 劳动真实发生过。

### 3.2 质量证据（Quality Evidence）

**做得怎么样。**

- 例：L1/L2 一次通过率；L4 抽检通过率；返工轮次分布；争议中被推翻的判定数。
- 性质：**相对、有条件、依赖样本量**。
- 约束：
  - **MUST** 附样本量。样本量过小时 **MUST** 标注 `insufficient_sample`，**MUST NOT** 呈现比率。
  - **MUST NOT** 用于排序参与者。
  - **MUST NOT** 从活动证据推导（做得多 ≠ 做得好）。
  - 单次失败 **MUST NOT** 产生持久负面标签；质量证据是分布，不是评级。

### 3.3 影响证据（Impact Evidence）

**产生了什么实际作用。**

- 例：成果被需求方采用；被下游项目引用；受益方反馈。
- 性质：**只能由外部主体确认，不能由项目自证**。
- 约束：
  - 影响证据 **MUST** 由需求方或受益方声明，**MUST NOT** 由项目方或参与者自行填写。
  - **MUST NOT** 从活动或质量证据推导。交付了 100 个 Unit 不构成任何影响声明。
  - 无外部确认时 **MUST** 留空并标 `unclaimed`，**MUST NOT** 用产出量代替。
- **当前状态：全部为空。** 没有任何真实成果、任何真实采用、任何受益方（blocked）。

### 3.4 为什么必须分开

合并三者会产生具体的失真：
- 活动 + 质量合并 → 高产出低质量的参与者看起来优于低产出高质量的；
- 质量 + 影响合并 → 项目自己给自己颁发影响力证书；
- 三者合成一个分数 → 参与者优化分数而非优化公共价值。

分开的代价是账本不好看、无法一眼排名。这是有意的。

---

## 4. ContributionRecord 最小字段

### 4.1 字段表

| 字段 | 强度 | 类型 | 说明 |
|---|---|---|---|
| `record_id` | MUST | string | 唯一标识 |
| `action_id` | MUST | string | 所属 Action |
| `contributor_ref` | MUST | string | **假名标识**，MUST NOT 为邮箱/账号/真名 |
| `track` | MUST | enum | `R`\|`E`\|`Q`\|`P`\|`S` |
| `evidence_class` | MUST | enum | `activity`\|`quality`\|`impact` |
| `subject_type` | MUST | enum | 关联对象类型（submission / validation / unit 等） |
| `subject_id` | MUST | string | 关联对象 ID |
| `confirming_event_id` | MUST | string | **触发记账的确认事件**（§5） |
| `recorded_at` | MUST | date-time | 记账时间 |
| `status` | MUST | enum | `active`\|`revoked`\|`superseded` |
| `activity_measures` | SHOULD | object | 活动计量（仅 evidence_class=activity） |
| `quality_measures` | SHOULD | object | 质量计量 + 必须的 `sample_size` |
| `impact_claim` | MAY | object | 影响声明 + 必须的 `claimed_by`（外部主体） |
| `self_reported_usage` | MAY | object | 自报用量，MUST 带 `self_reported: true` |
| `notes` | MAY | string | 备注 |
| `revocation_reason_code` | 条件 MUST | string | status=revoked 时必填 |

### 4.2 禁止字段（MUST NOT 出现）

- `score` / `points` / `total` / `rank` / `level` / `tier`（任何统一积分或等级）
- `impact_value` / `token_equivalent` / `credit_value`（任何换算）
- 任何第三方账号标识、邮箱、API Key、设备指纹
- 任何完整对话记录或未经同意的 PII

这些禁止项由 `schemas/core/contribution_record.schema.json` 的 `additionalProperties: false` 与 conformance fixture 检查。

### 4.3 示例（synthetic）

```json
{
  "record_id": "cr-synthetic-0001",
  "action_id": "act-synthetic-alttext-001",
  "contributor_ref": "pseudo-alpha",
  "track": "E",
  "evidence_class": "activity",
  "subject_type": "submission",
  "subject_id": "sub-synthetic-a-1",
  "confirming_event_id": "evt-synthetic-0007",
  "recorded_at": "2026-08-09T10:00:00+08:00",
  "status": "active",
  "activity_measures": {
    "accepted_units": 1,
    "rejected_units": 1,
    "completed_attempts": 1
  },
  "self_reported_usage": {
    "self_reported": true,
    "model_calls_range": "1-3"
  },
  "notes": "SYNTHETIC 演示记录；非真实贡献"
}
```

注意：`accepted_units: 1` 与 `rejected_units: 1` 并存 —— 这是部分通过的正常记账形态，不是异常。

---

## 5. 只有状态确认后才能记账

### 5.1 规则

- ContributionRecord **MUST** 引用一个 `confirming_event_id`。
- 该 Event **MUST** 已存在于 Event 日志中，且 **MUST** 是下表允许的确认事件之一。
- **MUST NOT** 在 Submission 处于 `received` / `validating` 时记账。
- **MUST NOT** 在 Claim 建立时记账（认领不是贡献）。
- **MUST NOT** 预记、暂记或"待确认记账"。

### 5.2 各轨道的确认事件

| 轨道 | 允许的确认事件 |
|---|---|
| R | `requirement.accepted`、`task_definition.frozen`、`validation.recorded`(L4) |
| E | `submission.accepted`、`submission.partially_accepted` |
| Q | `validation.recorded`(L3/L4)、`dispute.resolved` |
| P | `protocol.version_frozen`、`schema.version_frozen` |
| S | `resource.available`、`controlled_execution.completed` |

### 5.3 部分通过时的记账

- 只记**已通过**的 Unit 为 `accepted_units`。
- 未通过的 Unit 记为 `rejected_units`（属于活动证据，不是惩罚）。
- 返工成功后 **MUST** 产生**新的** ContributionRecord，**MUST NOT** 修改原记录把 rejected 改成 accepted。

### 5.4 幂等与记账

- 同一 `idempotency_key` 的重复提交 **MUST NOT** 产生第二条 ContributionRecord。
- 同一 `(subject_id, contributor_ref, evidence_class)` **MUST** 至多一条 `active` 记录。

### 5.5 撤销

- 事后发现问题（作弊、误判、争议推翻）时 **MUST** 将原记录置 `revoked` 并填 `revocation_reason_code`，同时写入新 Event。
- **MUST NOT** 删除记录。
- **MUST NOT** 静默修改历史计量。

---

## 6. 呈现约束

若将来存在公开账本界面：

- **MUST** 按轨道与证据类别分区呈现；
- **MUST NOT** 提供跨轨道总分或全局排行榜作为主视图；
- **MUST** 在质量证据旁显示样本量；
- **MUST** 在影响证据旁显示声明方；无声明方时显示 `unclaimed`；
- **MUST** 显示自报用量的 `self_reported` 标记；
- **MAY** 提供参与者查看自己历史的私有视图；
- **MUST NOT** 默认公开单个参与者的质量比率。

---

## 7. Deferred / Unknown / Blocked

**Deferred**：账本界面、参与者私有视图、贡献导出格式、跨 Action 的贡献聚合、荣誉/致谢的具体形态。

**Unknown**：非积分的激励是否足以维持参与（无参与者，无数据）；质量证据的合理最小样本量；影响证据的采集方式是否可行；假名标识的抗女巫能力。

**Blocked**：R 轨道（无真实需求方）；S 轨道（无机构接洽）；影响证据（无真实成果与受益方）；任何真实记账（无账本、无参与者）。

---

## 8. 诚实声明

- 本规范为 candidate draft，**未实现**。
- **当前不存在任何真实 ContributionRecord、真实参与者、真实账本。**
- 文中示例标注 SYNTHETIC，**不是真实贡献，不是 Pilot 成果**。
- 本规范不构成对任何参与者的权益承诺 —— 它明确规定了**不存在**可兑换权益。
