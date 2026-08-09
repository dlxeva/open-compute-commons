# OCC v0.2 Conformance Report (v0.1, candidate draft)

- **生成日期**：2026-08-09（运行时 `date`，非写死）
- **校验器**：`scripts/validate_v02.py`（仅用 Python 标准库，无 `jsonschema` 依赖）
- **Python 版本**：3.11.15（运行环境）
- **运行命令**：

```bash
python3 scripts/validate_v02.py            # 校验 conformance/ 下全部 fixture 集
python3 scripts/validate_v02.py conformance/valid   # 仅校验单个集
python3 scripts/validate_v02.py --list      # 列出 fixture 集
echo "exit=$?"                              # 全部通过为 0；任一不符为 1
```

退出码约定：发现与 `expected.json` 不符（schema / state / invariant 错误计数不符，或预期错误码未出现）时返回 **1**，全数通过返回 **0**。

---

## 重要声明：这是文件级候选校验，不是线上服务认证

本仓库处于 **C0（无运行时实现）** 阶段（见 `spec/PROTOCOL_v0.2.md` §11/§12）。`scripts/validate_v02.py`
是一个 **本地文件级数据契约校验器**。它：

- 只检查磁盘上的 JSON fixture 是否符合 `schemas/core/*.schema.json` 的**可静态检查子集**；
- 只检查 fixture 内部是否自洽（状态转换、关键不变量、错误码是否被显式引用）；
- **不**存在任何 Control Plane / API / Runner，因此**不**构成任何服务一致性认证（OCC C1–C3 均未达成）。

任何"通过"仅表示：在给定 fixture 上，本地子集校验与不变量检查与其 `expected.json` 一致。它**不**证明真实系统行为正确。

---

## 校验器能力与诚实限制（内置子集校验器）

`scripts/validate_v02.py` 内置一个 **JSON Schema draft-07 子集**校验器。明确支持的关键字：

| 关键字 | 支持 |
|---|---|
| `type` | ✅ |
| `required` | ✅ |
| `enum` | ✅ |
| `pattern` | ✅（Python `re`，与 ECMA-262 存在边缘差异，未归一化） |
| `minimum` / `maximum` | ✅ |
| `minLength` | ✅ |
| `minItems` | ✅ |
| `additionalProperties: false` | ✅（这是阻止 `score`/`points`/`rank`/`token_equivalent` 等换算字段进入 ContributionRecord 的核心机制） |
| `properties` | ✅ |
| `items` | ✅ |
| `$ref` 本地 `#/definitions/...` | ✅ |

**明确不支持（必须诚实声明）**：

- `format` 语义校验（如 `date-time`、`sha256` 仅按 `pattern` 校验，不校验时间合法性）。
- `allOf` / `anyOf` / `oneOf` / `not`。
- 远程 `$ref`（跨文件/跨 URL）。
- `patternProperties`、`additionalProperties` 为 schema 对象（仅支持布尔）。
- `if` / `then` / `else`、`dependentRequired`、`dependencies`、`uniqueItems` 等其余 draft-07 关键字。
- 数字精度/整数边界、Unicode 归一化等细枝末节。

若环境已安装 `jsonschema`，可另行做完整 draft-07 校验；本仓库**不依赖也不安装**它。

**业务错误码的处理边界**：`expected_error_codes` 比对的是 fixture 数据中**显式引用**的码
（来自 `events.error_codes`、`validations.error_codes`、`submission.status_reason_code`、
`shard.prior_error_codes`），而非校验器对语义结果的重新推导。即：校验器验证这些码"确实出现在
数据中、未被静默删除"，但不独立判定"该码是否正确"。这是子集能力的诚实边界。

---

## 每个 fixture 集结果

| fixture 集 | schema | state | invariant | 结果 | 说明 |
|---|---|---|---|---|---|
| `valid` | 0 | 0 | 0 | PASS | 完整合规路径，全对象通过 |
| `partial_acceptance_rework` | 0 | 0 | 0 | PASS | 部分通过 + 返工；引用 `E_RULE_LENGTH_OUT_OF_RANGE` |
| `duplicate_idempotency` | 0 | 0 | 0 | PASS | 幂等去重 + replication 区分；引用 `E_DUPLICATE_SUBMISSION` |
| `invalid_redline`（负向） | 3 | 0 | 1 | PASS | 故意违规，预期报 `E_SCHEMA_EXTRA_FIELD` ×2、`E_INV_MISSING_CONFIRMING_EVENT` |

退出码结果：**全部 PASS（exit 0）**。

### 明细

**valid** — 11 个对象全部符合 schema，无状态/不变量错误。`ContributionRecord` 引用了
`evt-synthetic-valid-004`（submission.accepted 确认事件）。

**partial_acceptance_rework** — schema 全通过。返工 Shard `shard-synthetic-pa-a-rework-1`
仅含失败 Unit `unit-synthetic-012`，设 `parent_shard_id` 指向源 Shard，不含已通过 Unit
（不变量 I-3 通过）。`E_RULE_LENGTH_OUT_OF_RANGE` 在 `validations` 与 `events` 中显式引用。

**duplicate_idempotency** — schema 全通过。核心不变量验证：
- `sub-synthetic-dup-2` 命中同 `idempotency_key`（`idem-sub-dup-0001`），状态 `duplicate`、
  `duplicate_of = sub-synthetic-dup-1`，**不产生第二条 active ContributionRecord**（pseudo-alpha
  在 E 轨道仅 `cr-synthetic-dup-0001` 一条 active）。
- `sub-synthetic-dup-3` 由不同 contributor（`pseudo-beta`）、不同 `idempotency_key`
  （`idem-sub-dup-0003`）产生，是 replication（设计内重复执行），产生独立合法 CR，与 idempotency
  去重区分（不变量 I-2 通过）。
- `E_DUPLICATE_SUBMISSION` 在 `events`/`submission.status_reason_code` 中显式引用。

**invalid_redline（负向测试）** — 故意违规：ContributionRecord 携带禁止字段 `score`、`points`
（`additionalProperties:false` 捕获，`E_SCHEMA_EXTRA_FIELD` ×2），且缺 `confirming_event_id`
（`E_SCHEMA_MISSING_FIELD` + 不变量 `E_INV_MISSING_CONFIRMING_EVENT`）。该 fixture 标注
`negative_test: true`，**不进入任何真实成果/贡献叙述**，仅用于确认校验器能捕获红线与非法状态。

---

## 覆盖与不覆盖项

### 已覆盖（本次收尾新增/修复后）

- 核心 schema 的 required / type / enum / pattern / minimum / maximum / minLength /
  minItems / additionalProperties / properties / items / 本地 $ref。
- 状态机不变量：
  - 部分通过只对失败 Unit 返工（rework Shard 仅含失败 Unit 且指向 parent）。
  - 重复 idempotency 不产生第二条 active ContributionRecord。
  - replication 与 duplicate 区分（不同 contributor/key 视为合法复制）。
  - ContributionRecord 必须引用存在的 `confirming_event_id`。

### 未覆盖 / 已知缺口（诚实列出）

- **CanonicalResult 对象**：`spec/PROTOCOL_v0.2.md` 多次引用，但 `schemas/core/` 未建独立 schema，
  fixture 亦未包含 `canonical_results.json`。因此不变量 #4「任一 Unit 的 active CanonicalResult ≤ 1」
  与「Shard completed ⇒ 所有 Unit 有 active CanonicalResult」**无法在本校验器中体现**，列为 deferred。
- **格式校验**：`date-time`、内容合法性等 `format` 未校验（子集限制）。
- **完整 draft-07**：`allOf/anyOf/oneOf/not/patternProperties/if-then-else` 等未实现。
- **流程层状态机穷举**：仅检查上述可静态判定的不变量；完整状态转换表（如 `received → duplicate`
  之外的全部边）未做穷举校验。
- **共识/外推正确性**：`consensus_rule`、`extrapolated` 标注的语义正确性未自动判定。
- **真实运行时行为**：本仓库无运行时，所有"通过"仅为文件级自洽。

---

## 本报告覆盖的文件

- `scripts/validate_v02.py` —— 校验器本体。
- `schemas/core/*.schema.json` —— 被套用的 schema。
- `conformance/valid/`、`conformance/partial_acceptance_rework/`、
  `conformance/duplicate_idempotency/`、`conformance/invalid_redline/` —— 四个 fixture 集。

fixture 全部为 **synthetic**。`invalid_redline` 是**有意违规的负向集**，它的"PASS"表示
"校验器如预期地报出了这些错误"，不表示该 fixture 合规。

---

## 重新运行的可复现性

```bash
python3 scripts/validate_v02.py && echo "ALL PASS"
```

若环境装有 `jsonschema`，可额外对照完整 draft-07 校验（非本仓库依赖，不在本报告中执行）。
