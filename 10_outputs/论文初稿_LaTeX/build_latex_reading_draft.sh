#!/usr/bin/env bash
# Generate the editable LaTeX reading draft and compile its A4 PDF.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUTPUT_DIR="$ROOT/10_outputs/论文初稿_LaTeX"
TEX_FILE="$OUTPUT_DIR/全国中学生物理竞赛复赛理论试题的科学思维要求及教学设计启示.tex"
BUILD_DIR="$OUTPUT_DIR/build"

mkdir -p "$BUILD_DIR"
python3 "$OUTPUT_DIR/prepare_latex_source.py"

TEXINPUTS="$ROOT//:" python3 \
  /Users/dongxingxi/.codex/plugins/cache/openai-bundled/latex/0.2.4/scripts/compile_latex.py \
  "$TEX_FILE" --compiler texlive --engine xelatex --output-directory "$BUILD_DIR"

TEXINPUTS="$ROOT//:" python3 \
  /Users/dongxingxi/.codex/plugins/cache/openai-bundled/latex/0.2.4/scripts/compile_latex.py \
  "$TEX_FILE" --compiler texlive --engine xelatex --output-directory "$BUILD_DIR"
