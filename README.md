# Maat Benchmarks — Results & Methodology

Measured results and methodology for **Maat**, a deterministic governance layer that validates handoffs between agents in multi-agent AI workflows. This repository publishes the **benchmark designs, methodology, and complete measured results** referenced in the Maat whitepaper.

These are the benchmarks behind the claim that a deterministic layer catches inter-agent handoff failures — the failure class UC Berkeley's [MAST study](https://github.com/multi-agent-systems-failure-taxonomy/MAST) measured as ~37% of all multi-agent failures — before they propagate.

**Anchoring references:** [MAST taxonomy](https://github.com/multi-agent-systems-failure-taxonomy/MAST) (Cemri et al., 2025) · [Karpathy's "March of Nines"](https://venturebeat.com/technology/karpathys-march-of-nines-shows-why-90-ai-reliability-isnt-even-close-to) on compounding reliability.

---

## What's here

**Complete measured results** for six controlled multi-agent workflow benchmarks, plus the methodology and per-gate analysis behind them.

| Benchmark | Agents | Trials | Domain |
|-----------|--------|--------|--------|
| B2B financial | 6 | 75 | Lead-to-invoice financial workflow |
| Hospital triage | 10 | 75 | Clinical intake-to-disposition |
| Software dev team | 12 | 75 | Software spec-to-release |
| Enterprise discovery | 12 | 90 | Process discovery + mid-flight amendments |
| E-commerce agency | 15 | 135 | Multi-marketplace, two concurrent clients |
| Health insurance claims | 10 | 72 | EU health-insurance claims adjudication |

- **`results/`** — per-benchmark summaries, gate reports, and the consolidated cross-benchmark table (`WORKSTREAM_B_CONSOLIDATED.md`). Every number, every arm, every profile.
- **`benchmarks/*/`** — per-benchmark result summaries and prose design descriptions.
- **`kim-comparison/`** — standalone follow-on studies on the insurance fleet: topology ablation (T2: pipe / independent / centralized) and prompt-specification ablation (T3: rich vs SPEC-MIN), framed against Kim et al. ([arXiv:2512.08296](https://arxiv.org/abs/2512.08296)). Reports, JSONLs, figures, and analysis-only verify code. See `kim-comparison/README.md`.

---

## What each benchmark measures

Each benchmark runs a multi-agent workflow three ways — **Maat off**, **Maat on (warn)**, and **Maat on (intervene/halt)** — injects a realistic defect at an agent handoff, and measures whether Maat catches it. The only difference between arms is Maat.

- **Deterministic scoring, no LLM in the scoring path.** Every benchmark scores on a rubric of business-meaningful pass/fail checks against the workflow contract. Scores are reproducible byte-for-byte.
- **Data-level defect injection.** Failure profiles corrupt the data an agent treats as authoritative — closer to how real pipelines fail than prompt-level nudges, which modern models often ignore.
- **Honest reporting.** Where a defect didn't manifest because the model self-corrected, where a gate wasn't exercised, or where a catch happened for a structural rather than semantic reason — the results say so.

See `results/WORKSTREAM_B_CONSOLIDATED.md` for the full cross-benchmark detail. Headline results below.

---

## Results at a glance

Across six controlled benchmarks and 500+ trials, on a unified deterministic 7-check rubric (0–7) with **no language model in the validation path or the scoring path**, Maat improved output correctness on **every benchmark** — and cut cost where it halted defective chains early.

| Benchmark | Agents | Maat off | Maat on | Δ | Cost off | Cost on | Cost change |
|-----------|--------|----------|---------|-----|----------|---------|-------------|
| B2B financial | 6 | 5.28 | 6.68 | **+26.5%** | $0.0088 | $0.0044 | **−50%** |
| Hospital triage | 10 | 6.12 | 6.88 | **+12.4%** | $0.0249 | $0.0127 | **−49%** |
| Software dev team | 12 | 6.24 | 6.48 | +3.8% | $0.0568 | $0.0522 | −8% |
| Enterprise discovery | 12 | 6.50 | 7.00 | **+7.7%** | $0.0868 | $0.0862 | ~neutral |
| E-commerce agency | 15 | 6.22 | 6.89 | **+10.7%** | $0.2090 | $0.1740 | **−17%** |
| Health insurance | 10 | 5.667 | 5.833 | +2.9% | $0.0412 | $0.0185 | **−55%** |

*Direction positive on every benchmark. On the insurance grid, 11 documented false positives remain — all `REQ_VALUE_MISMATCH` or `INFO_EMPTY` on two profiles (excluded treatment, fraud) where the model correctly denies the claim while the anchor’s expected payout still reflects the clean-claim value: an anchor-configuration boundary, reported in `results/` rather than tuned away.*

### Specific defects caught

Each benchmark injects a realistic defect and measures whether Maat catches it. Clean catches include:

- **VAT/tax misclassification** — caught on **100%** of trials where it occurred (e-commerce and insurance). The error that triggers tax audits and retroactive liability.
- **A revenue-reporting defect nobody injected** — the e-commerce analytics agent systematically mis-reported revenue on its own; Maat detected this genuine, un-planted error in **100%** of the cases its validation reached.
- **Payout overpayment** — an inflated billed amount produced a €1,310 payout against a contract-correct €810 (a 61.7% overpayment); Maat compared it to the policy and halted before it reached the final report (insurance).
- **Cross-marketplace price drift** — the same product priced 40% apart across three marketplaces (Amazon/eBay/Temu), detected and halted (e-commerce).
- **Claimant identity drift** — a wrong policyholder ID propagating downstream, halted before a wrong-party payout and a GDPR breach (insurance).
- **GDPR data-residency violation** — non-EU routing of special-category medical data, caught 100% of seeds (insurance).
- **Contract scope creep and fabricated discounts** — blocked at the handoff, with ~58% cost savings on early halts (B2B, e-commerce).

### The cost story

On the workflows where Maat halted defective chains early, it cut wasted compute by up to **50%** — it stops a bad chain before the remaining agents burn tokens on poisoned data. Maat's own per-handoff cost is negligible: the gates are deterministic code, microseconds per check, no model call.

### Reported honestly

- The **software-dev** benchmark shows the smallest lift (+3.8%): a code-release pipeline re-derives its own artifacts, so a single dropped field is often caught downstream anyway. We report this because it shows exactly where Maat earns its keep and where it may not.
- Several injected defects **did not manifest** because the tested model self-corrected — a governance layer cannot catch a defect the agents decline to make. We treat these as model-dependent, not universal, and propose them as pilot experiments.
- Full per-profile detail, including every non-manifesting profile and every false-positive check, is in `results/`.

---

## What's not here

This repository publishes the **designs and results**. It does not include the runnable benchmark harness or the Maat conductor engine — those are the core intellectual property and are available for evaluation. The `kim-comparison/` package includes **analysis-only** code (`code/verify.sh`) to regenerate tables from banked JSONLs; it still does not ship the full harness or conductor.

If you want to inspect the full harness, reproduce the results end-to-end, or evaluate Maat on your own workflows, **contact the Maat team** (see the whitepaper for details). We're glad to give serious evaluators a running instance and the harness under evaluation terms.

---

## Reading the results

Start with `results/WORKSTREAM_B_CONSOLIDATED.md` for the cross-benchmark table, then drill into any benchmark's `RESULTS_SUMMARY.md` for per-profile detail and its `gate_report.md` (where present) for which gate caught what. The insurance and e-commerce benchmarks include the most detailed gate-level breakdowns. For the Kim-comparison topology and specification studies, start at `kim-comparison/README.md`.

---

*Maat is developed by SynWe Group s.r.o. Intellectual property, including the SynWe methodology and the Maat conductor, belongs to Uliana Elina. Benchmark designs and results in this repository are provided for inspection and evaluation. The runnable harness and conductor engine are available under evaluation terms. © 2026 SynWe Group s.r.o.*
