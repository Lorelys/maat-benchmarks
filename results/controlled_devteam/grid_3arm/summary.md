# Devteam Grid — Three-Arm Comparison

Trials completed: **75** / 75
Total cost: **$4.1954** (cap $8.00)

Arms: maat_off (no validation), maat_on (halt-only), maat_on_retry (up to 3 retries).
Scoring: release_manager output — feature_completeness + contract_consistency + security_checks_present (0–3).

## Comparison (profile × mode)

| profile | metric | maat_off | maat_on_halt | maat_on_retry | Δ(halt−off) | Δ(retry−halt) | Δ(retry−off) |
|---------|--------|----------|--------------|---------------|-------------|---------------|--------------|
| spec_drift | correctness | 3.000 | 3.000 | 2.900 | +0.000 | -0.100 | -0.100 |
| spec_drift | cost ($) | 0.0547 | 0.0545 | 0.0561 | -0.0002 | +0.0016 | +0.0014 |
| spec_drift | halt rate | 0.000 | 0.000 | 0.000 | +0.000 | +0.000 | +0.000 |
| spec_drift | retries | 0.000 | 0.000 | 0.200 | +0.000 | +0.200 | +0.200 |
| | | | | | | | |
| api_contract_mismatch | correctness | 2.800 | 3.000 | 3.000 | +0.200 | +0.000 | +0.200 |
| api_contract_mismatch | cost ($) | 0.0563 | 0.0541 | 0.0586 | -0.0022 | +0.0045 | +0.0023 |
| api_contract_mismatch | halt rate | 0.000 | 0.200 | 0.000 | +0.200 | -0.200 | +0.000 |
| api_contract_mismatch | retries | 0.000 | 0.000 | 0.000 | +0.000 | +0.000 | +0.000 |
| | | | | | | | |
| schema_mismatch | correctness | 3.000 | 3.000 | 3.000 | +0.000 | +0.000 | +0.000 |
| schema_mismatch | cost ($) | 0.0579 | 0.0547 | 0.0602 | -0.0032 | +0.0055 | +0.0023 |
| schema_mismatch | halt rate | 0.000 | 0.200 | 0.000 | +0.200 | -0.200 | +0.000 |
| schema_mismatch | retries | 0.000 | 0.000 | 0.200 | +0.000 | +0.200 | +0.200 |
| | | | | | | | |
| security_oversight | correctness | 3.000 | 2.800 | 3.000 | -0.200 | +0.200 | +0.000 |
| security_oversight | cost ($) | 0.0577 | 0.0502 | 0.0594 | -0.0076 | +0.0092 | +0.0017 |
| security_oversight | halt rate | 0.000 | 0.400 | 0.000 | +0.400 | -0.400 | +0.000 |
| security_oversight | retries | 0.000 | 0.000 | 0.000 | +0.000 | +0.000 | +0.000 |
| | | | | | | | |
| missing_docs | correctness | 3.000 | 3.000 | 3.000 | +0.000 | +0.000 | +0.000 |
| missing_docs | cost ($) | 0.0573 | 0.0475 | 0.0599 | -0.0098 | +0.0124 | +0.0026 |
| missing_docs | halt rate | 0.000 | 0.600 | 0.000 | +0.600 | -0.600 | +0.000 |
| missing_docs | retries | 0.000 | 0.000 | 0.400 | +0.000 | +0.400 | +0.400 |
| | | | | | | | |

