#!/usr/bin/env bash
# Валидация синтаксиса и рендер всех диаграмм architecture/src -> architecture/docs/images
# Использование: scripts/render.sh [путь_к_plantuml.jar]
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
JAR="${1:-$ROOT/plantuml.jar}"
export LC_ALL=C.UTF-8
J=(java -Djava.awt.headless=true -Dfile.encoding=UTF-8 -DPLANTUML_LIMIT_SIZE=16384 -jar "$JAR")
cd "$ROOT/src"
mapfile -t FILES < <(find . -name '*.puml' -not -path './core/*' | sed 's#^\./##' | sort)
mapfile -t DIRS < <(printf '%s\n' "${FILES[@]}" | xargs -n1 dirname | sort -u)
echo "[INFO] $("${J[@]}" -version 2>/dev/null | head -1)"
echo "[INFO] Найдено диаграмм: ${#FILES[@]}"
TMP=$(mktemp -d); FAIL=0
# --- Этап 1. Валидация синтаксиса = компиляция в PNG (одна JVM на папку) ---
for d in "${DIRS[@]}"; do
  mapfile -t DF < <(printf '%s\n' "${FILES[@]}" | awk -F/ -v d="$d" '(d=="." && NF==1) || (d!="." && $1==d)')
  for f in "${DF[@]}"; do echo "[INFO] Checking PlantUML syntax for src/$f..."; done
  o="$ROOT/docs/images/$d"; mkdir -p "$o"
  "${J[@]}" -tpng -o "$o" "${DF[@]}" > "$TMP/out.txt" 2>&1 || true
  if grep -q "Error line" "$TMP/out.txt"; then
    FAIL=1
    grep "Error line" "$TMP/out.txt" | while read -r l; do
      file=$(echo "$l" | sed 's/.*in file: //'); line=$(echo "$l" | sed 's/Error line \([0-9]*\).*/\1/')
      echo "[ERROR] Syntax Error in file: src/$file, Line $line"
      echo "        ----> $(sed -n "${line}p" "$file" 2>/dev/null)"
      echo "        Error: PlantUML cannot parse this line (незакрытая скобка/кавычка или неизвестный макрос)"
    done
  fi
done
if [ $FAIL -ne 0 ]; then
  echo "Error: process completed with exit code 1."
  echo "Pipeline failed. Status: CRITICAL FAILURE ❌"; exit 1
fi
echo "Parsed ${#FILES[@]} files successfully. No structural or syntax errors detected."
# --- Этап 2. Векторные артефакты SVG и отчёт ---
echo "Executing Graphviz layout calculation engine..."
for d in "${DIRS[@]}"; do
  mapfile -t DF < <(printf '%s\n' "${FILES[@]}" | awk -F/ -v d="$d" '(d=="." && NF==1) || (d!="." && $1==d)')
  o="$ROOT/docs/images/$d"
  "${J[@]}" -tsvg -o "$o" "${DF[@]}" >/dev/null 2>&1 || { echo "[ERROR] SVG render failed in src/$d"; FAIL=1; }
  for f in "${DF[@]}"; do b=$(basename "$f" .puml); p="$o/$b.png"; pre=$( [ "$d" != "." ] && echo "$d/" )
    if [ -s "$p" ] && [ -s "$o/$b.svg" ]; then
      echo "Successfully rendered artifact: docs/images/$pre$b.png [Size: $(python3 -c "import struct,sys;d=open(sys.argv[1],'rb').read(24);print('%dx%d'%struct.unpack('>II',d[16:24]))" "$p")] + $b.svg"
    else echo "[ERROR] Artifact missing: docs/images/$pre$b"; FAIL=1; fi
  done
done
rm -rf "$TMP"
if [ $FAIL -ne 0 ]; then echo "Pipeline failed. Status: CRITICAL FAILURE ❌"; exit 1; fi
echo "Job completed with exit code 0. Status: SUCCESS ✅"
