# Specification study T3 (results + prompts)

Prompt-richness ablation (`rich` = T2 reused vs `min` = SPEC-MIN) on pipe +
independent. Pre-registration: [`MAAT_SPEC_STUDY_T3.md`](MAAT_SPEC_STUDY_T3.md).
Report: [`T3_REPORT.md`](T3_REPORT.md).

## Prompts

- `prompts/min.py` — SPEC-MIN (Kim-style zero-shot + schema skeleton)
- `prompts/STRIP_MAP.md` — what was removed vs rich
- `prompts/rich.py` — pointer to vendored rich `SYSTEM_PROMPTS` in analysis fixtures

## Results

`results/claude-haiku-4.5/min/trials.jsonl` (28) + `analysis/ANALYSIS.*`

Recompute: see [`../code/README.md`](../code/README.md).
