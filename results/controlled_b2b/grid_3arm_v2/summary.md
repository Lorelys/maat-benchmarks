# B2B Grid — Three-Arm Comparison

Trials completed: **75** / 75
Total cost: **$0.6893** (cap $2.00)

Arms: maat_off (no validation), maat_on (halt-only), maat_on_retry (up to 3 retries).
Scoring: invoice correctness vs ground truth.

## Comparison (profile × mode)

| profile | metric | maat_off | maat_on_halt | maat_on_retry | Δ(halt−off) | Δ(retry−halt) | Δ(retry−off) |
|---------|--------|----------|--------------|---------------|-------------|---------------|--------------|
| discount_fabrication | correctness | 2.000 | 2.800 | 2.400 | +0.800 | -0.400 | +0.400 |
| discount_fabrication | cost ($) | 0.0093 | 0.0041 | 0.0128 | -0.0052 | +0.0087 | +0.0035 |
| discount_fabrication | halt rate | 0.000 | 0.800 | 0.400 | +0.800 | -0.400 | +0.400 |
| discount_fabrication | retries | 0.000 | 0.000 | 2.600 | +0.000 | +2.600 | +2.600 |
| | | | | | | | |
| scope_creep | correctness | 2.000 | 2.600 | 2.200 | +0.600 | -0.400 | +0.200 |
| scope_creep | cost ($) | 0.0093 | 0.0073 | 0.0131 | -0.0020 | +0.0059 | +0.0038 |
| scope_creep | halt rate | 0.000 | 0.600 | 0.200 | +0.600 | -0.400 | +0.200 |
| scope_creep | retries | 0.000 | 0.000 | 2.000 | +0.000 | +2.000 | +2.000 |
| | | | | | | | |
| usage_inflation | correctness | 1.000 | 2.200 | 1.000 | +1.200 | -1.200 | +0.000 |
| usage_inflation | cost ($) | 0.0089 | 0.0064 | 0.0102 | -0.0025 | +0.0038 | +0.0013 |
| usage_inflation | halt rate | 0.000 | 0.600 | 0.000 | +0.600 | -0.600 | +0.000 |
| usage_inflation | retries | 0.000 | 0.000 | 0.600 | +0.000 | +0.600 | +0.600 |
| | | | | | | | |
| contract_mismatch | correctness | 2.000 | 2.000 | 1.600 | +0.000 | -0.400 | -0.400 |
| contract_mismatch | cost ($) | 0.0089 | 0.0063 | 0.0119 | -0.0026 | +0.0056 | +0.0030 |
| contract_mismatch | halt rate | 0.000 | 0.600 | 0.200 | +0.600 | -0.400 | +0.200 |
| contract_mismatch | retries | 0.000 | 0.000 | 1.400 | +0.000 | +1.400 | +1.400 |
| | | | | | | | |
| sla_drift | correctness | 2.000 | 3.000 | 1.600 | +1.000 | -1.400 | -0.400 |
| sla_drift | cost ($) | 0.0089 | 0.0051 | 0.0152 | -0.0038 | +0.0101 | +0.0063 |
| sla_drift | halt rate | 0.000 | 1.000 | 0.200 | +1.000 | -0.800 | +0.200 |
| sla_drift | retries | 0.000 | 0.000 | 3.400 | +0.000 | +3.400 | +3.400 |
| | | | | | | | |

