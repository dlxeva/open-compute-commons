# Open Compute Commons：协议 v0.2（候选草案 / candidate draft）

- **状态**：candidate draft，未发布、未实现、未上线。
- **日期**：2026-08-09。
- **上一版**：v0.1（保留在未公开的本地实验目录中，**不在本仓库内**，见 §13）。
- **本版性质**：**语义与数据契约候选（semantic & data contract candidate）**。本文件定义对象、状态、字段和错误语义，**不定义线上系统**。

> **一句话边界**：v0.2 只是一份"如果要做，对象和状态应该长这样"的契约草案。线上 Control Plane、MCP adapter、Runner、账本服务**均未实现**。文中所有 fixture、样例、任务包均为 **synthetic**，不是真实 Pilot 成果，不代表任何真实需求方、真实授权数据或真实公益产出。

---

## 0. 修订范围（v0.1 → v0.2）

本次修订回应工程反馈，范围如下：

| # | 修订项 | v0.1 状态 | v0.2 状态 |
|---|---|---|---|
| 1 | 对象模型 | 只有隐含的"任务/分片" | 补齐 11 个一级对象（§2） |
| 2 | 状态机 | 单一任务状态机混合多个生命周期 | 拆为 Action / Shard / Claim / Submission 四套（§3） |
| 3 | 版本与不可变性 | 无 | version / content_hash / 冻结语义（§4） |
| 4 | 幂等 | 无 | idempotency_key + 重放语义（§4.3） |
| 5 | 认领语义 | "领任务"一句话 | lease / timeout / 续租 / 抢占 / replication（§5） |
| 6 | 验收 | 单层"自动检查 + 人工抽检" | 四层验证 L1–L4（§6） |
| 7 | 争议与错误 | 一个 `DISPUTED` 状态 | 争议流程 + 结构化错误码表（§7） |
| 8 | 数据/执行策略 | 散落在提案 | `data_policy` / `execution_policy` 显式对象（§8） |
| 9 | 安全模型 | 零散声明 | 显式威胁模型与约束（§9） |
| 10 | 规范强度 | 无 | MUST / SHOULD / MAY + conformance profile（§10、§11） |
| 11 | 入口形态 | 未定义 | Web/CLI 为基础入口，MCP 仅可选适配器（§8.3） |
| 12 | 控制面/执行面 | 未分离 | Control Plane 与 Execution Plane 分离（§9.1） |

v0.1 中未被本文件覆盖的内容（角色定义、机构补充轨道叙事、共建问题清单）继续以 v0.1 为准。

**未在本轮修订中解决的，见 §12 deferred / unknown / blocked。**

---

## 1. 关键词与规范强度

本文件中的 **MUST / MUST NOT / SHOULD / SHOULD NOT / MAY** 按 RFC 2119 / RFC 8174 解释，仅在全大写时具有规范含义。

由于**尚无实现**，所有 MUST 的当前效力是：**任何声称兼容 OCC v0.2 的实现必须满足**；它们不构成对当前仓库或任何人的义务。

---

## 2. 对象模型（Object Model）

### 2.1 对象总览

```text
Action  (一次公共行动，最外层容器)
  └── TaskDefinition  (冻结的任务语义：做什么、怎么验收)
        └── Unit      (验收原子：能被独立判定 pass/fail 的最小工作)
              └── Shard  (认领原子：一个或多个 Unit 的打包)
                    └── Claim  (某参与者对某 Shard 的一次租约)
                          └── Attempt  (一次实际执行，计量原子)
                                └── Submission  (一次交付)
                                      └── Validation  (对 Submission 的一层判定)

CanonicalResult      (某 Unit 最终被采纳的唯一结果)
ContributionRecord   (贡献记账条目)
Release              (冻结并公开的成果集合)
Event                (所有状态变更的 append-only 记录)
```

三种原子的划分见 `spec/TASK_SPLITTING_v0.1.md`：**Unit 是验收原子，Shard 是认领原子，Attempt 是执行计量原子。**

### 2.2 Action

一次公共行动。是预算、策略、发布和账本的边界。

必备字段（MUST）：`action_id`、`version`、`status`、`title`、`purpose`、`data_policy`、`execution_policy`、`created_at`。

SHOULD：`requester_ref`（需求方引用）、`coordinator_ref`、`acceptance_policy_ref`、`result_license`、`content_hash`。

MUST NOT：包含任何参与者账号标识、API Key、令牌、cookie 或凭据引用（§9.3）。

### 2.3 TaskDefinition

Action 下的一类任务的**冻结语义**：输入形态、执行说明、输出 schema、验收规则。

必备（MUST）：`task_definition_id`、`action_id`、`version`、`status`、`instructions_ref`、`output_schema_ref`、`acceptance_policy`、`content_hash`。

关键规则：
- TaskDefinition 一旦 `status=frozen`，其语义 **MUST NOT** 原地修改；任何修改 MUST 产生新的 `version` 与新的 `content_hash`（§4）。
- 已经基于旧版本产生的 Claim/Submission **MUST** 继续按旧版本验收，除非显式作废（`superseded`）。

### 2.4 Unit

**验收原子**。一个 Unit 是能被独立判定 `pass` / `fail` 的最小工作量。

必备（MUST）：`unit_id`、`task_definition_id`、`input_ref`、`content_hash`。

SHOULD：`workload_envelope`（预计工作量区间）、`sensitivity_level`（L0–L3）。

规则：
- Unit **MUST** 可独立验收，不依赖同批其他 Unit 的结果。
- Unit **MUST NOT** 跨越 `data_policy` 中的不同敏感级别。

### 2.5 Shard

**认领原子**。一个 Shard 打包 1..N 个 Unit，是参与者能"领"的东西。

必备（MUST）：`shard_id`、`task_definition_id`、`unit_ids`（非空）、`status`、`version`、`content_hash`。

SHOULD：`lease_duration_seconds`、`max_concurrent_claims`、`replication_factor`、`parent_shard_id`（返工分片指向原分片）。

规则：
- 同一 Unit **MAY** 出现在多个 Shard 中，当且仅当为了 `replication`（重复执行取共识）或 `rework`（返工）。
- 返工 Shard **MUST** 只包含未通过的 Unit，**MUST NOT** 重新包含已产生 CanonicalResult 的 Unit（§6.5）。

### 2.6 Claim

某参与者在某时间窗内对某 Shard 的**排他或有限并发的租约**。

必备（MUST）：`claim_id`、`shard_id`、`contributor_ref`、`status`、`leased_at`、`lease_expires_at`、`idempotency_key`。

MUST NOT：包含参与者的第三方账号 ID、邮箱、API Key。`contributor_ref` **MUST** 是项目内的假名标识（pseudonymous handle）。

### 2.7 Attempt

**执行计量原子**。一次实际的执行尝试。同一 Claim 下 **MAY** 有多个 Attempt（失败重试、模型切换）。

必备（MUST）：`attempt_id`、`claim_id`、`status`、`started_at`。

SHOULD：`finished_at`、`self_reported_usage`（自报用量，见 §8.4）、`execution_environment`（自报的执行环境类别，非设备指纹）。

规则：用量数据 **MUST** 被标注为 `self_reported`，实现 **MUST NOT** 将其呈现为已核实的计量。

### 2.8 Submission

一次交付。指向具体产出物与其 hash。

必备（MUST）：`submission_id`、`claim_id`、`unit_results`（每个 Unit 一条）、`status`、`submitted_at`、`content_hash`、`idempotency_key`。

规则：
- Submission **MUST** 覆盖其 Claim 对应 Shard 的**全部** Unit；对未完成的 Unit **MUST** 显式标注 `skipped` 并给出原因码，不允许静默缺失。
- Submission 一旦提交 **MUST** 不可变；修正 **MUST** 通过新的 Submission（新 `submission_id`）表达。

### 2.9 Validation

对一个 Submission 的**一层**判定。四层各产生一条 Validation（§6）。

必备（MUST）：`validation_id`、`submission_id`、`layer`（`L1_schema`|`L2_rule`|`L3_crosscheck`|`L4_human`）、`verdict`、`decided_at`。

SHOULD：`per_unit_verdicts`、`error_codes`、`sample_ratio`（L4 抽检比例）、`validator_ref`。

规则：Validation **MUST** 是 append-only；改判 **MUST** 通过新的 Validation 记录（并在 `supersedes` 中引用被改判者）表达，**MUST NOT** 原地覆盖。

### 2.10 CanonicalResult

某 Unit **最终被采纳**的唯一结果。这是"这个 Unit 到底算谁做完了、结果是什么"的唯一权威答案。

必备（MUST）：`unit_id`、`source_submission_id`、`content_hash`、`accepted_at`。

规则：
- 一个 Unit **MUST** 至多有一个 `active` 的 CanonicalResult。
- 当 `replication_factor > 1` 时，CanonicalResult **MUST** 由 `acceptance_policy.consensus_rule` 决定（§6.4），**MUST NOT** 简单取先到者。
- 撤销 CanonicalResult **MUST** 通过新记录标记 `revoked` 并给出理由码，历史 **MUST** 保留。

### 2.11 ContributionRecord

贡献记账条目。详见 `spec/CONTRIBUTION_v0.1.md`。

关键规则：**只有在相关状态被确认后才允许记账**（Submission 已 accepted，或轨道对应的确认事件已发生）。**MUST NOT** 存在统一积分、等级分或 token-to-impact 换算。

### 2.12 Release

冻结并公开的成果集合。

必备（MUST）：`release_id`、`action_id`、`canonical_result_refs`、`content_hash`、`license`、`released_at`。

规则：Release **MUST** 不可变。修正 **MUST** 发新版本。

### 2.13 Event

所有状态变更的 append-only 记录。

必备（MUST）：`event_id`、`event_type`、`subject_type`、`subject_id`、`occurred_at`。

规则：
- 每一次 §3 中的状态转换 **MUST** 产生至少一条 Event。
- Event 日志 **MUST** 是 append-only；**MUST NOT** 删除或原地修改。
- Event **MUST NOT** 包含凭据、完整对话记录或未经同意的 PII。

---

## 3. 四套状态机（分开，不复用）

v0.1 把一切塞进一条 `DRAFT → … → COMPLETED` 链，这在工程上不可用：行动的生命周期、分片的可认领性、某人的租约、某次交付的处理进度是**四件不同的事**，会并发、会交叉。v0.2 拆开。

### 3.1 Action 状态机

```text
draft → review → open → executing → validating → releasing → closed
```

异常 / 终止：`suspended`（可恢复）、`cancelled`（终止）、`archived`。

- `draft → review`：需求与授权材料齐备。
- `review → open`：`data_policy` 与 `execution_policy` 已确认，TaskDefinition 已 frozen。
- `open → executing`：首个 Claim 建立。
- 任意状态 → `suspended`：MUST 记录理由码。`suspended` 时 **MUST NOT** 接受新 Claim，已有 Claim **MAY** 继续至到期。
- `→ cancelled`：**MUST** 保留既有 Event 与 ContributionRecord，**MUST NOT** 追溯删除已确认贡献。

### 3.2 Shard 状态机

```text
draft → open → partially_claimed → fully_claimed → completed
```

异常：`blocked`、`expired`、`rework_required`、`retired`。

- `open ↔ partially_claimed ↔ fully_claimed`：**可逆**。租约到期或释放会让 Shard 退回可认领。这是 v0.1 单链模型无法表达的关键点。
- `→ rework_required`：部分 Unit 未通过。**MUST** 派生新的返工 Shard（`parent_shard_id` 指向本 Shard），本 Shard **MUST NOT** 被原地"重开"。
- `→ completed`：其全部 Unit 均已有 active CanonicalResult。
- `→ retired`：TaskDefinition 被 supersede，本 Shard 不再有效。

### 3.3 Claim 状态机

```text
requested → active → submitted → closed
```

异常：`expired`、`released`（参与者主动放弃）、`revoked`（协调方回收）、`superseded`。

- `active` **MUST** 带 `lease_expires_at`。
- `active → expired`：到期未提交且未续租。到期 **MUST** 使对应 Shard 的该份额回到可认领状态。
- `expired` 的 Claim 下若**后续**收到 Submission：实现 **MUST** 接受该 Submission 进入验证（不丢弃已完成的劳动），但 **MUST** 标注 `late=true`，且当该 Unit 已有 active CanonicalResult 时 **MUST** 按 §6.4 的重复处理规则处理，**MUST NOT** 自动覆盖。
- `revoked` **MUST** 附理由码（§7.3）。

### 3.4 Submission 状态机

```text
received → validating → accepted
                     ↘ partially_accepted
                     ↘ rejected
                     ↘ needs_rework
```

异常：`duplicate`、`invalid`、`disputed`、`withdrawn`。

- `received → duplicate`：`idempotency_key` 命中已有记录（§4.3）。**MUST** 返回原记录，**MUST NOT** 创建第二条。
- `partially_accepted`：**部分 Unit 通过**。这是 v0.2 的一等公民状态，不是 `rejected` 的变体。通过的 Unit **MUST** 正常产出 CanonicalResult 并记账；未通过的 Unit **MUST** 进入返工流程。
- `disputed`：进入 §7 争议流程。**MUST NOT** 在争议解决前产生新的 CanonicalResult 覆盖争议标的。

### 3.5 状态机之间的关系（不变量）

以下不变量 **MUST** 成立：

1. Claim 处于 `active` ⇒ 其 Shard 处于 `partially_claimed` 或 `fully_claimed`。
2. Shard 处于 `completed` ⇒ 其所有 Unit 均有 active CanonicalResult。
3. Submission 处于 `accepted` ⇒ 其 Claim 处于 `submitted` 或 `closed`。
4. 任一 Unit 的 active CanonicalResult 数量 ≤ 1。
5. Action 处于 `closed` ⇒ 无 `active` Claim。

`scripts/validate_v02.py` 检查其中可静态检查的部分。

---

## 4. 版本、哈希与不可变性

### 4.1 版本

- 所有可冻结对象（Action、TaskDefinition、Shard、Release）**MUST** 有 `version`，格式为整数递增或 semver 字符串，同一 Action 内 **MUST** 保持一致风格。
- 冻结后修改语义 **MUST** 递增 version 并生成新 `content_hash`。
- 旧版本 **MUST** 保留可读，**MUST NOT** 被删除。

### 4.2 content_hash

- 算法 **MUST** 显式声明，推荐 `sha256`。
- 计算对象 **MUST** 是对象的**规范化序列化**（canonical JSON：键排序、UTF-8、无多余空白），且 **MUST** 排除 `content_hash` 字段自身与纯运行时字段（如 `received_at`）。
- 字段格式 **SHOULD** 为 `sha256:<64 hex>`。
- 输入数据（Unit 的 `input_ref` 指向物）**SHOULD** 也带 hash，以便验证参与者处理的是同一份输入。

> 当前仓库中的 `examples/synthetic-action/checksums.json` 为 **synthetic 演示**：其中的 hash 值可被本地重算核对，但演示的是机制，不是真实发布物的完整性证明。

### 4.3 幂等（Idempotency）

- Claim 与 Submission 的创建 **MUST** 携带 `idempotency_key`（客户端生成，建议 UUIDv4 或对内容取 hash）。
- 同一 `idempotency_key` 的重复提交 **MUST** 返回**首次**结果，**MUST NOT** 产生第二条记录、第二份 ContributionRecord 或第二次计量。
- `idempotency_key` 的作用域 **MUST** 限定在 `(action_id, contributor_ref, object_type)` 内，**MUST NOT** 全局共享。
- 若同一 key 携带**不同内容**：实现 **MUST** 拒绝并返回 `E_IDEMPOTENCY_CONFLICT`（§7.3），**MUST NOT** 静默采纳任一版本。
- 保留期 **SHOULD** ≥ Action 生命周期 + 30 天。

### 4.4 不可变对象清单

以下对象一旦创建 **MUST NOT** 原地修改：Submission、Validation、Event、CanonicalResult（撤销走新记录）、Release、已 frozen 的 TaskDefinition。

---

## 5. 认领：租约、超时与重复执行

### 5.1 Lease（租约）

- Claim **MUST** 有明确的 `lease_expires_at`。
- 默认租期 **SHOULD** 由 Shard 的 `lease_duration_seconds` 决定，**SHOULD** 参考该 Shard 的 `workload_envelope` 上界的 2–3 倍。
- 参与者 **MAY** 在到期前续租（renew）。续租 **MUST** 产生 Event，**SHOULD** 有次数上限以避免无限占用。

### 5.2 Timeout（超时）

- 租约到期 **MUST** 使 Claim 转入 `expired`，并释放 Shard 份额。
- 释放 **MUST NOT** 惩罚参与者，**MUST NOT** 自动删除其已产生的 Attempt 记录。
- 到期后的迟交见 §3.3。

### 5.3 Replication（重复执行）

重复执行是**质量手段**，不是浪费：

- `replication_factor = N` 表示同一 Unit 需要 N 份独立结果。
- 当 `N > 1`，`max_concurrent_claims` **MUST** ≥ N，且不同 Claim **MUST** 属于不同 `contributor_ref`。
- 参与者 **SHOULD NOT** 能看到同一 Unit 的他人结果（避免趋同）。实现若无法保证，**MUST** 在 Action 中声明该限制未满足。
- 共识规则见 §6.4。

### 5.4 与幂等的区别（易混淆点）

- **Replication**：*有意*的多次独立执行，产生多条**不同**的 Submission，是设计意图。
- **Idempotency**：*无意*的重复提交（网络重试、双击、脚本重跑），**MUST** 去重为一条。

两者 **MUST NOT** 混用同一机制：replication 靠不同 `claim_id`，幂等靠相同 `idempotency_key`。

---

## 6. 四层验证（Four-Layer Validation）

每一层产生一条独立的 Validation 记录。层与层之间 **MUST** 顺序执行，前一层 `fail` 时后续层 **MAY** 跳过（跳过 **MUST** 记录为 `skipped` 而非 `pass`）。

### 6.1 L1 — Schema / 结构校验（自动，MUST）

检查交付物是否符合 `output_schema_ref`：字段存在、类型正确、枚举合法、必填齐全。

- **MUST** 完全自动化，**MUST** 可离线复现。
- 失败 **MUST** 给出 `E_SCHEMA_*` 错误码与 JSON 路径。

### 6.2 L2 — 规则 / 红线校验（自动，MUST）

检查 `acceptance_policy` 中可机器判定的规则：长度区间、禁止字段、禁止推测标记、格式约束、敏感内容红线。

- 红线命中 **MUST** 直接判 `fail`，**MUST NOT** 由 L3/L4 覆盖为 pass（红线不可上诉为通过，只能通过争议流程认定"红线判定本身有误"）。

### 6.3 L3 — 交叉核对（自动或半自动，SHOULD）

- 当 `replication_factor > 1`：比较多份独立结果的一致性。
- 当有 gold set（已知答案的校准样本）：比对准确率。
- 输出 **SHOULD** 是分数与分歧点，而非单纯 pass/fail。

### 6.4 L4 — 人工抽检与领域判定（人工，MUST 对 L0 以上任务）

- **MUST** 声明 `sample_ratio` 与抽样方法。
- 抽检结果 **MAY** 外推到未抽检部分，但外推 **MUST** 显式标注为外推，**MUST NOT** 记为逐条已验。
- 领域正确性判定 **MUST** 由需求方或其委托的验收者做出，**MUST NOT** 由协调方单方面判定。

### 6.5 判定合成与部分通过

- Submission 的最终结论 **MUST** 由四层结果按 `acceptance_policy.combination_rule` 合成。
- **部分通过是默认支持的结果**：逐 Unit 判定，通过的进 CanonicalResult，未通过的进返工。
- 返工 **MUST** 只针对未通过的 Unit（生成新 Shard，`parent_shard_id` 指向原 Shard）。
- 重复执行的共识规则（`consensus_rule`）**MUST** 显式声明，可选：`unanimous`、`majority`、`highest_l3_score`、`human_arbitration`。无声明时 **MUST** 默认 `human_arbitration`，**MUST NOT** 默认取先到者。

---

## 7. 争议与错误码

### 7.1 谁可以发起争议

参与者（对自己 Submission 的判定）、需求方（对已接受结果的质量）、验收者（对他人判定）、协调方（对流程异常）。

### 7.2 争议流程

```text
raised → triage → (resolved_upheld | resolved_overturned | resolved_partial | withdrawn | unresolvable)
```

- 争议 **MUST** 有 `dispute_id`、标的对象引用、理由码、发起方。
- 争议期间标的对象 **MUST** 冻结（不产生新 CanonicalResult 覆盖）。
- 结论 **MUST** 通过**新的** Validation / CanonicalResult 记录表达，**MUST NOT** 原地改写历史。
- 仲裁人 **MUST NOT** 是被争议判定的作出者本人。
- `unresolvable`：无法判定时 **MUST** 标为 unresolvable 并保留双方记录，**MUST NOT** 强行给出结论。

> **unknown**：仲裁人如何产生、是否需要第三方、争议是否有时限 —— 无真实运行经验，本版**不定**（§12）。

### 7.3 错误码表

结构化错误码，供 L1–L4 与流程层引用。格式：`E_<域>_<原因>`。

| 错误码 | 域 | 含义 | 典型层 |
|---|---|---|---|
| `E_SCHEMA_MISSING_FIELD` | schema | 必填字段缺失 | L1 |
| `E_SCHEMA_TYPE_MISMATCH` | schema | 类型不符 | L1 |
| `E_SCHEMA_ENUM_INVALID` | schema | 枚举值非法 | L1 |
| `E_SCHEMA_EXTRA_FIELD` | schema | 不允许的额外字段 | L1 |
| `E_RULE_LENGTH_OUT_OF_RANGE` | rule | 长度越界 | L2 |
| `E_RULE_FORBIDDEN_CONTENT` | rule | 出现禁止内容 | L2 |
| `E_RULE_SPECULATION_DETECTED` | rule | 推测了未提供的信息 | L2 |
| `E_RULE_SOURCE_MODIFIED` | rule | 改动了不该改的原始数据 | L2 |
| `E_REDLINE_SENSITIVE_DATA` | redline | 涉及禁止级别数据 | L2 |
| `E_REDLINE_POLICY_VIOLATION` | redline | 违反 data/execution policy | L2 |
| `E_CROSSCHECK_DIVERGENCE` | crosscheck | 多份结果分歧超阈值 | L3 |
| `E_CROSSCHECK_GOLD_MISMATCH` | crosscheck | 校准样本不达标 | L3 |
| `E_HUMAN_DOMAIN_REJECT` | human | 领域判定不通过 | L4 |
| `E_HUMAN_INCONCLUSIVE` | human | 人工无法判定 | L4 |
| `E_CLAIM_LEASE_EXPIRED` | claim | 租约已过期 | 流程 |
| `E_CLAIM_LIMIT_EXCEEDED` | claim | 超过并发认领上限 | 流程 |
| `E_CLAIM_NOT_OWNER` | claim | 非租约持有者 | 流程 |
| `E_IDEMPOTENCY_CONFLICT` | idempotency | 同 key 不同内容 | 流程 |
| `E_DUPLICATE_SUBMISSION` | idempotency | 幂等命中，返回原记录 | 流程 |
| `E_VERSION_SUPERSEDED` | version | 基于已作废版本提交 | 流程 |
| `E_HASH_MISMATCH` | version | content_hash 不匹配 | 流程 |
| `E_STATE_ILLEGAL_TRANSITION` | state | 非法状态转换 | 流程 |
| `E_UNIT_ALREADY_CANONICAL` | state | Unit 已有 active 结果 | 流程 |

实现 **MAY** 扩展错误码，扩展 **MUST** 遵循同一命名格式，**MUST NOT** 复用上表已定义码表达不同含义。

---

## 8. data_policy 与 execution_policy

### 8.1 data_policy

显式对象，MUST 出现在 Action 上。字段：

| 字段 | 强度 | 说明 |
|---|---|---|
| `sensitivity_level` | MUST | `L0` 公开授权 / `L1` 受限 / `L2` 机构内部 / `L3` 个人隐私等 |
| `license` | MUST | 输入数据的许可 |
| `authorization_ref` | MUST | 授权证明的引用 |
| `redistribution_allowed` | MUST | 是否允许参与者再分发 |
| `pii_present` | MUST | 是否含 PII |
| `retention_policy` | SHOULD | 参与者本地留存要求 |
| `egress_constraints` | SHOULD | 允许/禁止发往哪类服务 |

规则：
- 第一阶段 **MUST** 仅接受 `sensitivity_level = L0`。
- `L1` 及以上 **MUST NOT** 进入公开认领轨道（当前状态：**blocked**，见 §12）。
- 公开轨道 **MUST NOT** 提供保密承诺：数据一旦发到参与者环境及其所用模型服务，**MUST** 假定二者均可见。

### 8.2 execution_policy

| 字段 | 强度 | 说明 |
|---|---|---|
| `execution_locus` | MUST | 执行发起位置类别（参与者自有环境 / 机构受控环境） |
| `third_party_inference_possible` | MUST | 是否可能调用第三方模型服务 |
| `account_custody` | MUST | 固定值 `participant_self_custody`（见 §9.3） |
| `allowed_tooling` | SHOULD | 允许的工具类别 |
| `reproducibility_requirements` | SHOULD | 是否要求记录模型/参数 |
| `usage_reporting` | SHOULD | 自报用量的粒度 |

**关键澄清（沿用并强化 v0.1）**：参与者在**自己控制的环境**中发起执行。模型推理**可能发生在第三方服务端**。参与者 **MUST** 自行确认所用第三方服务的服务条款、数据政策与额度限制。项目 **MUST NOT** 代管账号、**MUST NOT** 自动调用个人订阅、**MUST NOT** 声称"本地推理"。

### 8.3 入口形态：Web/CLI 基础，MCP 可选

- 基础入口 **MUST** 是 Web 与/或 CLI。任何参与者 **MUST** 能在不使用 MCP 的情况下完成完整流程（浏览 → 认领 → 执行 → 提交）。
- MCP **MAY** 作为**可选适配器**存在，**MUST NOT** 成为必需依赖，**MUST NOT** 承载 Web/CLI 不具备的特权能力。
- 任何适配器 **MUST NOT** 请求、存储或代理参与者的第三方账号凭据。

> **当前状态**：Web、CLI、MCP adapter **均未实现**（§12）。本节定义的是"若实现则必须满足"。

### 8.4 自报用量

用量字段 **MUST** 标注 `self_reported: true`。实现 **MUST NOT** 将自报用量呈现为已核实计量，**MUST NOT** 据此计算任何可兑换权益。

---

## 9. 安全模型

### 9.1 Control Plane 与 Execution Plane 分离

```text
┌─────────────────────── Control Plane ───────────────────────┐
│ Action / TaskDefinition / Unit / Shard / Claim              │
│ Validation / CanonicalResult / ContributionRecord / Event   │
│ 只处理：元数据、状态、hash、判定、账本                        │
│ MUST NOT 持有：参与者凭据、第三方账号、原始敏感数据            │
└──────────────────────────────────────────────────────────────┘
                    ▲ 只交换 (输入引用, 结果, hash, 自报用量)
                    ▼
┌────────────────────── Execution Plane ──────────────────────┐
│ 参与者自有环境 / 机构受控环境                                 │
│ 持有：参与者自己的账号与额度、实际推理调用                     │
│ MUST 由参与者或机构自己控制，MUST NOT 由项目代管               │
└──────────────────────────────────────────────────────────────┘
```

规则：
- Control Plane **MUST NOT** 具备在 Execution Plane 中执行代码的能力。
- Execution Plane **MUST NOT** 向 Control Plane 传输凭据、完整对话记录或超出 `data_policy` 允许范围的内容。
- 两个平面之间的接口 **MUST** 是数据交换，**MUST NOT** 是远程执行。

### 9.2 威胁模型（本版覆盖 / 不覆盖）

覆盖并有对策：

| 威胁 | 对策 |
|---|---|
| 重复提交刷贡献 | 幂等键 + 状态确认后记账（§4.3、§11） |
| 低质量批量交付 | L1/L2 自动 + L3 交叉 + L4 抽检（§6） |
| 结果被静默改写 | 不可变对象 + append-only Event（§4.4） |
| 抢占/囤积分片 | lease + timeout + 并发上限（§5） |
| 凭据泄露 | 凭据不进入项目（§9.3） |
| 判定者自证 | 仲裁人不得为原判定者（§7.2） |

**不覆盖（承认为残留风险）**：参与者是否真的按说明执行（只能靠自审计 + 抽检）；自报用量真实性；女巫攻击 / 多马甲；参与者环境被入侵；第三方模型服务侧的数据处理。这些 **MUST** 在任何真实 Pilot 前显式向参与者披露。

### 9.3 凭据与身份约束（硬约束）

以下为 **MUST NOT**，无例外：

- **MUST NOT** 收集、存储、代理或转发参与者的第三方账号密码、API Key、OAuth token、session cookie。
- **MUST NOT** 要求参与者将订阅额度转移给项目。
- **MUST NOT** 把订阅额度包装为可交易余额或 token。
- **MUST NOT** 收集参与者完整对话记录、设备指纹或账号邮箱作为必填项。
- **MUST NOT** 要求上传身份证明材料作为参与前提。
- 参与者标识 **MUST** 为项目内假名（`contributor_ref`）。

### 9.4 公开账本的最小化

Event 与公开账本 **MUST** 遵循最小化：只记录任务编号、状态、时间区间、贡献类型、自报用量区间、判定结论、成果引用。**MUST NOT** 记录凭据、PII、完整原始交付内容（除非 `data_policy` 明确允许公开）。

---

## 10. Conformance Levels（一致性档次）

实现可声称以下档次之一。声称 **MUST** 说明档次与未满足项。

### Profile C0 — Document-Conformant（文档一致）

- 使用 v0.2 的对象名与状态名；
- 提供 TaskDefinition、Unit、Shard 的静态定义；
- 不要求任何运行时系统。

**当前仓库处于 C0。** 详见 `docs/CONFORMANCE_REPORT.md`。

### Profile C1 — Schema-Conformant（结构一致）

- C0 全部，且
- 所有核心对象通过 `schemas/core/` 校验；
- 提供 content_hash 且可本地复算；
- 提供 valid / invalid fixture 并能区分。

### Profile C2 — Lifecycle-Conformant（生命周期一致）

- C1 全部，且
- 实现四套状态机及 §3.5 全部不变量；
- 实现幂等（§4.3）与 lease/timeout（§5）；
- 实现 L1+L2 自动验证；
- 支持部分通过与返工派生。

### Profile C3 — Operationally-Conformant（运行一致）

- C2 全部，且
- 实现 L3、L4 与争议流程；
- Control/Execution Plane 实际分离部署；
- 公开 append-only 账本；
- Web/CLI 基础入口可用。

> **C1–C3 当前均未达成**：无运行时实现。C1 的静态部分由 `scripts/validate_v02.py` 对 fixture 做了本地检查，但这只是**文件级校验**，不是服务一致性认证。

---

## 11. 记账约束（与 spec/CONTRIBUTION_v0.1.md 呼应）

- ContributionRecord **MUST** 在**状态被确认后**才创建：Submission 达 `accepted` 或 `partially_accepted`（后者只记通过部分），或对应轨道的确认事件已发生。
- **MUST NOT** 在 `received` / `validating` 阶段预记。
- **MUST NOT** 存在跨轨道的统一积分、总分、等级或排行榜作为主要呈现。
- **MUST NOT** 存在 token-to-impact 换算或任何将贡献折算为影响力/金钱的公式。
- 活动证据、质量证据、影响证据 **MUST** 分开呈现，**MUST NOT** 合并为单一数字。
- 撤销贡献（如事后发现作弊）**MUST** 通过新记录标注，**MUST NOT** 删除历史。

---

## 12. Deferred / Unknown / Blocked

明确区分三类，不含糊。

### 12.1 Deferred（有意推迟，方向已知）

| 项 | 说明 |
|---|---|
| Web / CLI 实现 | 本轮不实现，仅定义契约 |
| MCP adapter | 可选适配器，本轮不实现 |
| Runner / 执行器 | 不实现；执行留在参与者环境 |
| 账本服务与公开站点 | 不建 |
| 通知/提醒机制 | 未设计 |
| 多语言任务包 | 未设计 |
| 机构补充轨道细化 | 沿用 v0.1 §7，未细化到 v0.2 对象模型 |

### 12.2 Unknown（无证据，不猜）

| 项 | 为什么 unknown |
|---|---|
| 真实任务的合理 Unit 粒度 | 无真实任务，无真实耗时数据 |
| `workload_envelope` 的实际数值 | 样例中全为 synthetic 假设值 |
| 合理的 `replication_factor` | 取决于任务类型与质量分布，无数据 |
| L4 抽检比例应为多少 | 无真实错误率数据 |
| 争议实际发生率与仲裁机制 | 无运行经验 |
| 参与者留存与规模 | 未招募 |
| 自动验收能覆盖多少比例 | 依赖任务类型，无数据 |
| 第三方服务条款是否允许此类协作 | **未逐家核实**，不假设允许 |
| 仲裁人如何产生 | 未定 |

### 12.3 Blocked（有明确前置条件，未满足）

| 项 | 阻塞于 |
|---|---|
| 任何真实 Pilot | 无真实需求方、无真实授权数据 |
| L1+ 数据处理 | 无受控环境、无数据处理责任主体、无法律实体 |
| 受限托管模式 | 无权限/加密/删除/审计能力 |
| 机构 Credits 轨道 | 无机构接洽、无条款 |
| 公开发布仓库 / 社区帖 | 明确不在本轮范围 |
| 组织/法律主体 | 未注册 |
| 真实成果许可与署名 | 需真实任务方确认 |

---

## 13. 本仓库中与本协议配套的文件

- `spec/TASK_SPLITTING_v0.1.md`：Unit / Shard / Attempt 三种原子的切分方法学。
- `spec/CONTRIBUTION_v0.1.md`：记账语义与禁止字段。
- `schemas/core/`：v0.2 核心对象的 JSON Schema（候选数据契约）。
- `conformance/`：synthetic fixture 集（含一个负向集）。
- `scripts/validate_v02.py`：本地文件级校验器（仅标准库）。
- `examples/synthetic-action/`：synthetic 样例任务包。
- `docs/CONFORMANCE_REPORT.md`：本地校验结果与校验器能力边界。

> **关于 v0.1**：本协议的前一版 `PROTOCOL_v0.1.md`，以及一批早期的机构分配轨道 schema、案例与模拟脚本，
> 留在**未公开的本地实验目录**中，**不包含在本仓库内**。本文件中提到 v0.1 之处仅为版本沿革说明，
> 不表示本仓库存在这些文件。如果需要它们进入公开讨论，需要单独审阅后再决定是否发布（见 `PUBLISH_CHECKLIST.md`）。

---

## 14. 诚实声明（重申）

- 本协议为 **candidate draft**，未发布、未注册组织、未部署平台、未接收真实数据、未代表任何机构承诺。
- 线上 **Control Plane、MCP adapter、Runner、账本服务均未实现**。
- 所有 fixture、样例任务包、单元与分片均为 **synthetic**，**不是真实 Pilot 成果**，不构成公益产出。
- 参与者在**自己控制的环境**中执行；第三方服务条款、数据政策与额度**由参与者自行确认**；**项目不代管账号**。
- 本协议不构成对任何参与者的义务，也不构成任何机构的背书。
