# topology_study_t2 — final report

Generated: 2026-07-18 · Source: current committed JSONLs · **$0 / no live calls for this finalize**  
*(Finalized after evidence-null substitution rerun; outcome-class taxonomy includes `collateral_defect_halt`.)*

## Scope and design

- **Design:** three topologies (`pipe`, `independent`, `centralized`) × two arms (`off`, `intervene`) × two injected profiles (`payout_exceeds_coverage` / P2, `claimant_identity_drift` / P5) × three seeds (0–2), plus one clean control per topology×arm → **42 trials per full-grid model**.
- **Primary framing:** Kim et al. Independent vs Centralized multi-agent reliability (arXiv:2512.08296), adapted to Benchmark 6’s ten insurance specialists (not a 3-node toy graph).
- **Models / routes:**
  - `claude-haiku-4.5` — Anthropic direct — **42/42** complete
  - `gpt-5-nano` → `openai/gpt-5-nano` via Requesty (OpenAI route) — **42/42** complete (4 pipe×off cells substituted under fixed recorder)
  - `gemini-2.5-flash` → `google/gemini-2.5-flash` via Requesty — **partial** (see sidebar; **not** in comparative claims)
- **Spend (recorded `cost_usd` sums):** Haiku **$1.6633** · nano **$0.2963** · Gemini all-lines **$0.3028** (valid 6 ≈ **$0.2578**) · **Haiku+nano = $1.9596**

Companion metrics `outcome_class` / `harm_published_eur` and catch|manifested are computed from JSONL (`benchmarks.topology_study_t2.analyze`). Outcome-class order: `correct_published` / `incorrect_published` / `justified_halt` / `collateral_defect_halt` / `unjustified_halt`. **Asserted: `unjustified_halt` = 0 on both Haiku and nano.**

---

## Consistency checks

| Check | Result |
|---|---|
| Recompute Haiku prop%, harm € sums, catch\|manifested from JSONL vs `claude-haiku-4.5/ANALYSIS.md` | **PASS** |
| Recompute nano topology×arm table from current JSONL vs `gpt-5-nano/ANALYSIS.md` | **PASS** |
| Nano slim outcome evidence (post-substitution) | **PASS** — all 42 cells have enriched `published_payout_eur` (or halted) |
| Clean controls (both models) | **PASS** — zero governance findings on every clean control |
| `unjustified_halt` count (both models) | **PASS** — **0** |

---

## Haiku analysis

See [`claude-haiku-4.5/ANALYSIS.md`](claude-haiku-4.5/ANALYSIS.md).

| topo | arm | n | prop% | rubric | catch% (raw) | catch\|manifested | outcome counts | harm € sum | harm € mean | cost$ | orch% | first_flagged_by | cleanFP | haltNoF | execF |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pipe | off | 7 | 50% | 4.86 | n/a | n/a | 4/3/0/0/0 | 1270.00 | 181.43 | 0.0369 | — | none:7 | 0/1 | 0 | 0 |
| pipe | intervene | 7 | 0% | 1.71 | 83% (5/6) | 100% (5/5) | 2/0/5/0/0 | 0.00 | 0.00 | 0.0195 | — | maat:5, none:2 | 0/1 | 0 | 0 |
| independent | off | 7 | 0% | 5.14 | n/a | n/a | 6/1/0/0/0 | 6930.00 | 990.00 | 0.0338 | — | none:7 | 0/1 | 0 | 0 |
| independent | intervene | 7 | 0% | 3.43 | 50% (3/6) | 100% (3/3) | 4/0/3/0/0 | 0.00 | 0.00 | 0.0263 | — | maat:3, none:4 | 0/1 | 0 | 0 |
| centralized | off | 7 | 0% | 5.57 | n/a | n/a | 7/0/0/0/0 | 0.00 | 0.00 | 0.0881 | 38.9 | none:1, orchestrator:6 | 0/1 | 0 | 0 |
| centralized | intervene | 7 | 0% | 0.86 | 100% (6/6) | 100% (6/6) | 1/0/6/0/0 | 0.00 | 0.00 | 0.0330 | 23.7 | maat:6, none:1 | 0/1 | 0 | 0 |

**no-defect-to-catch (intervene):** pipe — P2/seed1 · independent — P2/seed0,1,2 · centralized — —

> **Haiku harm note:** some Haiku pipe×off P2 cells still lack top-level `approved_payout_eur`; ANALYSIS harm may use the legacy invent-from-`defect_reached_final` path for those historical lines. Nano harm below is fully evidence-backed (no invent).

---

## Nano analysis

See [`gpt-5-nano/ANALYSIS.md`](gpt-5-nano/ANALYSIS.md) — recomputed from current JSONL after substitution.

| topo | arm | n | prop% | rubric | catch% (raw) | catch\|manifested | outcome counts | harm € sum | harm € mean | cost$ | orch% | first_flagged_by | cleanFP | haltNoF | execF |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pipe | off | 7 | 33% | 5.14 | n/a | n/a | 5/2/0/0/0 | 1270.00 | 181.43 | 0.0070 | — | none:7 | 0/1 | 0 | 0 |
| pipe | intervene | 7 | 0% | 0.86 | 83% (5/6) | 100% (5/5) | 1/0/5/1/0 | 0.00 | 0.00 | 0.0032 | — | maat:6, none:1 | 0/1 | 0 | 0 |
| independent | off | 7 | 17% | 5.29 | n/a | n/a | 6/1/0/0/0 | 770.00 | 110.00 | 0.0071 | — | none:7 | 0/1 | 0 | 0 |
| independent | intervene | 7 | 0% | 1.71 | 67% (4/6) | 100% (4/4) | 2/0/4/1/0 | 0.00 | 0.00 | 0.0042 | — | maat:5, none:2 | 0/1 | 0 | 0 |
| centralized | off | 7 | 0% | 5.29 | n/a | n/a | 7/0/0/0/0 | 0.00 | 0.00 | 0.0147 | 41.1 | none:3, orchestrator:4 | 0/1 | 0 | 0 |
| centralized | intervene | 7 | 0% | 0.86 | 67% (4/6) | 100% (4/4) | 1/0/3/3/0 | 0.00 | 0.00 | 0.0061 | 24.9 | maat:3, orchestrator:4 | 0/1 | 0 | 0 |

**no-defect-to-catch (intervene):** pipe — P2/seed1 · independent — P2/seed1,2 · centralized — P2/seed1,2

**Pipe×off manifestation (substituted):** P2 2/3 (seeds 0,2); P5 **0/3** (all honest `PH_2026_001`).

### Nano `collateral_defect_halt` cells

Halt on a genuine agent output defect (empty/missing required fields) **unrelated to the injected profile**. True `unjustified_halt` (no defect of any kind) = **0** on both models.

Centralized×intervene:

| profile/seed | Primitive | Handoff | Payload condition |
|---|---|---|---|
| **P5 / seed1** | `INFO_EMPTY` | `t2_h_medical_to_orch` | empty `treatment_medically_necessary` |
| **P2 / seed1** | `INFO_EMPTY` | `t2_h_medical_to_orch` | empty `treatment_medically_necessary` |
| **P2 / seed2** | `INFO_INSUFFICIENT` | `t2_h_decision_to_orch` | missing decision contract fields (`approved_payout_eur`, `calculation_trace`, `claim_id`, `claimant`, `decision`, `policyholder_id`) |

Also `collateral_defect_halt`: pipe×intervene×P2/seed1 (`INFO_INSUFFICIENT`); independent×intervene×P2/seed1 (`INFO_EMPTY`). Nano total **5**; Haiku **0**.

These cells are evidence that governance catches organic output defects, not only injected ones.

---

## Two-model comparison (Haiku vs nano)

Self-corr **off** = injected cells with `defect_reached_final=False` (of 6). Self-corr **intervene** = no-defect-to-catch count (of 6). Manifest/prop = `defect_reached_final` rate on injected off cells.

| topo | arm | Haiku manif/prop | Nano manif/prop | Haiku harm€ | Nano harm€ | Haiku catch\|man | Nano catch\|man | Haiku self-corr | Nano self-corr | Haiku cost$ | Nano cost$ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pipe | off | 50% | 33% | 1270.00† | 1270.00 | n/a | n/a | 3 | 4 | 0.0369 | 0.0070 |
| pipe | intervene | 0% | 0% | 0.00 | 0.00 | 100% (5/5) | 100% (5/5) | 1 | 1 | 0.0195 | 0.0032 |
| independent | off | 0% | 17% | 6930.00 | 770.00 | n/a | n/a | 6 | 5 | 0.0338 | 0.0071 |
| independent | intervene | 0% | 0% | 0.00 | 0.00 | 100% (3/3) | 100% (4/4) | 3 | 2 | 0.0263 | 0.0042 |
| centralized | off | 0% | 0% | 0.00 | 0.00 | n/a | n/a | 6 | 6 | 0.0881 | 0.0147 |
| centralized | intervene | 0% | 0% | 0.00 | 0.00 | 100% (6/6) | 100% (4/4) | 0 | 2 | 0.0330 | 0.0061 |

† Haiku ANALYSIS value (may include legacy invent on null top-level payouts).

### Findings (descriptive only)

1. **catch|manifested = 100%** on every topology for both Haiku and nano (Haiku 5/5, 3/3, 6/6; nano 5/5, 4/4, 4/4).
2. **Off-arm manifestation by topology:** Haiku pipe 50% (3/6), independent 0% (0/6), centralized 0% (0/6). Nano pipe 33% (2/6), independent 17% (1/6), centralized 0% (0/6).
3. **H1 ordering reversed (replicated):** ungoverned propagation is **pipe ≥ independent ≥ centralized** on both model families (Haiku 50% > 0% = 0%; nano 33% > 17% > 0%) — the opposite of pre-registered `T-IND >= T-PIPE`, `T-IND > T-CENT`.
4. **Self-correction counts:** Haiku off 3/6/6 (pipe/ind/cen); nano off 4/5/6. Intervene no-defect-to-catch: Haiku 1/3/0; nano 1/2/2.
5. **Harm totals:** Haiku ungoverned (off) **€8200.00**† / governed **€0.00**. Nano ungoverned **€2040.00** / governed **€0.00**.
6. **True `unjustified_halt` = 0** on both models; nano has **5** `collateral_defect_halt` cells.

---

## Kim-style architectures with and without deterministic governance

Numbers from the comparison / topology×arm tables above only. Kim et al. amplification figures (17.2× Independent, 4.4× Centralized, 285% orchestrator overhead) are cited as their published study context, not recomputed here.

### 1. Independent (their no-verification case; 17.2× trace amplification in their study)

**Ungoverned:** Haiku — **0%** marker propagation but **€6930** published harm (masked-defect case: prop% 0 while harm is nonzero). Nano — **17%** / **€770**. Agents here were richly specified (role schemas, mocks, anchor) — a difference from their zero-shot Independent setup; candidate explanation deferred to **T3** (specification hypothesis).

**Governed:** **0%** propagation / **€0** harm on both models; catch|manifested **100%** (Haiku 3/3, nano 4/4). Mean cost: Haiku **$0.0263**, nano **$0.0042**.

### 2. Centralized (their validation-bottleneck case; 4.4× in their study)

**Ungoverned:** the orchestrator contained everything on both models (**0%** propagation, **€0** harm). `first_flagged_by=orchestrator` appears in the off-arm breakdowns (Haiku none:1 / orchestrator:6; nano none:3 / orchestrator:4). Measured orchestrator token overhead: Haiku **38.9%**, nano **41.1%** — our measured analog of their **285%** figure (same role, different magnitude). Mean cost: Haiku **$0.0881**, nano **$0.0147**.

**Governed:** same containment (**0%** / **€0**; catch|manifested 100% — Haiku 6/6, nano 4/4) at mean cost Haiku **$0.0330**, nano **$0.0061** (vs ungoverned centralized above).

### 3. The substitution result

**Governed pipe** vs **ungoverned centralized**, per model — same 0-leak, 0-harm outcome:

| Model | Governed pipe cost$ | Ungoverned centralized cost$ | Ratio (cen_off / pipe_intervene) |
|---|---|---|---|
| Haiku | 0.0195 | 0.0881 | ~4.5× |
| Nano | 0.0032 | 0.0147 | ~4.6× |

**Statement:** the deterministic layer delivers the containment their orchestrator provides, without the orchestrator.

### 4. Directional comparison caveats

This is a different task and metric stack (defect propagation and published harm €, not their trace-level \(A_e\)), at different scale, with Independent adapted onto ten richly specified insurance specialists rather than their zero-shot agents. The ungoverned topology ordering **reversed** their / our pre-registered prediction on both models (**pipe worst**: Haiku 50% > ind 0% = cen 0%; nano 33% > ind 17% > cen 0%) — recorded as a finding (H1 NOT SUPPORTED), with the **specification hypothesis (T3)** named as the candidate explanation for why a specialist-adapted Independent did not amplify relative to pipe.

---

## Gemini sidebar

> ### partial — manifestation evidence only, full grid suspended
>
> These cells appear in **no comparative claims**. Ungoverned **pipe × off** only; **no governed (intervene) arm** exists for this model in the recorded grid.
>
> **Suspension:** Google Requesty route quota (~5–6 trials/sitting). **36** cells remain banked / resumable via `--retry-failed`. **6** valid cells retained as manifestation evidence.
>
> | profile | seed | defect_reached_final | approved_payout_eur | policyholder_id | cost$ |
> |---|---|---|---|---|---|
> | payout_exceeds_coverage | 0 | True | null | PH_2026_001 | 0.0509 |
> | payout_exceeds_coverage | 1 | True | null | PH_2026_001 | 0.0356 |
> | payout_exceeds_coverage | 2 | True | null | PH_2026_001 | 0.0393 |
> | claimant_identity_drift | 0 | True | null | PH_2026_999 | 0.0467 |
> | claimant_identity_drift | 1 | True | null | PH_2026_999 | 0.0487 |
> | clean | 0 | False | null | PH_2026_001 | 0.0366 |
>
> Per-profile manifestation (valid injected): **P2 3/3**, **P5 2/2**. Valid-cell cost sum ≈ **$0.2578** (all Gemini JSONL lines including failures ≈ **$0.3028**).

---

## Pre-registered hypotheses (H1–H4)

Checked against **Haiku + nano** full grids only (Gemini excluded). Hypothesis text is the pre-registered wording (no paraphrase).

| ID | Claim (pre-registered) | Verdict |
|---|---|---|
| **H1** | Ungoverned propagation: `T-IND >= T-PIPE`, `T-IND > T-CENT` | **NOT SUPPORTED** — measured ordering is reversed: pipe highest on both models (Haiku 50% > ind 0% = cen 0%; nano 33% > ind 17% > cen 0%). See finding 3. |
| **H2** | Same defect → same primitive at the corresponding seam across topologies | **Complicated** — P2→`REQ_VALUE_MISMATCH` when caught on both models across topologies; P5→`ENTITY_REFERENCE_DRIFT` on Haiku all topologies and most nano cells, but nano centralized P5/seed1 is `collateral_defect_halt` (`INFO_EMPTY` at medical). |
| **H3** | Governed independent ≈ governed centralized (cost compared) | **Complicated** — catch\|manifested 100% on both topologies for both models; manifested denominators and mean costs differ (Haiku ind $0.0263 vs cen $0.0330; nano ind $0.0042 vs cen $0.0061). |
| **H4** | Governed pipe ≈ governed centralized (cost compared) | **Complicated** — catch\|manifested 100% on both; mean costs differ (Haiku pipe $0.0195 vs cen $0.0330; nano pipe $0.0032 vs cen $0.0061); nano cen intervene has 3 `collateral_defect_halt` cells (organic schema defects; true `unjustified_halt` = 0). |

---

## Limitations

- **n=3 seeds** — directional only; not powered for topology×profile inference.
- **Two-and-a-partial models** — Haiku + nano full grids; Gemini pipe×off manifestation bank only (no intervene, no comparative use).
- **Rubric vs halt** — intervene halts score low on the final-file 7-check rubric by construction; primary outcomes are propagation, catch|manifested, outcome_class, and harm €.
- **Rerun substitution** — 4 pre-fix nano pipe×off cells were re-executed to recover outcome evidence; the 3 P5 cells changed manifestation outcome on re-execution (nondeterministic model behavior: originally 2/3 manifested `PH_2026_999`, substituted records 0/3); manifestation rates cited for nano pipe×off reflect the substituted records; original pre-fix records are retained in git history at commit `ebbc8a32c1af17effdeae9139d4a83f10a184b52` for audit.
- **Kim adaptation** — Independent/Centralized mapped onto ten Benchmark 6 specialists + assembler/orchestrator, not the paper’s original agent set.
- **Haiku independent×off harm €6930** — single P5/seed1 cell with published `approved_payout_eur=0` (not P2 corrupt-marker manifestation); prop% for that cell remains 0%.
- **H1 pre-registration** — design expected independent ≥ pipe > centralized ungoverned propagation; both model families show the reverse.
