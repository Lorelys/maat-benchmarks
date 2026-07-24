# MAAT specification-ablation study T3 — pre-registered design

**Status:** hypotheses frozen before any live T3 trial.  
**Package:** `benchmarks/spec_study_t3`  
**Depends on:** topology_study_t2 (read-only code + committed Haiku JSONL as rich baseline)

## Design

Ablate agent **prompt richness** on the same topologies/arms/profiles as T2,
holding Maat gate / REQ / Gate 7 configuration **byte-identical**. Only
specialist system prompts change (`rich` = Benchmark 6 / T2 prompts;
`min` = SPEC-MIN Kim-style zero-shot + schema skeleton).

- Topologies: `pipe`, `independent` (no centralized in T3)
- Arms: `off`, `intervene`
- Profiles: P2, P5 × seeds 0–2 + one clean per topology×arm
- Model: `claude-haiku-4.5` only
- Live grid: `--spec-level min` only (28 trials); `rich` is never live-run
  (reuse T2 Haiku committed results)

## Pre-registered hypotheses (H1–H4)

Frozen before live min trials:

1. **H1 (ungoverned amplification under min):** On `spec_level=min`, ungoverned
   independent marker propagation is strictly greater than ungoverned pipe
   (`T-IND_min > T-PIPE_min`).
2. **H2 (spec × topology interaction):** The rich→min increase in ungoverned
   propagation is larger for independent than for pipe
   (`Δprop_IND > Δprop_PIPE`).
3. **H3 (governance closes the gap):** Under intervene, catch|manifested remains
   100% for both topologies at both spec levels when the defect manifests;
   governed harm € = 0 on both.
4. **H4 (self-correction collapses under min):** Off-arm self-correction count
   (corrupt present at seam, honest value published) is lower for `min` than
   for `rich` on the same topology.

## Non-goals

- Do not modify Benchmark 6 or topology_study_t2 sources/results.
- Do not change Maat contracts between arms.
- Do not live-run `--spec-level rich`.
