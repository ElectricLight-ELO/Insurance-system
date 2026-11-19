#!/usr/bin/env python3
"""Журнал применения LLM в проекте (глава 6.2 курсовой).

Каждый запуск добавляет одну строку JSON в docs/llm_log.jsonl: какой паттерн
промпта применён, какая модель, какие файлы изменены и прошёл ли результат
проверки CI (check_rules.py). Персональные данные и тексты ответов не пишутся.

Пример:
  python3 scripts/llm_log.py --prompt prompts/system_c4_architect.md \
      --model "Claude Opus 5.5" --author mrW0LFHACK \
      --files src/romanov_webapp/L1_context.puml --decision accepted
"""
import argparse, datetime, hashlib, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "docs", "llm_log.jsonl")


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True, help="файл промпта из prompts/")
    ap.add_argument("--model", required=True)
    ap.add_argument("--author", required=True, help="логин GitHub")
    ap.add_argument("--files", nargs="+", required=True, help="изменённые файлы")
    ap.add_argument("--decision", choices=["accepted", "edited", "rejected"], required=True)
    ap.add_argument("--attempt", type=int, default=1)
    a = ap.parse_args()

    head = open(os.path.join(ROOT, a.prompt), encoding="utf-8").readline()
    m = re.search(r"id:\s*([\w-]+).*версия\s*([\d.]+).*паттерн:\s*(.+)$", head)
    pid, ver, pattern = (m.group(1), m.group(2), m.group(3).strip()) if m else ("?", "?", "?")

    chk = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "check_rules.py")],
                         capture_output=True, text=True)
    viol = re.search(r"Found (\d+) violation", chk.stdout)
    rec = {
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        "author": a.author, "model": a.model,
        "prompt_id": pid, "prompt_version": ver, "pattern": pattern,
        "prompt_sha": sha(os.path.join(ROOT, a.prompt)),
        "files": {f: sha(os.path.join(ROOT, f)) for f in a.files},
        "attempt": a.attempt,
        "ci_rules": "pass" if chk.returncode == 0 else "fail",
        "ci_violations": int(viol.group(1)) if viol else 0,
        "decision": a.decision,
    }
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(json.dumps(rec, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
