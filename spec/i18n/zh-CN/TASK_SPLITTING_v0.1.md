# Open Compute Commons：任务切分规范 v0.1（候选草案 / candidate draft）

- **状态**：candidate draft，未发布、未实现。
- **日期**：2026-08-09。
- **依赖**：`spec/PROTOCOL_v0.2.md`（对象模型与状态机）。
- **性质**：切分方法学与数据契约候选。本文件所有数值、样例任务与工作量估算均为 **synthetic**，**不是真实 Pilot 成果**。

---

## 1. 三种原子（本规范的核心区分）

v0.1 协议只有一个模糊的"分片"概念，导致验收、认领、计量三件事被绑死。v0.2 把它们拆成三个独立的原子：

| 原子 | 回答的问题 | 谁在意 | 数量关系 |
|---|---|---|---|
| **Unit** | 这一小块**做对了吗**？ | 验收者、需求方 | 1 Unit = 1 次独立 pass/fail 判定 |
| **Shard** | 这一批**归谁做**？ | 参与者、协调者 | 1 Shard = 1..N 个 Unit |
| **Attempt** | 这次执行**花了多少**？ | 计量、账本 | 1 Claim = 1..N 个 Attempt |

### 1.1 Unit 是验收原子

- Unit 是能被**独立**判定通过或不通过的最小工作。
- 判定 Unit A 时 **MUST NOT** 依赖 Unit B 的结果。
- 一个 Unit **MUST** 最终对应至多一个 active CanonicalResult。
- 部分通过、返工、共识，全部在 **Unit 粒度**上发生。

**为什么重要**：如果验收只能在整批上做，那么 100 个里错 1 个就得整批返工，参与者的 99 份劳动被浪费。Unit 粒度让部分通过成为一等公民。

### 1.2 Shard 是认领原子

- Shard 是参与者在界面上"领"的那个东西。
- Shard 的大小由**人的一次坐下能做完多少**决定，不由验收逻辑决定。
- Shard **MUST NOT** 影响验收粒度：把 20 个 Unit 打成一个 Shard，仍然是 20 次独立判定。

**为什么重要**：认领粒度是人体工学问题（太小则交互成本高，太大则无人敢领、超时率高），验收粒度是质量问题。两者最优值几乎从不相同。

### 1.3 Attempt 是执行计量原子

- 一次 Claim 下可以有多次 Attempt：第一次模型输出不合格、换模型重试、中途中断后重来。
- 用量、时长、模型信息记在 Attempt 上，**不记在 Shard 上**。
- Attempt 记录 **MUST** 标注 `self_reported`。

**为什么重要**：如果把用量记在 Shard 上，重试就会污染工作量基线；把它记在 Attempt 上，才能得到"完成一个 Shard 平均需要几次尝试"这个真正有用的校准数据。

### 1.4 三者关系图

```text
TaskDefinition (frozen)
   │
   ├── Unit u1 ─┐
   ├── Unit u2 ─┼── Shard s1 ── Claim c1 ── Attempt a1 (失败)
   ├── Unit u3 ─┘              └─ Attempt a2 (成功) ── Submission sub1
   │                                                      ├── u1: pass  → CanonicalResult
   │                                                      ├── u2: pass  → CanonicalResult
   │                                                      └── u3: fail  → rework
   ├── Unit u4 ─┐
   └── Unit u5 ─┴── Shard s2 ── Claim c2 ── ...

   Unit u3 → Shard s3 (rework, parent_shard_id = s1)   ← 只含失败的 u3
```

---

## 2. 切分约束（Splitting Constraints）

### 2.1 Unit 层约束

| # | 约束 | 强度 |
|---|---|---|
| U1 | Unit **MUST** 可独立验收，不依赖同批其他 Unit 结果 | MUST |
| U2 | Unit **MUST** 有稳定标识 `unit_id` 与输入 `content_hash` | MUST |
| U3 | Unit **MUST NOT** 跨越不同 `sensitivity_level` | MUST |
| U4 | Unit 的验收标准 **MUST** 在 TaskDefinition 冻结时已确定 | MUST |
| U5 | Unit **SHOULD** 小到单次判定在人可承受的注意力内完成 | SHOULD |
| U6 | Unit **SHOULD NOT** 需要参与者自行获取额外外部资料 | SHOULD |
| U7 | Unit **MAY** 携带难度标记，供后续校准使用 | MAY |

### 2.2 Shard 层约束

| # | 约束 | 强度 |
|---|---|---|
| S1 | Shard **MUST** 非空（至少一个 Unit） | MUST |
| S2 | Shard 内 Unit **MUST** 属于同一 TaskDefinition 同一 version | MUST |
| S3 | Shard 内 Unit **MUST** 共享同一 `data_policy` 敏感级别 | MUST |
| S4 | Shard **MUST** 声明 `lease_duration_seconds` | MUST |
| S5 | 返工 Shard **MUST** 只含未通过 Unit，并设 `parent_shard_id` | MUST |
| S6 | Shard 大小 **SHOULD** 使 `workload_envelope` 上界落在单次可完成范围内 | SHOULD |
| S7 | 同一 Unit 出现在多个并行 Shard 中 **MUST** 仅因 replication 或 rework | MUST |
| S8 | Shard **SHOULD NOT** 混合难度差异极大的 Unit（破坏工作量估算） | SHOULD |
| S9 | Shard **MAY** 声明 `max_concurrent_claims` 与 `replication_factor` | MAY |

### 2.3 Attempt 层约束

| # | 约束 | 强度 |
|---|---|---|
| A1 | Attempt **MUST** 关联到一个 Claim | MUST |
| A2 | 用量字段 **MUST** 标注 `self_reported: true` | MUST |
| A3 | Attempt **MUST NOT** 记录凭据、账号或完整对话记录 | MUST |
| A4 | 失败的 Attempt **MUST NOT** 被删除（是校准数据） | MUST |
| A5 | Attempt **SHOULD** 记录模型类别 / 能力等级，而非具体账号 | SHOULD |

---

## 3. workload_envelope（工作量信封）

不用单点估计，用**区间 + 依据等级**。单点估计会被当成承诺，区间才诚实。

### 3.1 结构

```yaml
workload_envelope:
  unit_of_measure: "unit"          # unit | shard | attempt
  human_minutes:                   # 人的注意力时间
    p50: 3
    p90: 8
    basis: "assumed"               # measured | calibrated | assumed | unknown
  model_calls:                     # 模型调用次数
    p50: 1
    p90: 3
    basis: "assumed"
  expected_attempts_per_claim:
    p50: 1
    p90: 2
    basis: "assumed"
  notes: "全部为 synthetic 假设值，无真实执行数据支撑"
```

### 3.2 basis 等级（必须诚实标注）

| basis | 含义 | 可用于 |
|---|---|---|
| `measured` | 来自本任务真实执行数据 | 正式估算 |
| `calibrated` | 来自校准批次（同类任务，样本 ≥ 校准要求） | 正式估算 |
| `assumed` | 拍脑袋 / 类比推测 | **仅供讨论**，MUST 标注 |
| `unknown` | 没有依据 | MUST 标注，MUST NOT 用于对外承诺 |

规则：
- Action 发布前，`workload_envelope.basis` **SHOULD** 至少达到 `calibrated`。
- 若为 `assumed` 或 `unknown`，发布材料 **MUST** 显式说明"工作量估算无实测依据"。
- **本仓库所有 workload_envelope 均为 `assumed`**（无任何真实执行数据）。

### 3.3 为什么不用单点值

自报用量 + 单点估计 = 参与者会把估计值当上限，超出就认为自己做错了，或者提前放弃。区间 + p90 让"这次花了 7 分钟"是正常的，不是异常。

---

## 4. 从校准到冻结发布的流程

```text
[1] draft_split        切分草案：定义 Unit 边界与验收规则
       ↓
[2] dry_review         需求方 + 协调方评审：Unit 是否真的可独立验收
       ↓
[3] calibration_batch  校准批次：小样本真实执行，测 workload 与错误率
       ↓
[4] revise             按校准结果调整 Unit 粒度 / Shard 大小 / 验收阈值
       ↓
[5] freeze             冻结 TaskDefinition：version + content_hash 固定
       ↓
[6] publish_shards     生成并发布 Shard，进入可认领
       ↓
[7] recalibrate        执行中周期性回看：超时率、返工率、实际 attempt 数
```

### 4.1 各阶段门槛

| 阶段 | 进入下一阶段的条件 | 强度 |
|---|---|---|
| [1]→[2] | 每个 Unit 有明确验收规则 | MUST |
| [2]→[3] | 需求方确认领域验收标准 | MUST |
| [3]→[4] | 校准批次完成，有实测 workload 与错误率 | SHOULD |
| [4]→[5] | 验收阈值确定，`data_policy`/`execution_policy` 确认 | MUST |
| [5]→[6] | `content_hash` 生成，version 固定 | MUST |
| [6] 期间 | 冻结后 **MUST NOT** 原地改语义；改动走新 version | MUST |

### 4.2 校准批次应测什么

- 单 Unit 实际耗时分布（p50 / p90）；
- 每 Claim 实际 Attempt 数；
- L1/L2 自动检查的通过率（衡量说明是否够清楚）；
- L4 人工判定与 L1/L2 的一致性（衡量自动检查是否够用）；
- 不同参与者之间的结果分歧率（决定 `replication_factor`）；
- 超时率（决定 `lease_duration_seconds`）。

> **当前状态：unknown。** 从未运行过校准批次。上述指标本仓库全部没有数据。

### 4.3 冻结的含义

冻结后 **MUST NOT** 改动：Unit 边界、验收规则、输出 schema、红线定义。

冻结后 **MAY** 改动（不影响已提交结果的语义）：`lease_duration_seconds`、`max_concurrent_claims`、Shard 的打包方式（对尚未认领的 Shard）。

任何对冻结项的改动 **MUST** 产生新 version，且已基于旧 version 的 Submission **MUST** 按旧 version 验收（§PROTOCOL_v0.2 2.3）。

---

## 5. 公共任务示例（**SYNTHETIC — 合成示例，非真实任务**）

> ⚠️ **本示例完全是合成的。**没有真实需求方、没有真实图片、没有真实授权、没有真实受益对象。所有 ID、数值、hash 均为演示用。**MUST NOT** 被引用为 OCC 已完成的公益成果或已开展的 Pilot。

### 5.1 场景设定（合成）

为一批**假设的**公开授权教育插图生成无障碍描述（alt text）。

```yaml
action_id: "act-synthetic-alttext-001"
title: "[SYNTHETIC] 公开授权教育插图无障碍描述"
synthetic: true
data_policy:
  sensitivity_level: "L0"
  license: "SYNTHETIC-PLACEHOLDER"     # 非真实许可
  authorization_ref: "synthetic://no-real-authorization"
  redistribution_allowed: true
  pii_present: false
execution_policy:
  execution_locus: "participant_self_controlled"
  third_party_inference_possible: true
  account_custody: "participant_self_custody"
```

### 5.2 Unit 定义（合成）

一个 Unit = 一张图片的一条无障碍描述。

满足 U1（独立验收）：判定"这张图的描述是否合格"不需要看别的图。

```yaml
unit_template:
  input_ref: "synthetic://image/{n}"
  output_schema_ref: "schemas/core/submission.schema.json#/definitions/unit_result"
  acceptance_rules:
    - id: "len"
      layer: "L2"
      rule: "描述长度 40–200 字符"
      error_code: "E_RULE_LENGTH_OUT_OF_RANGE"
    - id: "no_speculation"
      layer: "L2"
      rule: "不得推测图中未显示的信息（人物身份、地点、年代）"
      error_code: "E_RULE_SPECULATION_DETECTED"
    - id: "no_redundant_prefix"
      layer: "L2"
      rule: "不得以「一张图片显示」等冗余前缀开头"
      error_code: "E_RULE_FORBIDDEN_CONTENT"
    - id: "domain_adequacy"
      layer: "L4"
      rule: "教育语境下信息充分性由需求方判定"
      error_code: "E_HUMAN_DOMAIN_REJECT"
```

### 5.3 三个合成 Unit

| unit_id | 输入（合成） | 难度标记 |
|---|---|---|
| `unit-synthetic-001` | `synthetic://image/001` 简单示意图 | easy |
| `unit-synthetic-002` | `synthetic://image/002` 含图表的插图 | medium |
| `unit-synthetic-003` | `synthetic://image/003` 多元素场景图 | hard |

### 5.4 两个合成 Shard

```yaml
- shard_id: "shard-synthetic-a"
  unit_ids: ["unit-synthetic-001", "unit-synthetic-002"]
  lease_duration_seconds: 3600
  replication_factor: 1
  max_concurrent_claims: 1

- shard_id: "shard-synthetic-b"
  unit_ids: ["unit-synthetic-003"]
  lease_duration_seconds: 3600
  replication_factor: 2        # 难度高，取两份独立结果
  max_concurrent_claims: 2
```

注意 shard-b 展示了 Shard 与 Unit 的解耦：单个高难度 Unit 独立成 Shard 并要求重复执行。

### 5.5 合成 workload_envelope

```yaml
workload_envelope:
  unit_of_measure: "unit"
  human_minutes: { p50: 3, p90: 8, basis: "assumed" }
  model_calls:   { p50: 1, p90: 3, basis: "assumed" }
  expected_attempts_per_claim: { p50: 1, p90: 2, basis: "assumed" }
  notes: "SYNTHETIC：无任何真实执行数据，basis 一律 assumed"
```

---

## 6. 部分通过（Partial Acceptance）

### 6.1 规则

- 判定 **MUST** 逐 Unit 进行。
- Submission 的整体状态在有 pass 有 fail 时 **MUST** 为 `partially_accepted`，**MUST NOT** 整体判 `rejected`。
- 通过的 Unit **MUST** 立即产出 CanonicalResult 并可记账。
- 未通过的 Unit **MUST** 进入返工流程，**MUST NOT** 阻塞已通过部分的结算。

### 6.2 合成演练

`shard-synthetic-a` 包含 u001、u002：

```text
Submission sub-synthetic-a-1
  ├── unit-synthetic-001 → L1 pass, L2 pass, L4 pass  → accepted
  └── unit-synthetic-002 → L1 pass, L2 fail (E_RULE_LENGTH_OUT_OF_RANGE) → rejected

Submission status = partially_accepted
  → unit-synthetic-001: CanonicalResult 建立，参与者记 1 个 accepted unit
  → unit-synthetic-002: 进入返工
```

---

## 7. 返工（Rework）

### 7.1 规则

- 返工 **MUST** 通过**新 Shard** 表达，**MUST NOT** 原地重开旧 Shard。
- 返工 Shard **MUST** 设 `parent_shard_id`，**MUST** 只含未通过 Unit。
- 返工 Shard **MUST NOT** 包含已有 active CanonicalResult 的 Unit。
- 返工 Shard **SHOULD** 携带上一轮的错误码，让参与者知道要改什么。
- 返工 **MAY** 由原参与者认领，也 **MAY** 开放给他人；策略 **MUST** 在 `acceptance_policy` 中声明。
- 返工轮次 **SHOULD** 有上限；达上限后 Unit **SHOULD** 转 `human_arbitration` 或标记 `unresolvable`，**MUST NOT** 无限循环。

### 7.2 合成演练（承接 §6.2）

```yaml
- shard_id: "shard-synthetic-a-rework-1"
  parent_shard_id: "shard-synthetic-a"
  unit_ids: ["unit-synthetic-002"]        # 只有失败的那个
  rework_round: 1
  prior_error_codes: ["E_RULE_LENGTH_OUT_OF_RANGE"]
  lease_duration_seconds: 3600
```

`unit-synthetic-001` **不在**返工分片里 —— 这是本规范最重要的行为演示，也是 `examples/synthetic-action/` 与 conformance fixture 要验证的点。

---

## 8. 重复执行（Replication）与合并

### 8.1 与幂等的区别

| | Replication | Idempotency |
|---|---|---|
| 意图 | 有意多次独立执行 | 无意重复提交 |
| 结果 | 多条**不同** Submission | 去重为**一条** |
| 机制 | 不同 `claim_id` + 不同 `contributor_ref` | 相同 `idempotency_key` |
| 记账 | 每个参与者各记自己的活动证据 | 只记一次 |

**MUST NOT** 用同一机制处理两者。

### 8.2 合并规则（consensus_rule）

当 `replication_factor > 1`，`acceptance_policy.consensus_rule` **MUST** 显式声明：

| 规则 | 含义 | 适用 |
|---|---|---|
| `unanimous` | 全部一致才采纳 | 高风险、低容错 |
| `majority` | 多数一致采纳（N ≥ 3） | 有客观答案的分类任务 |
| `highest_l3_score` | 取 L3 交叉核对得分最高者 | 有 gold set 时 |
| `human_arbitration` | 人工在多份中选定 | 开放式生成任务 |

规则：
- 无声明时 **MUST** 默认 `human_arbitration`，**MUST NOT** 默认取先到者。
- `majority` 在 N = 2 时 **MUST NOT** 使用（无法产生多数），**MUST** 降级为 `human_arbitration`。
- 未被采纳的那份 Submission **MUST NOT** 被判为"错误"，**MUST** 记为 `not_selected`；其参与者的活动证据照常记录（见 `spec/CONTRIBUTION_v0.1.md`）。

### 8.3 合成演练

`shard-synthetic-b`（u003，`replication_factor: 2`）：

```text
Claim c-b-1 (contributor alpha) → sub-b-1 → L1/L2 pass
Claim c-b-2 (contributor beta)  → sub-b-2 → L1/L2 pass
L3 crosscheck: 分歧（两份描述侧重不同）
consensus_rule: human_arbitration (N=2，不可用 majority)
  → 仲裁选定 sub-b-1 → CanonicalResult(u003) ← sub-b-1
  → sub-b-2 标记 not_selected（非错误）
  → alpha 记 1 accepted unit；beta 记 1 completed attempt + not_selected
```

### 8.4 迟交与重复的碰撞

若某 Unit 已有 active CanonicalResult，此后收到针对它的 Submission：

- **MUST NOT** 自动覆盖 CanonicalResult；
- **MUST** 记录该 Submission 并标 `late=true` / `E_UNIT_ALREADY_CANONICAL`；
- **MUST** 记录该参与者的活动证据（劳动真实发生过）；
- **MAY** 在质量抽查中作为额外交叉核对样本使用。

---

## 9. Deferred / Unknown / Blocked

**Deferred**：自动切分工具、Unit 难度自动分级、动态 Shard 打包、跨 Action 的工作量基线库。

**Unknown**：真实任务的合理 Unit 粒度；真实 human_minutes 分布；合理 `replication_factor`；合理返工轮次上限；校准批次需要多大样本；不同模型间结果分歧的真实幅度。

**Blocked**：任何真实校准批次（无真实需求方与授权数据）；L1+ 任务的切分（无受控环境）；跨机构任务切分（无机构接洽）。

---

## 10. 诚实声明

- 本文件为 candidate draft，**未实现、未运行、未验证**。
- §5 示例明确标注 `synthetic: true`，**不是真实任务、不是 Pilot 成果、不代表任何真实需求方或授权数据**。
- 所有工作量数值 `basis: assumed`，**无实测依据**。
- 校准流程从未执行过；§4.2 所列指标本仓库全部没有数据。
