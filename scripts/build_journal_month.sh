#!/usr/bin/env bash
set -e

MONTH_DIR="docs/journal/2025/11"
OUT_FULL="docs/journal/2025-11.full.md"

cat "$MONTH_DIR"/*.md > "$OUT_FULL"
echo "Built $OUT_FULL"
