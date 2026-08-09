# schemas/core/ — OCC v0.2 核心对象 Schema

- **状态**：candidate draft，2026-08-09。
- **对应文档**：`spec/PROTOCOL_v0.2.md`、`spec/TASK_SPLITTING_v0.1.md`、`spec/CONTRIBUTION_v0.1.md`。

## 范围

本目录是本仓库中**唯一**的 schema 集合，对应协议 v0.2 的核心对象模型。

早期实验中还存在另一批面向"机构申请与算力分配"的 schema（application / review / allocation /
execution_record / acceptance_record）及其模拟脚本。它们**未包含在本仓库内**：那部分材料属于
v0.1 时期的探索，尚未审阅，不适合作为公开讨论的起点。本目录的 schema 与它们互不覆盖。

## 本目录文件

| 文件 | 对象 | 角色 |
|---|---|---|
| `action.schema.json` | Action | 行动容器；含 data_policy / execution_policy |
| `task_definition.schema.json` | TaskDefinition | 冻结的任务语义与 acceptance_policy |
| `unit.schema.json` | Unit | **验收原子** |
| `shard.schema.json` | Shard | **认领原子** |
| `claim.schema.json` | Claim | 租约（lease / timeout） |
| `attempt.schema.json` | Attempt | **执行计量原子** |
| `submission.schema.json` | Submission | 交付；含 `definitions/unit_result` |
| `validation.schema.json` | Validation | 四层验证之一层 |
| `contribution_record.schema.json` | ContributionRecord | 记账条目 |
| `event.schema.json` | Event | append-only 状态变更 |

未单独建 schema 的对象：`CanonicalResult`、`Release`、`Dispute` —— 语义已在 `spec/PROTOCOL_v0.2.md` §2.10 / §2.12 / §7 定义，schema 列为 deferred（本轮 fixture 未覆盖其独立校验）。

## 校验方式

```bash
python3 scripts/validate_v02.py
```

该脚本**只用 Python 标准库**，内置 JSON Schema draft-07 的一个**子集**校验器（支持 type / required / enum / pattern / minimum / maximum / minLength / minItems / additionalProperties / properties / items / $ref 本地引用）。

**限制**：不是完整的 draft-07 实现。未实现 `format` 语义校验、`allOf`/`anyOf`/`oneOf`/`not`、远程 `$ref`、`patternProperties` 等。若环境中安装了 `jsonschema`，可另行做完整校验；本仓库**不依赖**它，也**不安装**它。

## 设计约束（在 schema 中强制）

- `additionalProperties: false` 遍布各对象，用于阻止 `score` / `points` / `rank` / `token_equivalent` 等统一积分与换算字段进入 ContributionRecord。
- `contributor_ref` / `actor_ref` 使用 `^pseudo-` 模式，阻止邮箱、真名、第三方账号 ID。
- `execution_policy.account_custody` 为单值枚举 `participant_self_custody`，在结构层面固化"项目不代管账号"。
- `self_reported` 为常量 `true`，防止自报用量被伪装成已核实计量。
- 所有对象支持 `synthetic: true` 标记，用于区分演示数据与（尚不存在的）真实数据。

## 边界

这些 schema 是**数据契约候选**。没有任何线上服务消费它们；没有 Control Plane、没有 API、没有 Runner。它们当前的唯一用途是本地文件校验与讨论。
