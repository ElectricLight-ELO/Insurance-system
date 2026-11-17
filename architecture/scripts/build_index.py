#!/usr/bin/env python3
"""Собирает интерактивную карту архитектуры docs/index.html из docs/images/**.svg
и глоссария. Запускается в CI после рендера."""
import csv, html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "docs", "images")
OWNERS = [("team_tagan", "Таган А.М.", "тимлид, общая сборка"),
          ("kiselev_api", "Киселев Д.А.", "API · ДТП и осмотр"),
          ("uskov_worker", "Усков М.В.", "Worker · финансы"),
          ("mekhova_backoffice", "Мехова А.С.", "Backoffice"),
          ("romanov_webapp", "Романов Н.И.", "Web App")]
LEVELS = [("L0_landscape", "L0 Ландшафт"), ("L1_context", "L1 Контекст"), ("L2_container", "L2 Контейнеры"),
          ("L3_component", "L3 Компоненты"), ("L4_code", "L4 Код"), ("dynamic", "Динамика"),
          ("deployment", "Развёртывание")]


def title_of(svg):
    try:
        t = open(svg, encoding="utf-8").read(200000)
        m = re.search(r"<title>(.*?)</title>", t) or re.search(r'font-weight="bold"[^>]*>([^<]{8,})<', t)
        return html.unescape(m.group(1)) if m else ""
    except OSError:
        return ""


cells, items = [], []
items.append(("main", "Сводная диаграмма контейнеров (main.puml)", "images/main.svg", "images/main.png"))
rows = ""
for d, who, role in OWNERS:
    r = f"<tr><th>{who}<small>{role}</small></th>"
    for lv, name in LEVELS:
        svg = os.path.join(IMG, d, lv + ".svg")
        if d == "team_tagan" and lv == "L2_container" and not os.path.exists(svg):
            svg = os.path.join(IMG, "main.svg")
        if os.path.exists(svg):
            rel = os.path.relpath(svg, os.path.join(ROOT, "docs")).replace(os.sep, "/")
            key = f"{d}/{lv}"
            items.append((key, f"{who} — {name}", rel, rel[:-4] + ".png"))
            r += f'<td><button data-k="{key}">✅ {name.split()[0]}</button></td>'
        elif d == "team_tagan" and lv in ("L3_component", "L4_code"):
            r += '<td class="na">— у контейнеров</td>'
        else:
            r += '<td class="miss">❌ нет</td>'
    rows += r + "</tr>\n"

gl = list(csv.DictReader(open(os.path.join(ROOT, "glossary", "glossary_ids.csv"), encoding="utf-8"), delimiter=";"))
glrows = "".join(f"<tr><td><code>{html.escape(g['id'])}</code></td><td>{html.escape(g['тип'])}</td>"
                 f"<td>{html.escape(g['наименование'])}</td><td>{html.escape(g['владелец'])}</td><td>{g['уровни']}</td></tr>"
                 for g in gl)
js_items = ",\n".join(f'"{k}":{{"t":{t!r},"svg":"{s}","png":"{p}"}}'.replace("'", '"') for k, t, s, p in items)

page = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ИС ОСАГО — карта архитектуры C4</title>
<style>
:root{{--bg:#f7f8fa;--fg:#1d2433;--mut:#5b6476;--line:#d9dee7;--acc:#2E86C1;--card:#fff}}
@media (prefers-color-scheme:dark){{:root{{--bg:#14171c;--fg:#e6e9ef;--mut:#9aa3b2;--line:#2b313b;--acc:#5aa9e0;--card:#1b1f26}}}}
body{{margin:0;font:15px/1.45 system-ui,sans-serif;background:var(--bg);color:var(--fg)}}
header{{padding:20px 16px;border-bottom:1px solid var(--line)}} h1{{margin:0;font-size:22px}}
header p{{margin:4px 0 0;color:var(--mut)}} main{{padding:16px;max-width:1400px;margin:auto}}
table{{border-collapse:collapse;width:100%;background:var(--card)}} th,td{{border:1px solid var(--line);padding:6px 8px;text-align:left}}
th small{{display:block;color:var(--mut);font-weight:400}} .wrap{{overflow-x:auto}}
button{{font:inherit;border:1px solid var(--line);background:transparent;color:var(--fg);border-radius:6px;padding:3px 8px;cursor:pointer}}
button:hover,button.on{{border-color:var(--acc);color:var(--acc)}} .na{{color:var(--mut)}} .miss{{color:#c0392b}}
#view{{margin-top:16px;background:#fff;border:1px solid var(--line);border-radius:8px;min-height:200px}}
#vt{{display:flex;gap:12px;align-items:center;padding:8px 12px;border-bottom:1px solid #ddd;color:#222;flex-wrap:wrap}}
#vt a{{color:#2E86C1}} #pic{{overflow:auto;max-height:80vh}} #pic img{{display:block;max-width:none}}
h2{{font-size:18px;margin:24px 0 8px}}
</style></head><body>
<header><h1>ИС ОСАГО — интерактивная карта архитектуры C4</h1>
<p>Собрано CI/CD (GitHub Actions) из <code>architecture/src</code>. Нажмите на ячейку, чтобы открыть диаграмму; ползунок — масштаб.</p></header>
<main>
<p><button data-k="main" class="on">Сводная диаграмма контейнеров (main.puml)</button></p>
<div class="wrap"><table><tr><th>Участник</th>{''.join(f'<th>{n}</th>' for _, n in LEVELS)}</tr>
{rows}</table></div>
<div id="view"><div id="vt"><b id="vtitle"></b><span>масштаб <input id="z" type="range" min="20" max="200" value="60"></span>
<a id="lsvg" target="_blank">SVG</a><a id="lpng" target="_blank">PNG</a></div><div id="pic"><img id="img" alt=""></div></div>
<h2>Глоссарий глобальных ID</h2><div class="wrap"><table><tr><th>ID</th><th>Тип</th><th>Наименование</th><th>Владелец</th><th>Уровни</th></tr>{glrows}</table></div>
</main>
<script>
const D={{{js_items}}};
const img=document.getElementById('img'),z=document.getElementById('z');
function show(k){{const d=D[k];if(!d)return;img.src=d.svg;document.getElementById('vtitle').textContent=d.t;
document.getElementById('lsvg').href=d.svg;document.getElementById('lpng').href=d.png;
document.querySelectorAll('button[data-k]').forEach(b=>b.classList.toggle('on',b.dataset.k===k));}}
img.onload=()=>{{img.dataset.w=img.naturalWidth;zoom();}}
function zoom(){{if(img.dataset.w)img.style.width=(img.dataset.w*z.value/100)+'px';}}
z.oninput=zoom;
document.querySelectorAll('button[data-k]').forEach(b=>b.onclick=()=>show(b.dataset.k));
show('main');
</script></body></html>"""
open(os.path.join(ROOT, "docs", "index.html"), "w", encoding="utf-8").write(page)
print(f"Interactive map: docs/index.html ({len(items)} diagrams, {len(gl)} glossary IDs)")
