# Enterprise Discovery Grid — Summary

Trials in summary: **90** / 90
Skipped (existing): **55**
Failures logged: **0**
Total cost (new trials this run): **$3.0436**

Arms: v3_off (no v3), v3_warn (Gate 7 warn + amendments), v3_intervene (Gate 7 halt + amendments).
Scoring: 0–3 correctness (processes + dark processes + consistency).

## Per-arm overall

| arm | mean correctness | halt rate | mean cost ($) | n |
|-----|------------------|-----------|---------------|---|
| v3_off | 2.500 | 0.00 | 0.0868 | 30 |
| v3_warn | 3.000 | 0.00 | 0.0866 | 30 |
| v3_intervene | 3.000 | 0.17 | 0.0862 | 30 |

## Per-profile mean correctness (by arm)

| profile | v3_off | v3_warn | v3_intervene | Δ(warn−off) | Δ(intervene−off) |
|---------|--------|---------|--------------|-------------|------------------|
| baseline | 3.000 | 3.000 | 3.000 | +0.000 | +0.000 |
| missing_dark_process | 2.000 | 3.000 | 3.000 | +1.000 | +1.000 |
| cross_handoff_inconsistency | 3.000 | 3.000 | 3.000 | +0.000 | +0.000 |
| scope_amendment | 2.000 | 3.000 | 3.000 | +1.000 | +1.000 |
| revoked_authorization | 3.000 | 3.000 | 3.000 | +0.000 | +0.000 |
| conflicting_amendments | 2.000 | 3.000 | 3.000 | +1.000 | +1.000 |

## Notable findings

- v3_warn beats v3_off by 1.000 points on missing_dark_process
- v3_warn beats v3_off by 1.000 points on scope_amendment
