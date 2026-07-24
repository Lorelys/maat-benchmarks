#!/usr/bin/env bash
# Recompute ANALYSIS tables from banked JSONLs ($0, no LLM, no Maat engine).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
EXP="$(cd "$HERE/.." && pwd)"
export PYTHONPATH="$HERE${PYTHONPATH:+:$PYTHONPATH}"
cd "$EXP"

echo "=== T2 claude-haiku-4.5 ==="
python3 -m benchmarks.topology_study_t2.analyze \
  --model claude-haiku-4.5 --output-dir topology_study_t2/results

echo "=== T2 gpt-5-nano ==="
python3 -m benchmarks.topology_study_t2.analyze \
  --model gpt-5-nano --output-dir topology_study_t2/results

echo "=== T3 ==="
python3 -m benchmarks.spec_study_t3.analyze --output-dir spec_study_t3/results

echo "OK — regenerated ANALYSIS under topology_study_t2/results/ and spec_study_t3/results/"
echo "Note: gpt-5-nano ANALYSIS loses the hand-authored substitution note on regen;"
echo "      re-append from topology_study_t2/T2_REPORT.md provenance if needed."
