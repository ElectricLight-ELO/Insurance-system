"""Сверка глоссария с диаграммами united/un_comp и правилами именования."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tl_lib import Report, ROOT
sys.path.insert(0, str(Path(__file__).parent))
from build_glossary import parse, UN, CONT, GJ

G = json.loads(GJ.read_text(encoding="utf-8")); R = Report("glossary")
gl = {c["id"]: c for c in G["components"]}
seen = set()
for cid, (title, ctech, owner, fn) in CONT.items():
    rows = parse(UN / fn)
    for r in rows:
        key = f"{cid}.{r['name']}"; seen.add(key)
        c = gl.get(key)
        R.check(c is not None, f"G-MISSING:{key}", f"{key}: есть на диаграмме, нет в глоссарии")
        if not c: continue
        R.check(c["tech"] == r["tech"], f"G-TECH:{key}", f"{key}: технология {r['tech']!r} на диаграмме и {c['tech']!r} в глоссарии")
        R.check(c["desc"] == r["desc"], f"G-DESC:{key}", f"{key}: описание на диаграмме отличается от глоссария")
        R.check(c["layer"] == r["layer"], f"G-LAYER:{key}", f"{key}: слой {r['layer']!r} ≠ {c['layer']!r}")
    names = [r["name"] for r in rows]
    R.check(len(names) == len(set(names)), f"G-DUP:{cid}", f"{cid}: повторяющееся имя внутри контейнера")
for k in gl:
    R.check(k in seen, f"G-STALE:{k}", f"{k}: есть в глоссарии, нет на диаграмме")
# владелец и контейнер
for k, c in gl.items():
    R.check(c["owner"] == G["containers"][c["container"]]["owner"], f"G-OWNER:{k}", f"{k}: владелец не совпадает с владельцем контейнера")
    R.check(re.fullmatch(r"[A-Z][A-Za-z0-9]+", c["name"]) is not None, f"G-CASE:{k}", f"{k}: имя не в PascalCase")
# суффиксы по слою
SUF = {"Контроллеры": ("Controller",), "Сервисы": ("Service",), "API-клиенты": ("ApiClient",), "Страницы": ("Page", "Workplace", "Dashboard")}
for k, c in gl.items():
    for layer, suf in SUF.items():
        if c["layer"] == layer:
            R.check(c["name"].endswith(suf), f"G-SUFFIX:{k}", f"{k}: в слое «{layer}» имя должно оканчиваться на {'/'.join(suf)}")
    if c["layer"] == "Фасады и репозитории":
        R.check(c["name"].endswith(("Facade", "Repository")), f"G-SUFFIX:{k}", f"{k}: фасад/репозиторий без суффикса Facade/Repository")
# одноимённые компоненты обязаны иметь решение
by = {}
for c in G["components"]: by.setdefault(c["name"], []).append(c["container"])
for n, cs in by.items():
    if len(cs) > 1: R.check(n in G["homonyms"], f"G-HOMONYM:{n}", f"{n} встречается в {cs}, но решения по нему нет в homonyms")
for n in G["homonyms"]: R.check(len(by.get(n, [])) > 1, f"G-HOMONYM-STALE:{n}", f"{n}: лишняя запись homonyms")
sys.exit(R.finish())
