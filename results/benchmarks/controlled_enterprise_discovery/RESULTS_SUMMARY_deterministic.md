# controlled_enterprise_discovery — Deterministic Re-score (7 business checks)

**Transcripts:** 90 from `experiments/runs/controlled_enterprise_discovery/grid`
**Scorer:** `scorer_deterministic.py` — 7 boolean checks (0–7), zero LLM.
**Legacy scorer:** `scorer.py` — 0–3, zero LLM.

## Rubric (business rationale)

- **in_scope_delivery_complete:** Implementation config must include ≥11/12 SOW processes — incomplete delivery.
  - *Buyer consequence:* Failed SOW sign-off; change orders and implementation rework cost.
- **shadow_processes_captured:** All known dark/shadow processes must appear in final config — operational blind spots.
  - *Buyer consequence:* Undocumented shadow IT; compliance gaps and post-go-live discovery cost.
- **manual_credit_override_tracked:** Manual credit override process must be documented — credit fraud / control gap.
  - *Buyer consequence:* Uncontrolled credit overrides; revenue leakage and SOX control failure.
- **supplier_legal_gate_preserved:** Supplier onboarding legal-approval flag must match anchor — unapproved vendor risk.
  - *Buyer consequence:* Vendor onboarded without legal review; contract and liability exposure.
- **data_residency_gdpr_compliant:** No unauthorized US data residency in outputs — GDPR transfer violation.
  - *Buyer consequence:* GDPR cross-border transfer fine (up to 4% global revenue).
- **scope_amendment_in_deliverables:** Approved scope amendments must appear in final deliverables — audit deliverable gap.
  - *Buyer consequence:* Missing compliance audit artifact; failed customer acceptance testing.
- **unauthorized_changes_blocked:** Revoked amendments must be rejected; conflicting amendments governed — scope creep.
  - *Buyer consequence:* Unauthorized scope expansion billed or deployed without executive sign-off.

## Headline comparison

| metric | legacy (0–3) | deterministic (0–7) |
|--------|------------------------------|----------------------------------|
| v3_off mean | 2.500 | 6.500 |
| v3_intervene mean | 3.000 | 7.000 |
| Δ (on − off) | +0.500 (+20.0%) | +0.500 (+7.7%) |
| halt rate (v3_intervene) | — | — | 0.17 |
| mean cost (v3_off) | $0.0868 | — |
| mean cost (v3_intervene) | $0.0862 | — |

### Original-scale headline (committed `experiments/RESULTS_SUMMARY.md`)

- v3_off → v3_intervene: **2.500** → **3.000** (+20.0%) — enterprise discovery v3

## Per-profile Δ (on − off)

| profile | Δ legacy (0–3) | legacy % | Δ det (0–7) | det % |
|---------|--------------------------|----------|-------------------------|-------|
| baseline | +0.000 | +0.0% | +0.000 | +0.0% |
| missing_dark_process | +1.000 | +50.0% | +2.000 | +40.0% |
| cross_handoff_inconsistency | +0.000 | +0.0% | +0.000 | +0.0% |
| scope_amendment | +1.000 | +50.0% | +0.000 | +0.0% |
| revoked_authorization | +0.000 | +0.0% | +0.000 | +0.0% |
| conflicting_amendments | +1.000 | +50.0% | +1.000 | +16.7% |
