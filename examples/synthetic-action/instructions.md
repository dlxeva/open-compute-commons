# SYNTHETIC 任务说明（instructions_ref 目标）

> **本文件是合成演示。** 它被 `task_definition.json` 的 `instructions_ref` 指向，用于说明"冻结的任务语义"在文件层面长什么样。
> 它**不是**真实任务说明，**没有**真实任务方，**不可**替代真实授权数据下的作业指导。

## 任务目标（synthetic）

为每个 Unit 的输入（`input_ref` 指向的合成占位物）撰写一段客观描述。

## 输出要求

| 项 | 要求 |
|---|---|
| 格式 | 单段纯文本，写入 `unit_result.output` |
| 长度 | 40–200 字符（含端点） |
| 语气 | 客观描述，MUST NOT 臆造输入中不存在的事实 |
| 敏感内容 | MUST NOT 含 PII、凭据或 L1+ 敏感内容（红线规则） |

## 无法完成时

MUST NOT 静默省略。将该 Unit 的 `outcome` 设为 `skipped`，并附 `skip_reason_code`（格式 `E_[A-Z_]+`）。
Submission MUST 覆盖所属 Shard 的全部 Unit。

## 返工

若某 Unit 未通过验收，原 Shard 转 `rework_required`，由派生的返工 Shard 承接，且返工 Shard **只含未通过的 Unit**。已产生 CanonicalResult 的 Unit MUST NOT 被重新包含。

## 边界

- 本说明不构成对任何人的义务。
- 无认领入口、无提交入口、无评审者。本包不可执行。
