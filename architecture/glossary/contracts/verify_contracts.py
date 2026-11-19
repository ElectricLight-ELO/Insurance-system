"""Сверка пакета contracts с кодом Димы (схемы, перечисления) и со сгенерированными TypeScript-типами."""
import ast, sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE / "python")); sys.path.insert(0, str(HERE))
from tl_lib import Report, ROOT
from contracts.registry import CONTRACTS, ENUMS
import gen_ts

R = Report("contracts")
DIMA = ROOT / "Dima" / "app"

def fields(src, cls_names=None):
    out = {}
    for n in ast.parse(src).body:
        if isinstance(n, ast.ClassDef) and (cls_names is None or n.name in cls_names):
            out[n.name] = {s.target.id: (ast.unparse(s.annotation), s.value is not None)
                           for s in n.body if isinstance(s, ast.AnnAssign)}
    return out

# 1. TypeScript актуален
ts = HERE / "typescript" / "contracts.ts"
R.check(ts.exists() and ts.read_text(encoding="utf-8") == gen_ts.render(), "C-TS-STALE", "contracts.ts не соответствует Pydantic-моделям: запустите python contracts/gen_ts.py")
# 2. схемы Димы == implemented-контракты
code = fields((DIMA / "api" / "schemas.py").read_text(encoding="utf-8"))
mine = {}
for f in (HERE / "python" / "contracts").glob("*.py"): mine.update(fields(f.read_text(encoding="utf-8")))
for name, (model, status, owner) in CONTRACTS.items():
    R.check(name in mine, f"C-NOCLASS:{name}", f"{name}: нет класса в пакете")
    if status == "implemented":
        R.check(name in code, f"C-NOCODE:{name}", f"{name}: помечен implemented, но в Dima/app/api/schemas.py его нет")
        if name in code:
            a = {k: v for k, v in code[name].items()}
            R.check(a == mine[name], f"C-DRIFT:{name}", f"{name}: поля кода {sorted(a)} ≠ поля контракта {sorted(mine[name])} или различаются типы/обязательность")
for name in code:
    R.check(name in CONTRACTS, f"C-UNREGISTERED:{name}", f"{name}: схема есть в коде Димы, но не внесена в контракты")
# 3. перечисления
def enum_vals(path):
    out = {}
    for n in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(n, ast.ClassDef):
            out[n.name] = {s.targets[0].id: s.value.value for s in n.body if isinstance(s, ast.Assign) and isinstance(s.value, ast.Constant)}
    return out
dz = enum_vals(DIMA / "domain" / "enums.py")
nz = enum_vals(ROOT / "Nikita" / "inspection_logic" / "domain" / "enums.py")
for name, e in ENUMS.items():
    mine_v = {m.name: m.value for m in e}
    for src, label in ((dz, "Dима"), (nz, "Никита")):
        if name in src:
            R.check(src[name].items() <= mine_v.items(), f"C-ENUM:{name}:{label}", f"{name}: значения в коде ({label}) {src[name]} не входят в контракт {mine_v}")
for n in dz: R.check(n in ENUMS, f"C-ENUM-UNREG:{n}", f"перечисление {n} из кода Димы не внесено в контракты")
for n in nz: R.check(n in ENUMS, f"C-ENUM-UNREG:{n}", f"перечисление {n} из кода Никиты не внесено в контракты")
# 4. каждая модель собирает JSON Schema
for name, (model, *_ ) in CONTRACTS.items():
    try: model.model_json_schema(); R.ok += 1
    except Exception as e: R.check(False, f"C-SCHEMA:{name}", f"{name}: {e}")
sys.exit(R.finish())
