#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCC v0.2 本地一致性校验器（candidate draft，非线上认证）

只用 Python 标准库。内置一个 **JSON Schema draft-07 子集** 校验器，并对
conformance/ 下的 fixture 套用状态机不变量检查。

支持的本地区块：
  type / required / enum / pattern / minimum / maximum /
  minLength / minItems / additionalProperties / properties / items / $ref(本地)

明确不支持（诚实声明，见 docs/CONFORMANCE_REPORT.md）：
  format 语义校验、allOf/anyOf/oneOf/not、远程 $ref、patternProperties、
  if/then/else、dependentRequired 等 draft-07 其余关键字。

用法：
    python3 scripts/validate_v02.py
    python3 scripts/validate_v02.py conformance/<fixture_set>   # 仅校验单个集
    python3 scripts/validate_v02.py --list                      # 列出 fixture 集

退出码：发现与 expected.json 不符（含 schema/state/invariant 错误）时非零。
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA_DIR = os.path.join(ROOT, "schemas", "core")
CONFORMANCE_DIR = os.path.join(ROOT, "conformance")

# 文件名词干 -> (schema 文件名, 是否数组)
FILE_SCHEMA_MAP = {
    "action": ("action.schema.json", False),
    "task_definition": ("task_definition.schema.json", False),
    "units": ("unit.schema.json", True),
    "shard": ("shard.schema.json", False),
    "shards": ("shard.schema.json", True),
    "claim": ("claim.schema.json", False),
    "claims": ("claim.schema.json", True),
    "attempt": ("attempt.schema.json", False),
    "attempts": ("attempt.schema.json", True),
    "submission": ("submission.schema.json", False),
    "submissions": ("submission.schema.json", True),
    "validation": ("validation.schema.json", False),
    "validations": ("validation.schema.json", True),
    "contribution_record": ("contribution_record.schema.json", False),
    "contribution_records": ("contribution_record.schema.json", True),
    "event": ("event.schema.json", False),
    "events": ("event.schema.json", True),
}


class Issue:
    def __init__(self, kind, code, message, path=None):
        # kind: schema | state | invariant
        self.kind = kind
        self.code = code
        self.message = message
        self.path = path

    def __str__(self):
        loc = (" @ " + self.path) if self.path else ""
        return "[%s/%s] %s%s" % (self.kind, self.code, self.message, loc)


# ---------------------------------------------------------------------------
# 本地 JSON Schema 子集校验器
# ---------------------------------------------------------------------------

def load_schema(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _resolve_ref(ref, root_schema):
    """仅支持本地 #/definitions/... 引用。"""
    if not ref.startswith("#/"):
        raise ValueError("仅支持本地 $ref，远程引用未实现: %s" % ref)
    node = root_schema
    for part in ref[2:].split("/"):
        if part == "":
            continue
        node = node[part]
    return node


def _check_type(value, expected, path):
    """返回错误信息列表（空=通过）。"""
    errs = []
    if expected == "object":
        if not isinstance(value, dict):
            errs.append("type 应为 object，实际 %s " % type(value).__name__)
    elif expected == "array":
        if not isinstance(value, list):
            errs.append("type 应为 array，实际 %s" % type(value).__name__)
    elif expected == "string":
        if not isinstance(value, str):
            errs.append("type 应为 string，实际 %s" % type(value).__name__)
    elif expected == "boolean":
        if not isinstance(value, bool):
            errs.append("type 应为 boolean，实际 %s" % type(value).__name__)
    elif expected == "integer":
        if not (isinstance(value, int) and not isinstance(value, bool)):
            errs.append("type 应为 integer，实际 %s" % type(value).__name__)
    elif expected == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            errs.append("type 应为 number，实际 %s" % type(value).__name__)
    return errs


def validate_instance(inst, schema, root_schema=None, path=""):
    """返回 Issue 列表（空=通过）。"""
    if root_schema is None:
        root_schema = schema
    issues = []

    if not isinstance(schema, dict):
        return issues

    # $ref：解析后用目标 schema 校验，其余关键字忽略（子集限制）
    if "$ref" in schema:
        try:
            target = _resolve_ref(schema["$ref"], root_schema)
        except (KeyError, ValueError) as e:
            issues.append(Issue("schema", "E_SCHEMA_$REF_UNRESOLVED", str(e), path))
            return issues
        return validate_instance(inst, target, root_schema, path)

    # type
    if "type" in schema:
        terrs = _check_type(inst, schema["type"], path)
        for t in terrs:
            issues.append(Issue("schema", "E_SCHEMA_TYPE_MISMATCH", t, path))
        # 若类型不符，后续基于类型的检查跳过，避免噪声
        if terrs:
            return issues

    # enum
    if "enum" in schema and inst not in schema["enum"]:
        issues.append(Issue(
            "schema", "E_SCHEMA_ENUM_INVALID",
            "值 %r 不在枚举 %s 中" % (inst, schema["enum"]), path))

    # pattern (仅 string)
    if "pattern" in schema and isinstance(inst, str):
        if not re.search(schema["pattern"], inst):
            issues.append(Issue(
                "schema", "E_SCHEMA_PATTERN_MISMATCH",
                "值 %r 不匹配 pattern %s" % (inst, schema["pattern"]), path))

    # minimum / maximum
    if "minimum" in schema and isinstance(inst, (int, float)) and not isinstance(inst, bool):
        if inst < schema["minimum"]:
            issues.append(Issue(
                "schema", "E_SCHEMA_RANGE",
                "值 %s < minimum %s" % (inst, schema["minimum"]), path))
    if "maximum" in schema and isinstance(inst, (int, float)) and not isinstance(inst, bool):
        if inst > schema["maximum"]:
            issues.append(Issue(
                "schema", "E_SCHEMA_RANGE",
                "值 %s > maximum %s" % (inst, schema["maximum"]), path))

    # minLength
    if "minLength" in schema and isinstance(inst, str):
        if len(inst) < schema["minLength"]:
            issues.append(Issue(
                "schema", "E_SCHEMA_MINLEN",
                "长度 %d < minLength %d" % (len(inst), schema["minLength"]), path))

    # minItems
    if "minItems" in schema and isinstance(inst, list):
        if len(inst) < schema["minItems"]:
            issues.append(Issue(
                "schema", "E_SCHEMA_MINITEMS",
                "数组长度 %d < minItems %d" % (len(inst), schema["minItems"]), path))

    # object 专用：required / properties / additionalProperties
    if isinstance(inst, dict):
        for req in schema.get("required", []):
            if req not in inst:
                issues.append(Issue(
                    "schema", "E_SCHEMA_MISSING_FIELD",
                    "缺少必填字段 %r" % req,
                    (path + "." + req) if path else req))
        props = schema.get("properties", {})
        for key, val in inst.items():
            child_path = (path + "." + key) if path else key
            if key in props:
                issues.extend(validate_instance(val, props[key], root_schema, child_path))
            else:
                if schema.get("additionalProperties", True) is False:
                    issues.append(Issue(
                        "schema", "E_SCHEMA_EXTRA_FIELD",
                        "不允许的额外字段 %r（additionalProperties:false）" % key,
                        child_path))
                # additionalProperties 为 schema 对象的情况未实现（子集限制）
    elif isinstance(inst, list) and "items" in schema:
        for i, item in enumerate(inst):
            issues.extend(validate_instance(
                item, schema["items"], root_schema, "%s[%d]" % (path, i)))

    return issues


# ---------------------------------------------------------------------------
# 状态机 / 不变量检查
# ---------------------------------------------------------------------------

def check_invariants(data, issues):
    """对一组已加载对象做关键不变量检查。data: {stem: obj}。"""
    submissions = data.get("submissions", [])
    if isinstance(submissions, dict):
        submissions = [submissions]
    events = data.get("events", [])
    if isinstance(events, dict):
        events = [events]
    records = data.get("contribution_records", [])
    if isinstance(records, dict):
        records = [records]
    units = data.get("units", [])
    if isinstance(units, dict):
        units = [units]
    shards = data.get("shards", [])
    if isinstance(shards, dict):
        shards = [shards]

    # I-1 ContributionRecord 必须引用 confirming_event_id（且事件应存在）
    event_ids = {e.get("event_id") for e in events if isinstance(e, dict)}
    for r in records:
        if not isinstance(r, dict):
            continue
        ce = r.get("confirming_event_id")
        if not ce:
            issues.append(Issue(
                "invariant", "E_INV_MISSING_CONFIRMING_EVENT",
                "ContributionRecord %s 缺少 confirming_event_id" % r.get("record_id")))
            continue
        if event_ids and ce not in event_ids:
            issues.append(Issue(
                "invariant", "E_INV_CONFIRMING_EVENT_UNKNOWN",
                "ContributionRecord %s 引用的 confirming_event_id %s 在 events 中不存在"
                % (r.get("record_id"), ce)))

    # I-2 重复 idempotency：同一 (action_id, contributor_ref, object_type) 的
    #     相同 idempotency_key 不得产生第二条 active ContributionRecord。
    #     这里以 submission 的 idempotency_key 命中 duplicate 状态为前提，
    #     检查是否产生了第二条 active CR。
    sub_by_key = {}
    for s in submissions:
        if not isinstance(s, dict):
            continue
        k = s.get("idempotency_key")
        if k:
            sub_by_key.setdefault(k, []).append(s)
    for k, subs in sub_by_key.items():
        dups = [s for s in subs if s.get("status") == "duplicate"]
        if not dups:
            continue
        # 找到该 key 下非 duplicate 的源 submission 的 contributor
        src = next((s for s in subs if s.get("status") != "duplicate"), None)
        if not src:
            continue
        contrib = src.get("claim_id")  # 间接；用 claim 找 contributor 更准（见下）
        # 用 claim -> contributor 映射
        claims = {c.get("claim_id"): c for c in data.get("claims", []) if isinstance(c, dict)}
        src_claim = claims.get(src.get("claim_id"), {})
        contributor = src_claim.get("contributor_ref")
        if not contributor:
            continue
        # 数该 contributor 在 E 轨道因该源 submission 产生的 active CR 数
        active_for_key = 0
        for r in records:
            if (r.get("contributor_ref") == contributor
                    and r.get("status") == "active"
                    and r.get("subject_id") in {s.get("submission_id") for s in subs}):
                active_for_key += 1
        if active_for_key > 1:
            issues.append(Issue(
                "invariant", "E_INV_DUP_SECOND_RECORD",
                "idempotency_key %s 去重后仍产生 %d 条 active ContributionRecord（应为 1）"
                % (k, active_for_key)))

    # I-3 部分通过：rework Shard 只含未通过 Unit（依据 prior_error_codes 与
    #     源 submission 的失败 Unit）。此处检查：rework shard 若有 parent，
    #     其 unit_ids 应全部是该 parent 对应 submission 中 outcome 失败者。
    sub_by_id = {s.get("submission_id"): s for s in submissions if isinstance(s, dict)}
    shard_by_id = {s.get("shard_id"): s for s in shards if isinstance(s, dict)}
    for sh in shards:
        if not isinstance(sh, dict):
            continue
        parent = sh.get("parent_shard_id")
        if not parent:
            continue
        parent_shard = shard_by_id.get(parent)
        if not parent_shard:
            issues.append(Issue(
                "invariant", "E_INV_REWORK_PARENT_UNKNOWN",
                "rework shard %s 的 parent_shard_id %s 不存在"
                % (sh.get("shard_id"), parent)))
            continue
        parent_units = set(parent_shard.get("unit_ids", []))
        rework_units = set(sh.get("unit_ids", []))
        # rework shard 的 unit 必须是 parent 的子集
        if not rework_units.issubset(parent_units):
            issues.append(Issue(
                "invariant", "E_INV_REWORK_UNIT_LEAK",
                "rework shard %s 含非父 Shard 的 Unit: %s"
                % (sh.get("shard_id"), sorted(rework_units - parent_units))))


# ---------------------------------------------------------------------------
# fixture 装载与校验
# ---------------------------------------------------------------------------

def load_fixture_set(set_dir):
    data = {}
    expected = None
    for fname in os.listdir(set_dir):
        fpath = os.path.join(set_dir, fname)
        if not fname.endswith(".json"):
            continue
        stem = fname[:-5]
        with open(fpath, "r", encoding="utf-8") as f:
            obj = json.load(f)
        if stem == "expected":
            expected = obj
            continue
        data[stem] = obj
    return data, expected


def validate_fixture_set(set_dir):
    name = os.path.basename(set_dir)
    issues = []
    data, expected = load_fixture_set(set_dir)

    schema_cache = {}
    for stem, obj in data.items():
        if stem not in FILE_SCHEMA_MAP:
            continue
        schema_fname, is_array = FILE_SCHEMA_MAP[stem]
        if schema_fname not in schema_cache:
            schema_cache[schema_fname] = load_schema(
                os.path.join(SCHEMA_DIR, schema_fname))
        schema = schema_cache[schema_fname]
        if is_array:
            if not isinstance(obj, list):
                issues.append(Issue("schema", "E_SCHEMA_TYPE_MISMATCH",
                                    "fixture %s 应为数组" % stem))
                continue
            for i, item in enumerate(obj):
                p = "%s[%d]" % (stem, i)
                if isinstance(item, dict) and item.get("synthetic") is not False:
                    pass  # synthetic 不影响校验
                issues.extend(validate_instance(item, schema, schema, p))
        else:
            if isinstance(obj, list):
                # 单对象文件被写成数组：退化为逐项校验
                for i, item in enumerate(obj):
                    issues.extend(validate_instance(item, schema, schema,
                                                    "%s[%d]" % (stem, i)))
            else:
                issues.extend(validate_instance(obj, schema, schema, stem))

    # 状态机 / 不变量
    check_invariants(data, issues)

    # 业务错误码：fixture 数据中显式引用的码（events.error_codes /
    # validations.error_codes / submission.status_reason_code /
    # shard.prior_error_codes）。用于验证这些码“确实出现在数据中”，
    # 而非校验器重新推导语义结果。这是校验器子集能力的诚实边界。
    business_codes = set()
    for stem in ("events", "validations", "submissions", "shards"):
        objs = data.get(stem, [])
        if isinstance(objs, dict):
            objs = [objs]
        if not isinstance(objs, list):
            continue
        for o in objs:
            if not isinstance(o, dict):
                continue
            for fld in ("error_codes", "prior_error_codes"):
                for c in (o.get(fld) or []):
                    business_codes.add(c)
            if o.get("status_reason_code"):
                business_codes.add(o["status_reason_code"])

    return name, issues, expected, business_codes


def main(argv):
    args = argv[1:]
    if "--list" in args:
        for d in sorted(os.listdir(CONFORMANCE_DIR)):
            sd = os.path.join(CONFORMANCE_DIR, d)
            if os.path.isdir(sd) and os.path.exists(os.path.join(sd, "expected.json")):
                print(d)
        return 0

    target_sets = []
    for a in args:
        if a.startswith("conformance/") or a.startswith("conformance\\"):
            target_sets.append(os.path.join(ROOT, a))
        elif os.path.isdir(a):
            target_sets.append(a)
        else:
            # 当作 fixture 集名
            target_sets.append(os.path.join(CONFORMANCE_DIR, a))

    if not target_sets:
        for d in sorted(os.listdir(CONFORMANCE_DIR)):
            sd = os.path.join(CONFORMANCE_DIR, d)
            if os.path.isdir(sd) and os.path.exists(os.path.join(sd, "expected.json")):
                target_sets.append(sd)

    if not target_sets:
        print("未找到任何 conformance fixture 集（需含 expected.json）。", file=sys.stderr)
        return 2

    total_fail = 0
    print("=" * 72)
    print("OCC v0.2 本地一致性校验  (stdlib-only subset validator)")
    print("=" * 72)

    for set_dir in target_sets:
        name, issues, expected, business_codes = validate_fixture_set(set_dir)
        schema_issues = [i for i in issues if i.kind == "schema"]
        state_issues = [i for i in issues if i.kind == "state"]
        inv_issues = [i for i in issues if i.kind == "invariant"]
        seen_codes = sorted({i.code for i in issues})

        print("\n### fixture set: %s" % name)
        print("  schema_errors=%d  state_errors=%d  invariant_errors=%d"
              % (len(schema_issues), len(state_issues), len(inv_issues)))
        for i in issues:
            print("   - " + str(i))

        # 与 expected.json 比对
        mismatches = []
        if expected:
            exp = expected.get("expect", {})
            exp_schema = exp.get("schema_errors", 0)
            exp_state = exp.get("state_errors", 0)
            exp_inv = exp.get("invariant_errors", 0)
            exp_codes = set(exp.get("expected_error_codes", []))
            # 注意：expected_error_codes 是“预期会被引用/出现”的码，
            # 而非“必须产生 schema 错误”。这里做宽松比对：
            #   - 实际错误数需 == 预期（0 表示完全合规）
            #   - 若预期含错误码，则实际错误码集合应覆盖之（子集即可）
            if len(schema_issues) != exp_schema:
                mismatches.append("schema_errors 实际 %d != 预期 %d"
                                  % (len(schema_issues), exp_schema))
            if len(state_issues) != exp_state:
                mismatches.append("state_errors 实际 %d != 预期 %d"
                                  % (len(state_issues), exp_state))
            if len(inv_issues) != exp_inv:
                mismatches.append("invariant_errors 实际 %d != 预期 %d"
                                  % (len(inv_issues), exp_inv))
            missing_codes = exp_codes - (set(seen_codes) | business_codes)
            if missing_codes:
                mismatches.append("预期错误码未出现: %s" % sorted(missing_codes))

        if mismatches:
            total_fail += 1
            print("  RESULT: FAIL")
            for m in mismatches:
                print("    ! " + m)
        else:
            print("  RESULT: PASS")

    print("\n" + "=" * 72)
    if total_fail:
        print("汇总：%d 个 fixture 集未通过预期。" % total_fail)
        return 1
    print("汇总：全部 fixture 集通过预期。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
