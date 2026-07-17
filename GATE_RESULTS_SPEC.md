# Maat — Gate Results Specification

## Per-Gate Behavior and Evidence Across Six Controlled Benchmarks

**Companion document to the Maat whitepaper · Draft · July 2026**
**SynWe Group s.r.o. · IP: Uliana Elina**

---

## Purpose

This document is the auditable, gate-by-gate record of what each Maat gate did across every benchmark. It exists so a technical evaluator can see — per gate, per benchmark — whether the gate fired, on what defect, with what result, and where it was *not* exercised. It is deliberately honest about silence: a gate that stayed quiet because a benchmark did not stress it is recorded as "not exercised," not implied to be validated.

**Scoring throughout:** deterministic, no LLM in the scoring path. Benchmarks 1–5 use a unified 7-check rubric (0–7); benchmark 6 uses a 7-check insurance rubric (0–7). All arms: `v3_off` (Maat off), `v3_warn` (findings logged, chain continues), `v3_intervene` (chain halts on blocker).

---

## The seven gates (reference)

| Gate | Name | What it validates | Type |
|------|------|-------------------|------|
| 1 | Plan validation | Workflow plan is coherent before execution (no missing deps, cycles, orphans) | Structural |
| 2 | Handoff validation | Payload carries required fields; internally consistent; contract-valid | Content |
| 3 | Validation depth control | How strictly to validate, scaled to handoff criticality | Control |
| 4 | Integrity / role adherence | Each agent stays within its declared role | Behavioral |
| 5 | Survival / health monitoring | Agent looping, drift, resource exhaustion | Behavioral |
| 6 | Circuit breaker | Agents with elevated failure rates are paused | Behavioral |
| 7 | Cross-handoff entity consistency | A tracked entity stays consistent everywhere it appears | Content |

On top of the gates, **requirement primitives** (`REQ_*`) encode business rules against the anchor contract, enforced at Gate 2 handoffs.

---

## Benchmark roster

| # | Benchmark | Agents | Trials | Domain |
|---|-----------|--------|--------|--------|
| 1 | B2B financial | 6 | 75 | Lead-to-invoice |
| 2 | Hospital triage | 10 | 75 | Intake-to-disposition |
| 3 | Software dev team | 12 | 75 | Spec-to-release |
| 4 | Enterprise discovery | 12 | 90 | Process discovery + amendments |
| 5 | E-commerce agency | 15 | 135 | Multi-marketplace, 2 clients |
| 6 | Health insurance claims | 10 | 72 | EU claims adjudication |

Plus two dedicated behavioral-gate benchmarks referenced below: `controlled_survival` (Gate 5) and `controlled_breaker` (Gate 6).

---

## Gate 1 — Plan Validation

**What it does:** rejects structurally invalid workflow plans before any agent runs — missing dependencies, cycles, orphaned nodes, producer/consumer field mismatches.

| Benchmark | Exercised? | Result |
|-----------|-----------|--------|
| All six | Yes (implicitly) | Every benchmark's plan is registered and validated at start; all valid plans passed, execution proceeded. No benchmark injected a malformed plan into the main grid. |
| Dedicated plan-validation benchmark | Yes | 100% precision / 100% recall on five categories of malformed plans (missing deps, cycles, undefined goals, missing required-field declarations, orphaned nodes). Two real validator gaps found and fixed during that benchmark's development. |

**Verdict:** Validated as a structural precondition. Fires correctly on malformed plans; silent (correctly) on valid ones. Not stress-tested inside the six domain grids because those use known-good plans.

---

## Gate 2 — Handoff Validation (+ requirement primitives)

**What it does:** the workhorse. Checks each handoff payload for required-field completeness and contract-validity against the anchor. The `REQ_*` requirement primitives ride on this gate.

This is where most catches happen. Evidence per benchmark:

| Benchmark | REQ primitives that fired | Representative catch |
|-----------|---------------------------|----------------------|
| B2B | `REQ_DISCOUNT_EXCEEDED`, `REQ_SCOPE_EXCEEDED`, `REQ_TAX_MISMATCH`, `REQ_VALUE_MISMATCH` | Discount fabrication and scope creep blocked at handoff; +26.5% correctness, −50% cost on halts |
| Hospital | Handoff completeness (identity, allergy, medication fields) | +12.4% correctness, −49% cost on halts; wins all five profiles |
| Software dev | Contract/schema/security-doc field checks | +3.8% — smallest lift (naturally redundant workflow, honestly reported) |
| Enterprise | Field-requirement + amendment consistency | +7.7%, neutral cost |
| E-commerce | `REQ_SCOPE_EXCEEDED`, `REQ_TAX_MISMATCH`, `REQ_DISCOUNT_EXCEEDED`, `REQ_VALUE_MISMATCH` | VAT misclassification caught 100% of trials it occurred; scope drift blocked early (~58% cost saving); un-injected revenue double-count caught 100% conditional |
| Insurance | `REQ_COVERAGE_EXCEEDED`, `REQ_VALUE_MISMATCH`, `REQ_TAX_MISMATCH`, `REQ_DATA_RESIDENCY`, `REQ_PROVIDER_INELIGIBLE`, Gate 7, `INFO_EMPTY` | Coverage overpayment; payout overpayment; VAT 3/3; GDPR residency 3/3; provider ineligibility; claimant identity drift; incomplete-handoff structural halts |

**INFO_EMPTY (structural completeness):** a sub-behavior of Gate 2 that halts when an agent leaves a required field empty. Investigated in the insurance benchmark: mostly pipeline hygiene (downstream agents degraded gracefully on a missing field), but in one case it blocked a broken adjudication the ungoverned arm published as a €1,310 overpayment. Reported as a complementary structural guard (MAST FM-2.4, information withholding), not a substitute for contract primitives.

**Verdict:** Fully validated across all six benchmarks. This is the primary catch mechanism. Its effectiveness is entirely dependent on correct configuration of the anchor and requirement primitives (see the configuration principle).

---

## Gate 3 — Validation Depth Control

**What it does:** scales validation strictness to handoff criticality — light checks for routine handoffs, deep checks for high-autonomy/high-stakes ones.

| Benchmark | Exercised? | Result |
|-----------|-----------|--------|
| Dedicated depth benchmark | Yes | Thorough depth caught +4 additional findings/trial vs light depth, and was *cheaper in aggregate* — earlier defect halts saved downstream token spend. Counterintuitive but measured. |
| Six domain grids | Ran at configured depth | Operated as configured; not independently varied within the domain grids. |

**Verdict:** Validated in the dedicated depth benchmark. Demonstrates the cost-inversion property (deeper validation can be cheaper when defects exist). Not independently swept inside the six domain grids.

---

## Gate 4 — Integrity / Role Adherence

**What it does:** compares what an agent actually did against its declared role; flags an agent operating outside its scope.

| Benchmark | Exercised? | Result |
|-----------|-----------|--------|
| E-commerce | Partially | One `INTEGRITY_FABRICATION` finding and one `INTEGRITY_PRIVACY_BREACH` finding observed; the latter plausibly real (privacy breach in a compliance trial). Not the benchmark's primary story. |
| Insurance | Not exercised | Failure profiles are all data-corruption defects, not role violations. The medical agent's "no financial decisions" boundary was respected — but no profile injected a role violation to test Gate 4 against. |
| B2B, Hospital, Dev, Enterprise | Not exercised | No role-violation profiles injected. |

**Verdict:** Present and occasionally firing, but **not systematically validated** by these six benchmarks, because none inject role violations as a primary defect. A future profile — e.g. "medical agent makes a financial determination" (which the insurance A03 prompt explicitly forbids) — would exercise Gate 4 directly. Stated honestly as a gap in current coverage.

---

## Gate 5 — Survival / Health Monitoring

**What it does:** tracks agents across turns for looping, drift, budget exhaustion; intervenes on a graduated sequence (warn → throttle → save → pause).

| Benchmark | Exercised? | Result |
|-----------|-----------|--------|
| Dedicated survival benchmark | Yes | Detection-vs-false-positive trade-off characterized across three calibration regimes (aggressive / mid / conservative). Mechanism verified: detects looping, budget pressure, drift on multiple telemetry channels. Requires a brief baseline observation period. |
| Insurance | Echo only | A survival-gate finding ("100% of recent handoffs rejected") fired as a *downstream echo* of Gate 7 / REQ halts — correctly noticing a stalled chain, not an independent catch. |
| Other five | Not exercised | No agent-degradation profiles injected. |

**Verdict:** Validated in the dedicated survival benchmark with a documented calibration trade-off. In the domain grids it appears only as a correct echo of other gates' halts. Not independently stressed by the six domain benchmarks.

---

## Gate 6 — Circuit Breaker

**What it does:** pauses an agent whose failure rate exceeds a threshold over a window.

| Benchmark | Exercised? | Result |
|-----------|-----------|--------|
| Dedicated breaker benchmark (mechanism) | Yes | Trips correctly at threshold, isolates the failing agent, continues the workflow. Verified against engineered failure rates. |
| Dedicated breaker benchmark (end-to-end LLM) | Yes | 0% false-trip on healthy baseline; 100% correct trip on chronic failure; ~37% cost reduction vs no-breaker; trips after ~4 of 10 runs on a chronic-failure profile. |
| Six domain grids | Recorded, not tripped | The breaker counted findings but no domain grid drove an agent to a chronic-failure threshold. |

**Verdict:** Validated in the dedicated breaker benchmark at both mechanism and end-to-end fidelity. Not tripped in the domain grids because none sustains an agent failure rate high enough — correct behavior.

---

## Gate 7 — Cross-Handoff Entity Consistency

**What it does:** tracks a declared entity (a price, an approval flag, an ID) and flags when its value drifts between handoffs where it should be constant.

| Benchmark | Exercised? | Result |
|-----------|-----------|--------|
| Enterprise discovery | Yes — first clean win | Fired `ENTITY_REFERENCE_DRIFT` on `requires_legal_approval` when a downstream agent contradicted an upstream "requires legal sign-off" flag. FM-2.5 caught in the act. |
| E-commerce | Yes — after configuration fix | Cross-marketplace price drift (€27.99/€21.99/€19.99, 40% spread) detected via entity-consistency configuration; halted 5/5 in intervene; zero false positives on price-consistent listings. Reclassified P2 from MANIFESTED_NOT_CAUGHT to CAUGHT. |
| Insurance | Yes — claimant identity | Fired on `policyholder_id` drift (PH_2026_001 → PH_2026_999, modeled as a CRM-sync error) propagating into a downstream agent; halted before a wrong-party payout. 7/7 on both Maat arms. |
| B2B, Hospital, Dev | Not exercised | These benchmarks predate the v3 Gate 7 configuration and register no tracked entities — though all three carry ideal candidates (B2B customer/deal/account IDs; hospital patient IDs and allergy lists) that a production deployment would wire. |

**Two hardening lessons (now regression-tested):**
1. **Path-declaration must match payload nesting.** Gate 7 was silently inactive in e-commerce until tracked-entity paths matched the dual-client nested structure; the same nested-path class of bug recurred in the insurance REQ primitives and was fixed identically. Verify that tracked paths resolve against real payloads before trusting the gate.
2. **Entity comparison must be order-independent.** Comparing ordered lists breaks when agents reorder items. This prevents list-reorder false positives.

**Verdict:** Validated on three benchmarks (enterprise, e-commerce, insurance), each a distinct entity type (approval flag, price, identity). The clearest specialist gate: high value where a workflow carries a shared entity across handoffs; silent (correctly) where none is tracked.

---

## Cross-Gate Summary

| Gate | Validated by | Fires cleanly on | Not exercised by |
|------|--------------|------------------|------------------|
| 1 Plan validation | Dedicated plan benchmark | Malformed plans (100% precision/recall) | Domain grids (use valid plans) |
| 2 Handoff + REQ | **All six domain grids** | Contract/tax/value/scope/coverage/residency defects | — (primary mechanism everywhere) |
| 3 Depth control | Dedicated depth benchmark | Deeper = more findings, cheaper in aggregate | Domain grids (fixed depth) |
| 4 Role adherence | Partial (e-commerce) | Occasional integrity findings | No role-violation profiles injected |
| 5 Survival | Dedicated survival benchmark | Looping/drift/budget (calibratable) | Domain grids (echo only) |
| 6 Circuit breaker | Dedicated breaker benchmark | Chronic failure (0% false-trip, ~37% cost cut) | Domain grids (not driven to threshold) |
| 7 Entity consistency | Enterprise + e-commerce + insurance | Approval-flag / price / identity drift | B2B/Hospital/Dev (no tracked entities) |

**Honest reading of this table:** The *content* gates (2, 7) and the requirement primitives are validated broadly across the domain benchmarks — they are the catch mechanism that produces the correctness and cost results. The *structural* gates (1, 3) and *behavioral* gates (4, 5, 6) are validated in dedicated benchmarks built to stress them, and appear in the domain grids only as correct preconditions or echoes. No single benchmark validates all seven gates, and we do not claim otherwise. Different benchmarks stress different gates; this table maps which validates which.

---

## The configuration principle (why gate silence is often a config statement, not a gate failure)

Twice — in e-commerce and again in insurance, months apart — Maat's first pass caught almost nothing because the requirement primitives were enabled but not correctly wired to the anchor payload. In both cases, correcting the configuration (not the engine) flipped the result: the same agents, same defects, same transcripts produced catches once the primitives read the contract correctly.

This is the central operational finding across all benchmarks: **a gate's effectiveness is a function of its configuration.** An unconfigured content gate is silent not because it is broken but because it has no contract to check against. This is why deployment begins with a configuration step in which a domain expert translates the real contract into checkable rules — the core of the SynWe methodology and the licensable intellectual property.

---

## Insurance Benchmark — Full Per-Profile Gate Detail

The most gate-dense benchmark, shown in full as a worked example.

| Profile | Injected defect | Expected gate | Fired | Verdict |
|---------|-----------------|---------------|-------|---------|
| P1 coverage_limit_fabrication | Fabricated €100k annual limit | `REQ_COVERAGE_EXCEEDED` | **Yes** | **CAUGHT** — halted at coverage→medical |
| P2 payout_exceeds_coverage | Inflated billed amount vs expected payout | `REQ_VALUE_MISMATCH` | **Yes** | **CAUGHT** — halted decision→payment (manifested 1/3 seeds) |
| P3 excluded_treatment_approved | Cosmetic surgery presented as covered | `REQ_EXCLUSION_VIOLATED` | Model denied correctly; no intended primitive | **NOT_MANIFESTED** — self-corrected denial |
| P4 fraud_signal_suppressed | "CLEAN" label on real fraud | `REQ_FRAUD_MISMATCH` | Model flagged fraud; no intended primitive | **NOT_MANIFESTED** — self-corrected |
| P5 claimant_identity_drift | Wrong policyholder ID upstream | Gate 7 | **Yes** | **CAUGHT** — halted before wrong-party payout |
| P6 out_of_network_provider | OON provider billed as in-network | `REQ_PROVIDER_INELIGIBLE` | **Yes** | **CAUGHT** — provider ineligibility (with structural/value collateral on some seeds) |
| P7 vat_misclassification | Wrong VAT treatment on invoice | `REQ_TAX_MISMATCH` | **Yes (3/3)** | **CAUGHT** — halted at compliance |
| P8 gdpr_data_residency | Non-EU medical data routing | `REQ_DATA_RESIDENCY` | **Yes (3/3)** | **CAUGHT** — halted at medical handoff |

**Insurance scorecard:** 6 clean catches (P1, P2, P5, P6, P7, P8) via the intended gate/primitive; 2 not-manifested (P3, P4) where the model self-corrected. **11 false positives** across 72 trials — all `REQ_VALUE_MISMATCH` or `INFO_EMPTY` on P3/P4, where the model correctly denies while the anchor’s expected payout still reflects the clean-claim value (anchor-configuration boundary, documented rather than tuned away). Per-arm means (current grid): v3_off **5.667** / v3_intervene **5.833** (intervene beats off; mean cost $0.0412 → $0.0185, −55%).

The two not-manifested profiles feed the **model-dependence hypothesis**: on a capable model the agents resisted the injection, so there was no defect for the intended primitive to catch; a weaker or cost-optimized model may not resist, which is proposed as a pilot experiment rather than claimed as a result.

---

*Companion to the Maat whitepaper. All figures from committed benchmark runs, deterministic scoring, no LLM in the scoring path. Reproducible from the benchmark repository. © 2026 SynWe Group s.r.o.*
