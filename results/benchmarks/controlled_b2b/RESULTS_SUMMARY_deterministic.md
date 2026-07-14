# controlled_b2b — Deterministic Re-score (7 business checks)

**Transcripts:** 75 from `experiments/runs/controlled_b2b/grid_with_fixes`
**Scorer:** `scorer_deterministic.py` — 7 boolean checks (0–7), zero LLM.
**Legacy scorer:** `scorer.py` — 0–3, zero LLM.

## Rubric (business rationale)

- **invoice_matches_contract:** Final invoice total must match contracted subscription plus legitimate usage — prevents overbilling.
  - *Buyer consequence:* Direct monetary loss from incorrect invoice totals and disputed payments.
- **contract_tier_on_invoice:** Invoice pricing tier must match the signed deal tier — prevents wrong SLA/support billing.
  - *Buyer consequence:* Paying enterprise SLA rates for standard tier (or vice versa); contract dispute risk.
- **usage_billing_legitimate:** Billable units must stay within plausible usage — prevents inflated metered charges.
  - *Buyer consequence:* Overcharged usage fees on API/consumption meters; refund and audit exposure.
- **sla_tier_matches_deal:** Account SLA tier must match deal tier — prevents service-level / penalty mismatch.
  - *Buyer consequence:* Missed uptime credits or wrong support entitlements; SLA breach exposure.
- **entitlements_within_contract:** Onboarding entitlements and integrations must stay within contract bounds — prevents scope creep delivery.
  - *Buyer consequence:* Unpaid feature/integration delivery; change-order and margin leakage.
- **deal_value_not_discounted:** Deal total must stay within seed budget without fabricated discounts — prevents unauthorized revenue loss.
  - *Buyer consequence:* Unauthorized discount erodes ARR; finance reconciliation failures.
- **customer_billing_chain_intact:** Customer ID must be consistent across billing agents — prevents charges to wrong account.
  - *Buyer consequence:* Invoice sent to wrong customer entity; collections failure and compliance risk.

## Headline comparison

| metric | legacy (0–3) | deterministic (0–7) |
|--------|------------------------------|----------------------------------|
| maat_off mean | 1.920 | 5.280 |
| maat_on_halt mean | 2.720 | 6.680 |
| Δ (on − off) | +0.800 (+41.7%) | +1.400 (+26.5%) |
| halt rate (maat_on_halt) | — | — | 0.80 |
| mean cost (maat_off) | $0.0088 | — |
| mean cost (maat_on_halt) | $0.0044 | — |

### Original-scale headline (committed `experiments/RESULTS_SUMMARY.md`)

- maat_off → maat_on_halt: **1.920** → **2.720** (+41.7%) — ~+42% correctness (B2B v1)

## Per-profile Δ (on − off)

| profile | Δ legacy (0–3) | legacy % | Δ det (0–7) | det % |
|---------|--------------------------|----------|-------------------------|-------|
| discount_fabrication | +1.200 | +66.7% | +1.800 | +34.6% |
| scope_creep | +0.400 | +16.7% | +1.400 | +26.9% |
| usage_inflation | +1.000 | +83.3% | +1.400 | +29.2% |
| contract_mismatch | +0.400 | +18.2% | +0.400 | +6.5% |
| sla_drift | +1.000 | +50.0% | +2.000 | +40.0% |
