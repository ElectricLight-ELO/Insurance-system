"""Генерация TypeScript-типов из Pydantic-контрактов: python gen_ts.py  →  typescript/contracts.ts"""
import sys, json
from enum import Enum
from pathlib import Path
here = Path(__file__).parent
sys.path.insert(0, str(here / "python"))
from contracts.registry import CONTRACTS, ENUMS

def ts_type(s, defs):
    if "$ref" in s: return s["$ref"].split("/")[-1]
    if "anyOf" in s:
        parts = [ts_type(x, defs) for x in s["anyOf"]]
        return " | ".join(dict.fromkeys(parts))
    if "enum" in s: return " | ".join(json.dumps(v) for v in s["enum"])
    t = s.get("type")
    if t == "string": return "string"        # uuid, date-time, Decimal-строка → string
    if t in ("integer", "number"): return "number"
    if t == "boolean": return "boolean"
    if t == "null": return "null"
    if t == "array": return f"{ts_type(s['items'], defs)}[]"
    return "unknown"

def render():
    out = ["// АВТОГЕНЕРАЦИЯ из team_lead/contracts/python (gen_ts.py). Не править вручную.", ""]
    for n, e in ENUMS.items():
        out.append(f"export type {n} = " + " | ".join(json.dumps(m.value) for m in e) + ";")
    out.append("")
    for name, (model, status, owner) in CONTRACTS.items():
        sc = model.model_json_schema()
        req = set(sc.get("required", []))
        out.append(f"/** {status} · владелец: {owner} */")
        out.append(f"export interface {name} {{")
        for f, p in sc["properties"].items():
            p = dict(p); p.pop("title", None)
            t = ts_type(p, sc.get("$defs", {}))
            if t.startswith("string") is False and "$ref" in p and p["$ref"].split("/")[-1] in ENUMS: pass
            out.append(f"  {f}{'' if f in req else '?'}: {t};")
        out.append("}")
        out.append("")
    return "\n".join(out)

if __name__ == "__main__":
    (here / "typescript" / "contracts.ts").write_text(render(), encoding="utf-8"); print("typescript/contracts.ts")
