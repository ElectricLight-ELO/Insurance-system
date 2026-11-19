#!/usr/bin/env bash
# Рендер C4-диаграмм PlantUML в SVG + PNG.
set -euo pipefail

JAR="${1:?usage: render.sh <plantuml.jar>}"
SRC_DIR="src"
OUT_DIR="docs/images"

# 1. Проверка окружения
if ! command -v dot >/dev/null 2>&1; then
  echo "[ERROR] Graphviz 'dot' не найден в PATH." >&2
  exit 1
fi
GRAPHVIZ_DOT="$(command -v dot)"
echo "[INFO] Graphviz: ${GRAPHVIZ_DOT} ($(dot -V 2>&1))"

if [[ ! -f "$JAR" ]]; then
  echo "[ERROR] PlantUML jar не найден: $JAR" >&2
  exit 1
fi

# 2. Собираем список .puml и заранее готовим каталоги
mapfile -t FILES < <(find "$SRC_DIR" -type f -name '*.puml' | sort)
echo "[INFO] Найдено диаграмм: ${#FILES[@]}"

for f in "${FILES[@]}"; do
  rel="${f#"$SRC_DIR"/}"
  out_sub="$(dirname "$rel")"
  mkdir -p "${OUT_DIR}/${out_sub}"
  echo "[INFO] Output dir: ${OUT_DIR}/${out_sub}"
done

# 3. Синтаксическая проверка
echo "[INFO] Checking PlantUML syntax..."
java -DGRAPHVIZ_DOT="$GRAPHVIZ_DOT" -jar "$JAR" -checkonly "${FILES[@]}"

# 4. Рендер SVG и PNG
echo "[INFO] Rendering SVG..."
java -DGRAPHVIZ_DOT="$GRAPHVIZ_DOT" -jar "$JAR" \
  -tsvg -nometadata -failfast2 \
  -o "$(pwd)/${OUT_DIR}" \
  "${FILES[@]}"

echo "[INFO] Rendering PNG..."
java -DGRAPHVIZ_DOT="$GRAPHVIZ_DOT" -jar "$JAR" \
  -tpng -nometadata -failfast2 \
  -o "$(pwd)/${OUT_DIR}" \
  "${FILES[@]}"

# 5. Пост-проверка артефактов
MISSING=0
for f in "${FILES[@]}"; do
  rel="${f#"$SRC_DIR"/}"
  svg="${OUT_DIR}/${rel%.puml}.svg"
  if [[ ! -s "$svg" ]]; then
    echo "[ERROR] Artifact missing: ${svg}" >&2
    MISSING=$((MISSING + 1))
  fi
done

if [[ $MISSING -gt 0 ]]; then
  echo "Pipeline failed. Status: CRITICAL FAILURE ❌ (missing: $MISSING)" >&2
  exit 1
fi

echo "[INFO] OK: rendered ${#FILES[@]} diagrams into ${OUT_DIR}"
