# spec_study_t3 — final report (claude-haiku-4.5)

**Pre-registration:** Hypotheses H1–H4 were frozen in
`experiments/MAAT_SPEC_STUDY_T3.md` **before any live T3 trial**.

- **Rich baseline:** T2 Haiku JSONL, pipe+independent only — labeled **T2 (reused)**
- **Min grid:** 28/28 live trials under SPEC-MIN prompts
  (`experiments/runs/spec_study_t3/claude-haiku-4.5/min/trials.jsonl`)
- **Spend:** ~$0.93 (min live); rich costs from T2 reuse
- **Generated:** 2026-07-18

> **Rubric note:** Halted intervene chains score low on the final-file rubric
> by construction. Manifestation, propagation, catch|manifested, outcome_class,
> self-correction, and harm € are primary; mean rubric under intervene is secondary.

outcome_class order: `correct_published` / `incorrect_published` /
`justified_halt` / `collateral_defect_halt` / `unjustified_halt`

---

## 1. Rich vs min — topology × arm

| spec_level | source | topo | arm | n | manif (off) | prop% | catch\|manifested | outcome counts | self-corr | harm € sum | cost$ (mean) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rich | T2 (reused) | pipe | off | 7 | 3/6 (50%) | 50% | n/a | 4/3/0/0/0 | 3/6 | 1270.00 | 0.0369 |
| rich | T2 (reused) | pipe | intervene | 7 | — | 0% | 100% (5/5) | 2/0/5/0/0 | — | 0.00 | 0.0195 |
| rich | T2 (reused) | independent | off | 7 | 0/6 (0%) | 0% | n/a | 6/1/0/0/0 | 5/6 | 6930.00 | 0.0338 |
| rich | T2 (reused) | independent | intervene | 7 | — | 0% | 100% (3/3) | 4/0/3/0/0 | — | 0.00 | 0.0263 |
| min | T3 live | pipe | off | 7 | 0/6 (0%) | 0% | n/a | 7/0/0/0/0 | 6/6 | 0.00 | 0.0361 |
| min | T3 live | pipe | intervene | 7 | — | 0% | n/a (0 manifested) | 7/0/0/0/0 | — | 0.00 | 0.0359 |
| min | T3 live | independent | off | 7 | 1/6 (17%) | 0% | n/a | 6/1/0/0/0 | 5/6 | 769.99 | 0.0326 |
| min | T3 live | independent | intervene | 7 | — | 0% | 100% (2/2) | 5/0/2/0/0 | — | 0.00 | 0.0278 |

**Reading notes**

- **manif (off):** `defect_manifested_at_seam` among injected (6 per cell).
- **prop%:** `defect_reached_final` among injected.
- **self-corr:** off injected with honest published final (`correct_published`,
  `defect_reached_final=false`); injection wiring verified by static pre-checks.
- Min pipe intervene: **0 manifested** → catch|manifested is vacuous (`n/a`).
- Rich independent off harm (€6930) is dominated by one P5 seed1 trial that
  published payout `0` against seed-honest €6930 (not a P2 propagation event).

---

## 2. Clean controls and collateral (min)

| topo | arm | outcome_class | halt_gov | findings | rubric |
|---|---|---|---|---|---|
| pipe | off | correct_published | false | 0 | 6 |
| pipe | intervene | correct_published | false | 0 | 6 |
| independent | off | correct_published | false | 0 | 6 |
| independent | intervene | correct_published | false | 0 | 6 |

**All four min clean cells passed** (no governance halt, no findings, rubric 6).

**`collateral_defect_halt` under min:** **0** (no INFO_EMPTY / INFO_INSUFFICIENT
halts from stripped agents producing incomplete records in this grid).
`unjustified_halt`: **0**.

---

## 3. H1–H4 verdicts

Pre-registered text is in `experiments/MAAT_SPEC_STUDY_T3.md`. Verdicts below
use that document’s H1–H4 labels, with the empirical contrasts requested for
this report, and numbers from the table above.

- **H1 — NOT SUPPORTED.** Min does not exceed rich on ungoverned manifestation
  or harm: pipe manif 0/6 vs rich 3/6, harm €0 vs €1270; independent manif 1/6
  vs rich 0/6 but harm €770 vs €6930 (rich larger). Pre-registered form
  `T-IND_min > T-PIPE_min` prop also fails (both **0%**).
- **H2 — NOT SUPPORTED.** Independent self-correction does **not** disappear
  under min: **5/6** rich = **5/6** min (pipe self-corr rises 3/6 → 6/6).
  Pre-registered `Δprop_IND > Δprop_PIPE` also fails as an amplification claim
  (Δprop_PIPE = −50pp, Δprop_IND = 0pp; neither topology’s prop rises under min).
- **H3 — SUPPORTED (vacuous on min/pipe).** catch|manifested = **100%** wherever
  a defect manifested: rich pipe 5/5, rich ind 3/3, min ind 2/2; min pipe
  **0 manifested** → n/a. Governed harm € = **0** on all intervene cells.
- **H4 — NOT SUPPORTED.** Harm averted by governance
  (`off_harm − intervene_harm`) is **larger under rich**, not min:
  rich €1270+€6930=**€8200** averted vs min €0+€770=**€770**. Pre-registered
  self-corr collapse (`min < rich` per topo) also fails (pipe min 6/6 > rich 3/6;
  ind tied 5/6).

---

## 4. Cost

| grid | trials | total cost |
|---|---|---|
| min live (T3) | 28 | ~$0.93 |
| rich (T2 reused, pipe+ind) | 28 | (from T2; not re-spent) |

---

## Files

- Trials: `experiments/runs/spec_study_t3/claude-haiku-4.5/min/trials.jsonl`
- Analysis: `experiments/runs/spec_study_t3/claude-haiku-4.5/analysis/ANALYSIS.md`
- Pre-reg: `experiments/MAAT_SPEC_STUDY_T3.md`
