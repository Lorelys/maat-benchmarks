# B2B Grid With Retry — Summary

Trials completed: **50** / 50
Total cost: **$0.4974** (cap $0.50)

Arms: maat_off (no validation), maat_on_retry (up to 3 retries on blocker rejection).
Scoring: invoice correctness vs ground truth.

## Comparison (profile × mode)

| profile | mode | mean correctness | mean cost ($) | halt rate | retries/handoff |
|---------|------|------------------|---------------|-----------|-----------------|
| discount_fabrication | maat_off | 1.600 | 0.0087 | 0.00 | 0.00 |
| discount_fabrication | maat_on_retry | 2.200 | 0.0113 | 0.20 | 0.42 |
| scope_creep | maat_off | 2.400 | 0.0093 | 0.00 | 0.00 |
| scope_creep | maat_on_retry | 2.400 | 0.0113 | 0.00 | 0.20 |
| usage_inflation | maat_off | 1.400 | 0.0088 | 0.00 | 0.00 |
| usage_inflation | maat_on_retry | 1.600 | 0.0109 | 0.00 | 0.23 |
| contract_mismatch | maat_off | 2.400 | 0.0089 | 0.00 | 0.00 |
| contract_mismatch | maat_on_retry | 2.200 | 0.0101 | 0.00 | 0.17 |
| sla_drift | maat_off | 2.400 | 0.0087 | 0.00 | 0.00 |
| sla_drift | maat_on_retry | 2.400 | 0.0115 | 0.00 | 0.30 |

