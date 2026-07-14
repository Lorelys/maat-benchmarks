# Workstream B — Six-Benchmark Consolidated Deterministic Re-score

**Rubric philosophy:** ~7 business-meaningful boolean checks per benchmark (0–7 scale; e-commerce legacy scorer remains 0–15 for continuity). Zero LLM in all scorers.

## Methodology: original scorers were LLM-judge?

| benchmark | `rg` on `scorer*.py` | verdict |
|-----------|----------------------|---------|
| controlled_hospital | no anthropic/openai/messages.create | **deterministic** (0–3 disposition) |
| controlled_devteam | no anthropic/openai/messages.create | **deterministic** (0–3 release) |
| controlled_enterprise_discovery | no anthropic/openai/messages.create | **deterministic** (0–3) |
| controlled_b2b | no anthropic/openai/messages.create | **deterministic** (0–3 invoice) |
| controlled_ecommerce_agency | no anthropic/openai/messages.create | **deterministic** (legacy 0–15) |

## Fleet headline — Maat off vs Maat on

| benchmark | off arm | on arm | legacy off | legacy on | Δ legacy | legacy % | det off (0–7) | det on | Δ det | det % | halt (on) | cost off ($) | cost on ($) | original headline |
|-----------|---------|--------|------------|-----------|----------|----------|---------------|--------|-------|-------|-----------|--------------|-------------|-------------------|
| controlled_b2b | maat_off | maat_on_halt | 1.920 | 2.720 | +0.800 | +41.7% | 5.280 | 6.680 | +1.400 | +26.5% | 0.80 | 0.0088 | 0.0044 | +41.7% |
| controlled_hospital | maat_off | maat_on_halt | 2.527 | 2.860 | +0.333 | +13.2% | 6.120 | 6.880 | +0.760 | +12.4% | 0.88 | 0.0249 | 0.0127 | +13.2% |
| controlled_devteam | maat_off | maat_on_halt | 2.960 | 2.960 | +0.000 | +0.0% | 6.240 | 6.480 | +0.240 | +3.8% | 0.28 | 0.0568 | 0.0522 | ≈0% |
| controlled_enterprise_discovery | v3_off | v3_intervene | 2.500 | 3.000 | +0.500 | +20.0% | 6.500 | 7.000 | +0.500 | +7.7% | 0.17 | 0.0868 | 0.0862 | +20.0% |
| controlled_ecommerce_agency | v3_off | v3_intervene | 13.733 | 14.400 | +0.667 | +4.9% | 6.222 | 6.889 | +0.667 | +10.7% | 0.40 | 0.2090 | 0.1740 | +4.9% |
| controlled_insurance_claims | v3_off | v3_intervene | — | — | — | — | 5.417 | 5.625 | +0.208 | +3.9% | 0.71 | 0.0425 | 0.0272 | config-flip |

Insurance (benchmark 6) uses the 7-check rubric natively; its headline is the configuration flip — the same trials scored 4.75 unconfigured and 5.63 configured — plus four clean regulated catches (payout, identity, VAT, GDPR) with zero false positives. See `results/controlled_insurance_claims/`.

## Direction preservation (deterministic 7-check vs legacy)

- **controlled_b2b:** legacy Δ=+0.800, 7-check Δ=+1.400 → **consistent, stronger**
- **controlled_hospital:** legacy Δ=+0.333, 7-check Δ=+0.760 → **consistent, stronger**
- **controlled_devteam:** legacy Δ=+0.000, 7-check Δ=+0.240 → **consistent, stronger**
- **controlled_enterprise_discovery:** legacy Δ=+0.500, 7-check Δ=+0.500 → **consistent**
- **controlled_ecommerce_agency:** legacy Δ=+0.351, 7-check Δ=+0.516 → **consistent, stronger**
