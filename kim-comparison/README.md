# Kim-comparison studies (topology + specification)

Standalone experiment package for publication in
[maat-benchmarks](https://github.com/Lorelys/maat-benchmarks).

Multi-agent reliability under **topology** and **prompt specification**
ablations, framed against Kim et al., *Independent vs Centralized*
multi-agent systems ([arXiv:2512.08296](https://arxiv.org/abs/2512.08296)),
adapted to Benchmark 6’s ten EU health-insurance claim specialists (not a
3-node toy graph).

**Scope line:** all failure profiles are **data-level corruptions** in
**verification-rich** workflows by design (P2 billed-amount inflation; P5
claimant-identity drift). Maat gate/REQ/Gate7 contracts are held fixed
within each study; T2 varies graph structure, T3 varies specialist prompt
richness only.

**Data license:** Benchmark designs and banked results in this package are
© 2026 SynWe Group s.r.o. / Uliana Elina, provided for inspection and
evaluation. Redistribution or commercial use requires permission.
Analysis-only verify code is included under the same terms. The Maat
conductor and full harness remain available under separate evaluation
license.

---

## What was tested

### T2 — topology (`topology_study_t2/`)

| Dimension | Values |
|---|---|
| Topologies | `pipe`, `independent`, `centralized` |
| Arms | `off` (ungoverned), `intervene` (Maat halt) |
| Profiles | P2 `payout_exceeds_coverage`, P5 `claimant_identity_drift` |
| Seeds | 0–2 + one clean per topology×arm |
| Matrix | **42 trials / full-grid model** |

### T3 — specification (`spec_study_t3/`)

| Dimension | Values |
|---|---|
| Spec levels | `rich` = T2/Benchmark 6 prompts (**T2 Haiku reused**, never live in T3); `min` = SPEC-MIN zero-shot + schema skeleton |
| Topologies | `pipe`, `independent` |
| Arms / profiles | same as T2 (P2, P5 × seeds + clean) |
| Live matrix | **28 trials** (`min` only) |
| Pre-registration | `spec_study_t3/MAAT_SPEC_STUDY_T3.md` (H1–H4 frozen before live) |

---

## Models (pinned IDs) and spend

| CLI / slug | api_model (pinned) | Route | Grid | Spend (`cost_usd` Σ) |
|---|---|---|---|---|
| `claude-haiku-4.5` | `claude-haiku-4-5-20251001` | Anthropic direct | T2 **42/42**; T3 min **28/28** | T2 $1.6633 · T3 min ~$0.93 |
| `gpt-5-nano` | `openai/gpt-5-nano` | Requesty (OpenAI) | T2 **42/42** (4 cells substituted) | $0.2963 |
| `gemini-2.5-flash` | `google/gemini-2.5-flash` | Requesty (Google) | T2 **6 valid** banked; **36** failed/resumable; **full grid SUSPENDED** | $0.3028 all-lines (~$0.26 valid) |

Comparative claims use **Haiku + nano** only (≈ **$1.96** combined). Gemini is
manifestation evidence / resume bank only — **not** in comparative tables.
T3 rich rows are labeled **T2 (reused)** (no second Haiku spend).

---

## Headline results

### T2 — catch|manifested (intervene) and ungoverned harm (off)

| topo | Haiku prop% (off) | Nano prop% (off) | Haiku harm€ (off) | Nano harm€ (off) | Haiku catch\|man | Nano catch\|man |
|---|---|---|---|---|---|---|
| pipe | 50% | 33% | 1270 | 1270 | 100% (5/5) | 100% (5/5) |
| independent | 0% | 17% | 6930 | 770 | 100% (3/3) | 100% (4/4) |
| centralized | 0% | 0% | 0 | 0 | 100% (6/6) | 100% (4/4) |

- **`unjustified_halt` = 0** on Haiku and nano; nano has **5** `collateral_defect_halt` (organic INFO_* schema defects).
- Pre-registered H1 (Independent ≥ Pipe propagation) was **not supported** on these models (pipe highest on both).
- Full tables: `topology_study_t2/T2_REPORT.md`.

### T3 — rich (T2 reused) vs SPEC-MIN (Haiku)

| topo / arm | rich manif (off) | min manif (off) | rich harm€ (off) | min harm€ (off) | rich catch\|man | min catch\|man |
|---|---|---|---|---|---|---|
| pipe / off | 3/6 (50%) | 0/6 (0%) | 1270 | 0 | — | — |
| independent / off | 0/6 (0%) | 1/6 (17%) | 6930 | 770 | — | — |
| pipe / intervene | — | — | 0 | 0 | 100% (5/5) | n/a (0 manifested) |
| independent / intervene | — | — | 0 | 0 | 100% (3/3) | 100% (2/2) |

- H1/H2/H4 **not supported**; H3 **supported** where a defect manifested (vacuous on min/pipe).
- Full verdicts: `spec_study_t3/T3_REPORT.md`.

---

## How to verify ($0)

```bash
cd kim-comparison
chmod +x code/verify.sh
./code/verify.sh
```

Requires Python 3.10+ (stdlib only). Regenerates ANALYSIS files from JSONLs.
No API keys, no network, no Maat engine.

Live re-execution of trials requires the Maat engine (available under license)
and is **out of scope** for this package. Runner / conductor / gate code is
intentionally omitted.

---

## Provenance

| Event | Detail |
|---|---|
| Nano 4-cell recorder substitution | Four pre-fix `pipe×off` cells re-run under enriched slim recorder. P5 manifestation changed (originally 2/3 drifted → substituted 0/3). Analysis cites substituted records. **Original pre-fix lines:** git `ebbc8a32c1af17effdeae9139d4a83f10a184b52` (maat-api). |
| Gemini quota suspension | Google Requesty ~5–6 trials/sitting; full grid suspended; 6 valid `pipe×off` cells + 36 `halt_execution` records banked for resume. |
| T2 config / evidence retention | Slim JSONL `published_payout_eur` / `rubric_sources`; outcome taxonomy adds `collateral_defect_halt` vs `unjustified_halt`. |
| T3 SPEC-MIN freeze | Prompt set + `STRIP_MAP.md` frozen before live; rich never live-run in T3. |

---

## Figures

| File | Format |
|---|---|
| `topology_study_t2/figures/t2_harm_figure.png` | PNG (+ `.pdf`) |
| `topology_study_t2/figures/t2_substitution_figure.png` | PNG (+ `.pdf`) |

Sourced from local Downloads at package time (not previously in maat-api git).

---

## Limitations

- Nondeterminism: nano substitution changed P5 manifestation; rates are
  post-substitution.
- Gemini incomplete — do not use in model comparisons.
- Haiku legacy JSONL lines may lack enriched payout keys; ANALYSIS may use
  documented fallbacks (see T2 report).
- T3 min grid is a single model (Haiku); cross-model spec ablation not run.
- Governance results assume Maat intervene semantics as recorded in JSONL
  findings; engine source is not redistributed here.

---

## Layout

```
kim-comparison/
  README.md                 ← this file
  topology_study_t2/
    T2_REPORT.md
    results/<model>/trials.jsonl [+ ANALYSIS.md]
  spec_study_t3/
    MAAT_SPEC_STUDY_T3.md
    T3_REPORT.md
    prompts/{min.py,STRIP_MAP.md,rich.py}
    results/claude-haiku-4.5/{min/trials.jsonl,analysis/}
  code/                     ← analysis-only Python (see code/README.md)
```

Copy this directory to `maat-benchmarks` (e.g. on branch `kim-comparison-study`).
A partial tree may already exist under a local `maat-benchmarks-public` clone —
prefer replacing it with this export after review.
