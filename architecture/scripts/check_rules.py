#!/usr/bin/env python3
"""Проверка стандартов кодирования ИС ОСАГО (Lab 5, раздел 4.4 методички).

Правила:
  R1  запрет жёсткого позиционирования: Rel_D/U/L/R(...), Lay_*, -[hidden]-
  R2  запрет локальной стилизации: skinparam, Add*Tag, Update*Style, hide stereotype,
      инлайн-цвета #RRGGBB — разрешены только в src/core/*
  R3  у каждой стрелки Rel есть описание бизнес-действия и технический протокол
  R4  обе стороны связи объявлены в файле (защита от опечаток в ID)
  R5  ID элементов уровней L0–L3 (Person/System/Container/границы) — только из глоссария
  R6  стыковочные компоненты API имеют ID из глоссария (AuthController -> auth_comp ...),
      а L3 API объявляет их все
  R7  !include — только обёртки ../core/*.puml (никаких URL и локальных стилей)
Для сводной динамической диаграммы 4.25 действуют точечные исключения:
  R2  разрешён собственный набор параметров и тегов оформления;
  R5  разрешены пять алиасов существующих ID глоссария;
  R6  допускается префикс api_ у стыковочных компонентов;
  R7  разрешён встроенный !include <C4/C4_Dynamic>.
Остальные правила и требования к остальным файлам не меняются.
Код выхода 1, если найдено хоть одно нарушение.
"""
import csv, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pumlparse import split_args, strip_strings, DECL_RE, REL_RE, GLOBAL_KINDS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
GL = os.path.join(ROOT, "glossary", "glossary_ids.csv")

gl = {r["id"]: r for r in csv.DictReader(open(GL, encoding="utf-8"), delimiter=";")}
DOCK = {}
for i, r in gl.items():
    if r["тип"] == "Component*":
        DOCK[r["наименование"].split(" ")[0]] = i

# Сводное представление объединяет несколько локальных диаграмм и сохраняет
# их оформление и пространства имён. Исключения действуют только здесь.
GLOBAL_DYNAMIC = "src/team_tagan/4.25_dynamic_global_Tagan.puml"
GLOBAL_ALIASES = {
    "ais": "ais_osago",
    "email": "email_sys",
    "payment": "payment_sys",
    "security": "auditor",
    "insured": "payer",
}
GLOBAL_SKINPARAMS = {"defaultFontName", "wrapWidth", "dpi", "nodesep", "ranksep"}
GLOBAL_ELEMENT_TAGS = {"ext", "staff", "ctrl", "svc", "integ", "data"}
GLOBAL_REL_TAGS = {"async"}


def allowed_global_style(line):
    """Только параметры и теги оформления сводной диаграммы."""
    m = re.fullmatch(r"skinparam\s+(\w+)\s+([\w.-]+)", line)
    if m:
        return m.group(1) in GLOBAL_SKINPARAMS
    m = re.fullmatch(r'(AddElementTag|AddRelTag)\s*\(\s*"(\w+)"\s*,.*\)', line)
    if m:
        tags = GLOBAL_ELEMENT_TAGS if m.group(1) == "AddElementTag" else GLOBAL_REL_TAGS
        return m.group(2) in tags
    return False


errors, warns = [], []


def err(f, n, code, msg, line):
    errors.append((f, n, code, msg, line.strip()))


def check(path):
    rel = os.path.relpath(path, ROOT)
    is_global_dynamic = rel.replace(os.sep, "/") == GLOBAL_DYNAMIC
    lines = open(path, encoding="utf-8").read().split("\n")
    txt = "\n".join(lines)
    declared = {}
    for m in DECL_RE.finditer(txt):
        a = split_args(m.group(2))
        if a: declared[a[0]] = (m.group(1), a[1].strip('"') if len(a) > 1 else "")
    for m in re.finditer(r"\bas\s+(\w+)", txt):
        declared.setdefault(m.group(1), ("node", ""))
    is_api_l3 = rel.endswith("kiselev_api/L3_component.puml")
    stack = []
    for n, ln in enumerate(lines, 1):
        s = ln.strip()
        if not s or s.startswith("'"): continue
        bare = strip_strings(s)
        # R7
        if s.startswith("!include"):
            if not (re.fullmatch(r"!include\s+(\.\./)?core/[\w.]+\.puml", s)
                    or (is_global_dynamic and s == "!include <C4/C4_Dynamic>")):
                err(rel, n, "R7", "Подключение не через обёртку core/*.puml (URL/стили запрещены)", s)
            continue
        # R1
        mdir = re.search(r"\b((?:Rel|RelIndex|BiRel)_(?:U|D|L|R|Up|Down|Left|Right|Neighbor))\s*\(", bare)
        if mdir:
            err(rel, n, "R1", f"Macro '{mdir.group(1)}' is banned by methodologist guidelines. Use standard 'Rel()' macro.", s)
        if re.match(r"Lay_\w*\s*\(", bare) or "-[hidden]" in bare:
            err(rel, n, "R1", "Скрытые связи / Lay_* (ручное позиционирование) запрещены", s)
        # R2
        if re.match(r"(skinparam\b|Add\w*Tag\s*\(|Update\w*Style\s*\(|UpdateLayoutConfig|hide\s+stereotype)", bare):
            if not (is_global_dynamic and allowed_global_style(s)):
                err(rel, n, "R2", "Локальная стилизация запрещена — стили только в src/core/styles.puml", s)
        elif re.search(r"(?<![\w&])#[0-9A-Fa-f]{6}\b", bare):
            err(rel, n, "R2", "Инлайн-цвет запрещён — используйте $tags из core", s)
        # границы для R6
        b = re.match(r"\w*Boundary\(\s*(\w+)", s)
        if b: stack.append(b.group(1))
        elif s.startswith("}") and stack: stack.pop()
        # R5 / R6 объявления
        md = DECL_RE.match(ln)
        if md:
            kind = md.group(1); a = split_args(md.group(2)); i = a[0]; name = a[1].strip('"') if len(a) > 1 else ""
            canonical = GLOBAL_ALIASES.get(i, i) if is_global_dynamic else i
            if GLOBAL_KINDS.match(kind) and not kind.startswith("Component") and canonical not in gl:
                err(rel, n, "R5", f"ID '{i}' отсутствует в глоссарии (glossary/glossary_ids.csv)", s)
            if kind.startswith("Component") and "api" in stack and name in DOCK:
                allowed_ids = {DOCK[name]}
                if is_global_dynamic:
                    allowed_ids.add("api_" + DOCK[name])
                if i not in allowed_ids:
                    err(rel, n, "R6", f"Стыковочный компонент {name} должен иметь ID из {sorted(allowed_ids)}, а не '{i}'", s)
        # R3 / R4 связи
        mr = REL_RE.match(ln)
        if mr:
            mac = mr.group(1); a = [x for x in split_args(mr.group(2)) if not x.startswith("$")]
            off = 1 if mac.startswith("RelIndex") else 0
            if len(a) < off + 2:
                err(rel, n, "R3", "Неполная связь", s); continue
            for e in a[off:off + 2]:
                if e not in declared:
                    err(rel, n, "R4", f"Search code 404 — ID '{e}' не объявлен (опечатка или нет в глоссарии)", s)
            lab = a[off + 2].strip('"').strip() if len(a) > off + 2 else ""
            tech = a[off + 3].strip('"').strip() if len(a) > off + 3 else ""
            if not lab: err(rel, n, "R3", "У связи нет описания бизнес-действия", s)
            if not tech: err(rel, n, "R3", "У связи нет технического протокола (HTTPS/JSON, SQL/TCP 5432 ...)", s)
    if is_api_l3:
        miss = [i for i in DOCK.values() if i not in declared]
        if miss: err(rel, 0, "R6", "В L3 API не объявлены стыковочные компоненты: " + ", ".join(miss), "")


def main():
    files = sorted(p for p in glob.glob(os.path.join(SRC, "**", "*.puml"), recursive=True)
                   if os.sep + "core" + os.sep not in p)
    for p in files:
        print(f"[INFO] Rules check: {os.path.relpath(p, ROOT)}")
        check(p)
    for f, n, code, msg, line in errors:
        print(f"[ERROR] {code} in file: {f}, Line {n}\n        Error: {msg}\n        ----> {line}")
    if errors:
        print(f"Found {len(errors)} violation(s) in {len({e[0] for e in errors})} file(s).")
        print("Error: process completed with exit code 1.\nPipeline failed. Status: CRITICAL FAILURE ❌")
        sys.exit(1)
    print(f"Rules check passed: {len(files)} files, 0 violations (R1–R7). Glossary IDs: {len(gl)}.")


if __name__ == "__main__":
    main()
