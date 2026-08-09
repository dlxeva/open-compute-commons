# examples/synthetic-action —— SYNTHETIC 样例任务包

> **状态**：synthetic 演示，2026-08-09。对应 `spec/PROTOCOL_v0.2.md`（candidate draft）与 `schemas/core/`。

## 一句话

这是一组**声明式文件**，用来展示一个 OCC Action Package 在**文件层面**长什么样。它**不能被执行**，**没有真实任务方**，**不产生任何成果**。

## 明确不是什么

| 它不是 | 说明 |
|---|---|
| 真实 Pilot | 没有 Pilot 发生过。没有参与者、没有认领、没有提交、没有验收。 |
| 公益成果 | 内容全部为占位字符串，对任何人都没有使用价值。 |
| 真实授权数据的替代品 | `input_ref` 指向 `synthetic://` 占位符，不指向任何真实文件。真实任务 MUST 有真实的 `authorization_ref`。 |
| 可运行的软件 | 本目录**不含可执行代码**，且**按约定不得放入**。完整性检查用外部临时命令执行。 |
| 工作量证据 | 所有 `workload_envelope.basis` 均为 `assumed`，`calibration_status=not_started`，无任何实测。 |

## 文件清单

| 文件 | 角色 | 对应 schema |
|---|---|---|
| `README.md` | 本文件 | — |
| `manifest.json` | 包清单与边界声明 | — |
| `action.json` | Action 容器（data_policy / execution_policy） | `schemas/core/action.schema.json` |
| `task_definition.json` | 冻结的任务语义与 acceptance_policy | `schemas/core/task_definition.schema.json` |
| `units.json` | 3 个 synthetic Unit（验收原子） | `schemas/core/unit.schema.json` |
| `shards.json` | 2 个 Shard（认领原子），含 1 个返工 Shard | `schemas/core/shard.schema.json` |
| `acceptance_policy.json` | 验收策略的可读副本 | — |
| `instructions.md` | `instructions_ref` 指向的任务说明 | — |
| `checksums.json` | 完整性清单 | — |

## 演示的那条路径

```
shard-synthetic-sample-a  (unit-001, unit-002, unit-003)
        │
        ├── unit-001  通过
        ├── unit-002  未通过  → E_RULE_LENGTH_OUT_OF_RANGE
        └── unit-003  通过
        │
        ▼  原 Shard MUST NOT 原地重开，转 rework_required
shard-synthetic-sample-a-rework-1  (只含 unit-002)
        parent_shard_id = shard-synthetic-sample-a
        rework_round    = 1
```

要点：**返工 Shard 只含未通过的 Unit**。已通过的 unit-001 与 unit-003 已有 CanonicalResult，MUST NOT 被重新包含——否则会重复计量同一份工作。

这条路径的判定结果是**手工推演写入文件的**，不是任何程序算出来的。没有验证服务读过这些文件。

## 完整性核对

`checksums.json` 中 `algorithm=sha256` 的条目是**真实计算出的哈希**，可用 Python 标准库重算核对：

```
python3 -c "import hashlib,json,pathlib; d=pathlib.Path('examples/synthetic-action'); m=json.loads((d/'checksums.json').read_text()); [print(('OK  ' if hashlib.sha256((d/f['path']).read_bytes()).hexdigest()==f['sha256'] else 'FAIL'), f['path']) for f in m['files']]"
```

（在仓库根目录运行。`checksums.json` 自身不在被校验列表内——它无法包含自己的哈希。）

### 哪些是演示占位

必须分清两类哈希：

| 类别 | 位置 | 真假 |
|---|---|---|
| **文件哈希** | `checksums.json` 的 `files[].sha256` | **真实**。对文件字节做 sha256，可重算核对。 |
| **对象 content_hash** | 各 JSON 内的 `content_hash` / `input_hash` 字段，全为 64 个 `0` | **演示占位**。真实实现 MUST 对规范化序列化（键排序、UTF-8、排除 `content_hash` 自身）计算，本样例**未实现该规范化过程**。 |

换句话说：文件级完整性机制是**真的可核对**的；对象级 `content_hash` 只是**字段形态占位**。`spec/PROTOCOL_v0.2.md` §4.2 描述了正确算法，本包未实现它。

## 边界

- 本包不含外部链接。所有引用为仓库内相对路径或 `synthetic://` 占位符。
- 本包不需要网络访问。
- 敏感级别 L0，无 PII。项目**不处理 L1+ 数据**，**不代管账号**。
- 修改本包内任何文件后，`checksums.json` 中对应哈希即失效，需重算。
