# controlled_devteam — Deterministic Re-score (7 business checks)

**Transcripts:** 75 from `experiments/runs/controlled_devteam/grid_3arm`
**Scorer:** `scorer_deterministic.py` — 7 boolean checks (0–7), zero LLM.
**Legacy scorer:** `scorer.py` — 0–3, zero LLM.

## Rubric (business rationale)

- **all_user_stories_shipped:** Release must include all PM user stories — prevents missing contracted features.
  - *Buyer consequence:* Sprint failure; contractual feature gap and customer churn risk.
- **fe_be_api_paths_align:** Frontend API paths must overlap backend endpoints — prevents integration failure at deploy.
  - *Buyer consequence:* Production deploy blocked; hotfix cycle and delayed release revenue.
- **fe_be_payload_fields_align:** Request/response field names must match across FE/BE — prevents runtime serialization bugs.
  - *Buyer consequence:* Silent data bugs in production; customer-facing defects and rollback cost.
- **code_matches_db_schema:** Engineering code must not reference undeclared DB columns — prevents migration outages.
  - *Buyer consequence:* Database migration failure or runtime 500s; outage and incident response cost.
- **security_auth_reviewed:** Security report must cover auth/JWT/permissions — required release gate for production.
  - *Buyer consequence:* Ship vulnerable auth surface; breach liability and compliance audit failure.
- **user_stories_documented:** PM stories must appear in release documentation — audit and support readiness.
  - *Buyer consequence:* Failed SOC2/ISO audit trail; elevated support and onboarding cost.
- **spec_reflected_in_architecture:** All PM stories must trace to architecture — prevents building the wrong product.
  - *Buyer consequence:* Engineering rework when wrong capabilities built; wasted sprint capacity.

## Headline comparison

| metric | legacy (0–3) | deterministic (0–7) |
|--------|------------------------------|----------------------------------|
| maat_off mean | 2.960 | 6.240 |
| maat_on_halt mean | 2.960 | 6.480 |
| Δ (on − off) | +0.000 (+0.0%) | +0.240 (+3.8%) |
| halt rate (maat_on_halt) | — | — | 0.28 |
| mean cost (maat_off) | $0.0568 | — |
| mean cost (maat_on_halt) | $0.0522 | — |

### Original-scale headline (committed `experiments/RESULTS_SUMMARY.md`)

- maat_off → maat_on_halt: **2.960** → **2.960** (≈0%) — no material release correctness gain

## Per-profile Δ (on − off)

| profile | Δ legacy (0–3) | legacy % | Δ det (0–7) | det % |
|---------|--------------------------|----------|-------------------------|-------|
| spec_drift | +0.000 | +0.0% | +0.000 | +0.0% |
| api_contract_mismatch | +0.200 | +7.1% | +0.200 | +3.1% |
| schema_mismatch | +0.000 | +0.0% | +0.400 | +7.1% |
| security_oversight | -0.200 | -6.7% | -0.200 | -2.9% |
| missing_docs | +0.000 | +0.0% | +0.800 | +13.8% |
