# B2B Grid — Three-Arm Comparison

Trials completed: **75** / 75
Total cost: **$0.6236** (cap $2.00)

Arms: maat_off (no validation), maat_on (halt-only), maat_on_retry (up to 3 retries).
Scoring: invoice correctness vs ground truth.

## Comparison (profile × mode)

| profile | metric | maat_off | maat_on_halt | maat_on_retry | Δ(halt−off) | Δ(retry−halt) | Δ(retry−off) |
|---------|--------|----------|--------------|---------------|-------------|---------------|--------------|
| discount_fabrication | correctness | 2.000 | 2.800 | 2.000 | +0.800 | -0.800 | +0.000 |
| discount_fabrication | cost ($) | 0.0092 | 0.0040 | 0.0102 | -0.0052 | +0.0063 | +0.0010 |
| discount_fabrication | halt rate | 0.000 | 0.800 | 0.000 | +0.800 | -0.800 | +0.000 |
| discount_fabrication | retries | 0.000 | 0.000 | 0.600 | +0.000 | +0.600 | +0.600 |
| | | | | | | | |
| scope_creep | correctness | 2.000 | 2.600 | 2.000 | +0.600 | -0.600 | +0.000 |
| scope_creep | cost ($) | 0.0094 | 0.0060 | 0.0097 | -0.0034 | +0.0037 | +0.0003 |
| scope_creep | halt rate | 0.000 | 0.600 | 0.000 | +0.600 | -0.600 | +0.000 |
| scope_creep | retries | 0.000 | 0.000 | 0.200 | +0.000 | +0.200 | +0.200 |
| | | | | | | | |
| usage_inflation | correctness | 1.000 | 1.400 | 1.000 | +0.400 | -0.400 | +0.000 |
| usage_inflation | cost ($) | 0.0089 | 0.0077 | 0.0097 | -0.0013 | +0.0020 | +0.0007 |
| usage_inflation | halt rate | 0.000 | 0.200 | 0.000 | +0.200 | -0.200 | +0.000 |
| usage_inflation | retries | 0.000 | 0.000 | 0.400 | +0.000 | +0.400 | +0.400 |
| | | | | | | | |
| contract_mismatch | correctness | 2.000 | 2.400 | 2.000 | +0.400 | -0.400 | +0.000 |
| contract_mismatch | cost ($) | 0.0090 | 0.0063 | 0.0093 | -0.0027 | +0.0029 | +0.0003 |
| contract_mismatch | halt rate | 0.000 | 0.400 | 0.000 | +0.400 | -0.400 | +0.000 |
| contract_mismatch | retries | 0.000 | 0.000 | 0.200 | +0.000 | +0.200 | +0.200 |
| | | | | | | | |
| sla_drift | correctness | 2.000 | 3.000 | 2.000 | +1.000 | -1.000 | +0.000 |
| sla_drift | cost ($) | 0.0090 | 0.0051 | 0.0114 | -0.0039 | +0.0063 | +0.0024 |
| sla_drift | halt rate | 0.000 | 1.000 | 0.000 | +1.000 | -1.000 | +0.000 |
| sla_drift | retries | 0.000 | 0.000 | 1.400 | +0.000 | +1.400 | +1.400 |
| | | | | | | | |

