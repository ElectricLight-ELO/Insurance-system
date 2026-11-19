"""Глоссарий компонентов ИС ОСАГО.

    python build_glossary.py --init   # ОДИН РАЗ: собрать glossary.json из united/un_comp/*.puml
    python build_glossary.py          # пересобрать GLOSSARY.md из glossary.json

Источник истины — glossary.json. Диаграммы обязаны с ним совпадать (verify_glossary.py).
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UN = ROOT / "united" / "un_comp"
GJ = Path(__file__).with_name("glossary.json")
CONT = {
    "api": ("API", "FastAPI", "Дима", "api_component.puml"),
    "worker": ("Worker", "Python / Celery", "Миша", "worker_component.puml"),
    "backoffice": ("Backoffice", "React SPA", "Амелия", "backoffice_component.puml"),
    "webapp": ("Web App", "React SPA", "Никита", "webapp_component.puml"),
}
# решения тимлида по одноимённым компонентам в разных контейнерах
HOMONYMS = {
    "AuthLogic": ("same_role", "Одна и та же логика хранения токена и роли; допускается общий пакет фронта."),
    "HttpClient": ("same_role", "Один и тот же axios-клиент; допускается общий пакет фронта."),
    "AppRouter": ("different_role", "Разные наборы маршрутов и ролей (Web App — клиент/агент/эксперт, Backoffice — админ/поддержка/финансы)."),
    "AuthApiClient": ("different_role", "Один и тот же endpoint входа по коду, но разные клиенты; тело запроса задаёт contracts.auth."),
    "AuditService": ("different_role", "API пишет события аудита, Worker пишет статусы задач и логи."),
    "AisOsagoFacade": ("same_interface", "API: КБМ, ТС, водители, полис. Worker: регистрация договора, повторная проверка. Нужен ОДИН интерфейс IAisOsagoGateway."),
    "EmailFacade": ("same_interface", "API: вопросы и корректировки. Worker: полисы, чеки, отчёты. Нужен один интерфейс IEmailGateway."),
    "PaymentGatewayFacade": ("same_interface", "API: создание сессии и отчёты о поступлениях. Worker: статусы платежей для сверки. Один интерфейс IPaymentGateway."),
    "FileRepository": ("same_interface", "API пишет фото и подписи, Worker читает их и пишет PDF. Один интерфейс IFileRepository и одна схема документов DB_FILES."),
    "TariffRepository": ("same_interface", "API читает и меняет тарифы, Worker читает данные для расчёта и пишет маржу. Одна схема DB_TARIFS."),
}

def q(s): return s.replace("\\n", " ").strip()
def parse(path):
    layer, rows = "", []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*' --- (.+?) ---", line)
        if m: layer = m.group(1); continue
        m = re.match(r'\s*Component\((\w+),\s*"([^"]*)",\s*"([^"]*)",\s*"([^"]*)"(.*)\)\s*$', line)
        if m: rows.append(dict(alias=m[1], name=m[2], tech=m[3], desc=q(m[4]), layer=layer, tags=m[5]))
    return rows

def init():
    comps = []
    for cid, (title, ctech, owner, fn) in CONT.items():
        for r in parse(UN / fn):
            comps.append(dict(id=f"{cid}.{r['name']}", container=cid, name=r["name"], layer=r["layer"], tech=r["tech"],
                              desc=r["desc"], owner=owner, alias=r["alias"], status="changed" if "changed" in r["tags"] else "base"))
    G = dict(version=1,
             containers={k: dict(title=v[0], tech=v[1], owner=v[2], diagram=f"united/un_comp/{v[3]}") for k, v in CONT.items()},
             homonyms=HOMONYMS, components=comps)
    GJ.write_text(json.dumps(G, ensure_ascii=False, indent=1), encoding="utf-8")
    print("glossary.json:", len(comps), "компонентов")

def md():
    G = json.loads(GJ.read_text(encoding="utf-8"))
    out = ["# Глоссарий компонентов ИС ОСАГО", "",
           "> Файл сгенерирован из `glossary.json` (`python build_glossary.py`). Вручную не править.", "",
           f"Всего компонентов: **{len(G['components'])}**. " + ", ".join(
               f"{v['title']} — {sum(1 for c in G['components'] if c['container']==k)}" for k, v in G["containers"].items()) + ".", ""]
    for k, v in G["containers"].items():
        out += [f"## {v['title']} ({v['tech']}) — владелец: {v['owner']}", "", "| Компонент | Слой | Технология | Описание | Статус |", "|---|---|---|---|---|"]
        for c in G["components"]:
            if c["container"] == k:
                out.append(f"| `{c['name']}` | {c['layer']} | {c['tech']} | {c['desc']} | {'изменён на ревью' if c['status']=='changed' else 'базовый'} |")
        out.append("")
    out += ["## Одноимённые компоненты в разных контейнерах", "", "| Имя | Где | Решение | Комментарий |", "|---|---|---|---|"]
    for n, (kind, note) in G["homonyms"].items():
        where = ", ".join(c["container"] for c in G["components"] if c["name"] == n)
        out.append(f"| `{n}` | {where} | {kind} | {note} |")
    (Path(__file__).with_name("GLOSSARY.md")).write_text("\n".join(out) + "\n", encoding="utf-8")
    print("GLOSSARY.md")

if __name__ == "__main__":
    init() if "--init" in sys.argv else None
    md()
