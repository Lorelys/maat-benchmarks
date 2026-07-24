# topology_study_t2 — gpt-5-nano analysis (final)

- Model: `gpt-5-nano`
- Trials: 42 (last record per trial_id)
- Source: `experiments/runs/topology_study_t2/gpt-5-nano/trials.jsonl`
- Generated: 2026-07-19

> **Companion metrics note:** `outcome_class` and `harm_published_eur` were defined before the Gemini grid was analyzed. They are computed identically for every model from existing JSONL only (no scorer / rubric changes).

> **Rubric note:** Halted intervene chains score low on the final-file rubric by construction. Propagation, catch|manifested, outcome_class, and harm € are the primary outcomes; mean rubric under intervene is secondary.

outcome_class order in counts: `correct_published` / `incorrect_published` / `justified_halt` / `collateral_defect_halt` / `unjustified_halt`

## Topology × arm summary

| topo | arm | n | prop% | rubric | catch% (raw) | catch\|manifested | outcome counts | harm € sum | harm € mean | cost$ | orch% | first_flagged_by | cleanFP | haltNoF | execF |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pipe | off | 7 | 33% | 5.14 | n/a | n/a | 5/2/0/0/0 | 1270.00 | 181.43 | 0.0070 | — | none:7 | 0/1 | 0 | 0 |
| pipe | intervene | 7 | 0% | 0.86 | 83% (5/6) | 100% (5/5) | 1/0/5/1/0 | 0.00 | 0.00 | 0.0032 | — | maat:6, none:1 | 0/1 | 0 | 0 |
| independent | off | 7 | 17% | 5.29 | n/a | n/a | 6/1/0/0/0 | 770.00 | 110.00 | 0.0071 | — | none:7 | 0/1 | 0 | 0 |
| independent | intervene | 7 | 0% | 1.71 | 67% (4/6) | 100% (4/4) | 2/0/4/1/0 | 0.00 | 0.00 | 0.0042 | — | maat:5, none:2 | 0/1 | 0 | 0 |
| centralized | off | 7 | 0% | 5.29 | n/a | n/a | 7/0/0/0/0 | 0.00 | 0.00 | 0.0147 | 41.1 | none:3, orchestrator:4 | 0/1 | 0 | 0 |
| centralized | intervene | 7 | 0% | 0.86 | 67% (4/6) | 100% (4/4) | 1/0/3/3/0 | 0.00 | 0.00 | 0.0061 | 24.9 | maat:3, orchestrator:4 | 0/1 | 0 | 0 |

### catch|manifested detail (intervene injected)

- **pipe:** caught/manifested = 5/5
  - no-defect-to-catch: payout_exceeds_coverage/seed1
- **independent:** caught/manifested = 4/4
  - no-defect-to-catch: payout_exceeds_coverage/seed1, payout_exceeds_coverage/seed2
- **centralized:** caught/manifested = 4/4
  - no-defect-to-catch: payout_exceeds_coverage/seed1, payout_exceeds_coverage/seed2

## Clean-control (intervene)

- **pipe:** PASS (zero governance findings) — outcome=`correct_published`, harm€=0.00, findings=[], rubric=6.0, cost=$0.005691
- **independent:** PASS (zero governance findings) — outcome=`correct_published`, harm€=0.00, findings=[], rubric=6.0, cost=$0.006021
- **centralized:** PASS (zero governance findings) — outcome=`correct_published`, harm€=0.00, findings=[], rubric=6.0, cost=$0.013579

## Outcome class + harm (definitions)

- **correct_published** — completed; no defect in final evidence (not `defect_reached_final`, payout equals honest expected when present, no drifted identity in evidence).
- **incorrect_published** — completed with defect in final evidence (`defect_reached_final`, drifted identity, or published payout ≠ honest).
- **justified_halt** — governance halt with a defect-indicating finding (`REQ_VALUE_MISMATCH`, `ENTITY_REFERENCE_DRIFT`, …) showing the *injected* defect was present at/upstream of the halted seam.
- **collateral_defect_halt** — governance halt on a genuine agent output defect (empty/missing required fields: `INFO_EMPTY`, `INFO_INSUFFICIENT`) unrelated to the injected profile.
- **unjustified_halt** — halt with no defect of any kind present (true false positive).
- **harm_published_eur** — `|published approved_payout_eur − honest expected|` when a final file was published; `0` if equal or if halted.


## Rerun substitution note

Four pre-fix pipe×off cells were re-executed under the enriched slim recorder. On re-execution the 3 P5 cells changed manifestation (originally 2/3 `PH_2026_999`; substituted 0/3). Manifestation rates in this ANALYSIS reflect substituted records. Original pre-fix lines: git `ebbc8a32c1af17effdeae9139d4a83f10a184b52`.
