"""Реестр стыков: связи между компонентами РАЗНЫХ контейнеров. Сверка с глоссарием, уровнем 2, контрактами и кодом."""
import ast, json, re, sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE.parent / "contracts" / "python"))
from tl_lib import Report, ROOT
from contracts.registry import CONTRACTS

R = Report("joints")
J = json.loads((HERE / "joints.json").read_text(encoding="utf-8"))["joints"]
G = {c["id"]: c for c in json.loads((HERE.parent / "glossary" / "glossary.json").read_text(encoding="utf-8"))["components"]}
src = (ROOT / "united" / "un_context" / "container.puml").read_text(encoding="utf-8")
ALIAS = {"web_app": "webapp", "backoffice": "backoffice", "api": "api", "worker": "worker", "db_users": "db_users", "db_tarifs": "db_tarifs", "db_audit": "db_audit", "db_files": "db_files"}
L2 = {(ALIAS.get(a, a), ALIAS.get(b, b)) for a, b in re.findall(r'^Rel\w*\((\w+),\s*(\w+),', src, re.M)}
ids = [j["id"] for j in J]
R.check(len(ids) == len(set(ids)), "J-DUP", "повторяющиеся id стыков")

def cname(t): return re.sub(r"\[\]$", "", t.replace("multipart:", ""))
for j in J:
    a, b = j["from"], j["to"]
    for x in (a, b): R.check(x in G, f"J-NOCOMP:{j['id']}:{x}", f"{j['id']}: компонента {x} нет в глоссарии")
    ca, cb = a.split(".")[0], b.split(".")[0]
    if j["kind"] in ("http", "queue"):
        R.check((ca, cb) in L2, f"J-L2:{j['id']}", f"{j['id']}: на уровне 2 нет связи {ca}→{cb}")
    else:
        v = j["via"]; R.check((ca, v) in L2 and (cb, v) in L2, f"J-L2:{j['id']}", f"{j['id']}: на уровне 2 нет связей {ca}→{v} и {cb}→{v}")
    for e in j.get("endpoints", []):
        for k in ("request", "response"):
            n = cname(e[k])
            if n not in ("-", "application/pdf", "files"):
                R.check(n in CONTRACTS, f"J-NOCONTRACT:{j['id']}:{n}", f"{j['id']}: контракта {n} нет в пакете contracts")
                if e["status"] == "implemented" and n in CONTRACTS:
                    R.check(CONTRACTS[n][1] == "implemented", f"J-STATUS:{j['id']}:{n}", f"{j['id']}: endpoint implemented, контракт {n} — {CONTRACTS[n][1]}")
    if j.get("contract"): R.check(j["contract"] in CONTRACTS, f"J-NOCONTRACT:{j['id']}", f"{j['id']}: контракта {j['contract']} нет")
    else:
        if j["kind"] != "http": R.check(False, f"{j['id']}:no-contract", f"{j['id']}: у стыка через {j.get('via')} нет контракта схемы")
    R.check(j["status"] == "ok", f"{j['id']}:{j['status']}", f"{j['id']} {a} → {b}: {j['status']}. {j['note']}")

# покрытие: все API-клиенты фронта и все контроллеры API участвуют в стыках
frm = {j["from"] for j in J}; to = {j["to"] for j in J}
for k, c in G.items():
    if c["layer"] == "API-клиенты" and c["name"] != "HttpClient":
        R.check(k in frm, f"J-UNCOVERED:{k}", f"{k}: API-клиент без единого стыка (нет принимающего контроллера)")
    if c["layer"] == "Контроллеры":
        R.check(k in to, f"J-UNCOVERED:{k}", f"{k}: контроллер без клиента")
R.check(("api", "worker") in L2 and any(j["kind"] == "queue" for j in J), "J-L2-QUEUE", "связь API→Worker не покрыта стыком")

# маршруты кода Димы == implemented-endpoints реестра
DIMA = ROOT / "Dima" / "app" / "api"
code = {}
for f in DIMA.glob("*_controller.py"):
    t = ast.parse(f.read_text(encoding="utf-8")); prefix = ""
    for n in t.body:
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call) and getattr(n.value.func, "id", "") == "APIRouter":
            prefix = next((k.value.value for k in n.value.keywords if k.arg == "prefix"), "")
    for n in ast.walk(t):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for d in n.decorator_list:
                if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr in ("get", "post", "put", "delete"):
                    rm = next((ast.unparse(k.value) for k in d.keywords if k.arg == "response_model"), None)
                    code[(d.func.attr.upper(), prefix + (d.args[0].value if d.args else ""))] = (rm, f.stem)
decl = {(e["method"], e["path"]): e for j in J for e in j.get("endpoints", []) if e["status"] == "implemented"}
for k, (rm, ctl) in code.items():
    R.check(k in decl, f"J-ROUTE-UNDECLARED:{k[0]} {k[1]}", f"маршрут {k[0]} {k[1]} есть в коде ({ctl}), но не в реестре стыков")
    if k in decl and rm: R.check(rm == decl[k]["response"] or rm.replace("list[", "").rstrip("]") + ("[]" if rm.startswith("list[") else "") == decl[k]["response"], f"J-ROUTE-RESP:{k[0]} {k[1]}", f"{k}: response_model {rm} ≠ {decl[k]['response']}")
for k in decl: R.check(k in code, f"J-ROUTE-GHOST:{k[0]} {k[1]}", f"endpoint {k[0]} {k[1]} в реестре implemented, а в коде Димы его нет")

# клиент Никиты (код) против эндпоинтов, объявленных для его компонента
cl = (ROOT / "Nikita" / "inspection_logic" / "integration" / "api_client.py").read_text(encoding="utf-8")
m = re.search(r'f"\{self\._base_url\}(/[^"]*)"', cl); url = m.group(1) if m else None
keys = set(re.findall(r'^\s+"(\w+)":', cl[cl.find("payload = {"):cl.find("try:")], re.M))
mine = [e for j in J if j["from"] == "webapp.InspectionApiClient" for e in j.get("endpoints", [])]
paths = {e["path"] for e in mine}
R.check(any(p.endswith(url) or p.rstrip("/").split("/")[-1] == url.strip("/") for p in paths) and url in {p.replace("/api/claims/{claim_id}", "") for p in paths}, "J-03:client-url",
        f"InspectionApiClient.submit_results шлёт POST {url}; в API для InspectionController есть только {sorted(paths)}")
allow = set(CONTRACTS["InspectionCreateRequest"][0].model_fields)
R.check(keys <= allow, "J-03:client-payload", f"InspectionApiClient шлёт поля {sorted(keys)}; InspectionCreateRequest принимает {sorted(allow)} (лишние: {sorted(keys - allow)})")
resp = set(re.findall(r'raw\["(\w+)"\]', cl)); rf = set(CONTRACTS["InspectionResponse"][0].model_fields)
R.check(resp <= rf, "J-03:client-response", f"InspectionApiClient читает из ответа {sorted(resp)}; InspectionResponse содержит {sorted(rf)} (нет: {sorted(resp - rf)})")
sys.exit(R.finish())
