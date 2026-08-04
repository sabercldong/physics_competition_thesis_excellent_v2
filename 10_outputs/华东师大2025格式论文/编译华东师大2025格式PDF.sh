#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUTPUT_DIR="$ROOT/10_outputs/华东师大2025格式论文"
TEX_FILE="$OUTPUT_DIR/全国中学生物理竞赛复赛试题的科学思维要求与教学启示.tex"
BUILD_DIR="$OUTPUT_DIR/build"
COMPILER="/Users/dongxingxi/.codex/plugins/cache/openai-bundled/latex/0.2.4/scripts/compile_latex.py"

mkdir -p "$BUILD_DIR"
python3 "$OUTPUT_DIR/生成华东师大2025格式源文件.py"

TEXINPUTS="$ROOT//:" python3 "$COMPILER" \
  "$TEX_FILE" --compiler texlive --engine xelatex --output-directory "$BUILD_DIR"

TEXINPUTS="$ROOT//:" python3 "$COMPILER" \
  "$TEX_FILE" --compiler texlive --engine xelatex --output-directory "$BUILD_DIR"
