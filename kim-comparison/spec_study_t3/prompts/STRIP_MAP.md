# SPEC-MIN STRIP_MAP — what was removed vs Benchmark 6 / T2 rich prompts

Source rich prompts: `benchmarks.controlled_insurance_claims.agents.SYSTEM_PROMPTS`
(identical to topology_study_t2 rich specialist prompts).

SPEC-MIN keeps: one-line generic `ROLE:` statement + `OUTPUT:` JSON schema skeleton
(field names and type hints only).

SPEC-MIN removes for **every** role (unless noted):

| Removed block | Content class |
|---|---|
| Expanded ROLE subtitle (A0N name, duty paragraph beyond one line) | domain framing |
| `ANCHOR ACCESS:` | policy / governance summary |
| `DATA SOURCES:` | domain data-routing instructions |
| `INPUT:` upstream trust rules | pipeline lore |
| Schema parentheticals that encode policy/math (e.g. “must equal A01…”, Gate 7 notes, “insured share after deductible”) | calculation / identity policy |
| Entire `BOUNDARIES:` section | domain rules, payout math, exclusion logic, GDPR/tax rules, “do not invent…”, denial triggers |

## Per-role detail

### intake
- **Removed:** Claims Intake (A01) duty paragraph; ANCHOR ACCESS (policy_and_parties, coverage categories, provider_ids); DATA SOURCES; INPUT none; schema notes tying fields to mock/anchor; BOUNDARIES (identity preserve, no invent docs, no coverage/medical/fraud/payout).
- **Retained:** one-line role; output schema keys/types.

### coverage
- **Removed:** Coverage Validation (A02) duty; ANCHOR ACCESS (jurisdiction, deductible, limits, exclusions, waiting periods); DATA SOURCES; INPUT trust rules; schema notes on coinsurance meaning; BOUNDARIES (no field rewrite, exclusion/waiting-period rules, no payout math).
- **Retained:** one-line role; output schema keys/types (including enum literals for determinations).

### medical
- **Removed:** Medical Assessment (A03) duty; ANCHOR ACCESS (data_handling_rules); DATA SOURCES; INPUT; BOUNDARIES (no financial decisions, report-only findings, null-on-missing rules).
- **Retained:** one-line role; output schema keys/types.

### fraud
- **Removed:** Fraud Detection (A04) duty; ANCHOR ACCESS; DATA SOURCES; INPUT; BOUNDARIES (must not drop signals, no identity rewrite, default low-risk, not a coverage decision).
- **Retained:** one-line role; output schema keys/types.

### decision
- **Removed:** Claims Decision (A05) adjudication duty; ANCHOR ACCESS; DATA SOURCES; INPUT multi-stage list; schema notes (Gate 7, MUST equal A01); BOUNDARIES (identity preserve; deny triggers from coverage/medical/fraud; deductible/coinsurance/sub-limit/annual_limit math; missing-input partial rules).
- **Retained:** one-line role; output schema including `calculation_trace` key skeleton (structure only — no formula text).

### payment
- **Removed:** Payment Processing (A06) duty; ANCHOR ACCESS (payment_terms); DATA SOURCES; INPUT; BOUNDARIES (amount MUST equal A05; deny→zero payment rules; no bank details).
- **Retained:** one-line role; output schema keys/types.

### provider
- **Removed:** Provider Management (A07) duty; ANCHOR ACCESS (network, reimbursement_rules); DATA SOURCES; INPUT; BOUNDARIES (invoice match rules, in-network eligibility, no payout rewrite).
- **Retained:** one-line role; output schema keys/types.

### compliance
- **Removed:** Compliance Review (A08) duty; ANCHOR ACCESS (jurisdiction, regulatory_framework, tax_treatment, data_handling_rules); DATA SOURCES; INPUT; BOUNDARIES (VAT/tax match → REQ_TAX_MISMATCH, GDPR special-category / residency rules, no payout change).
- **Retained:** one-line role; output schema keys/types.

### legal
- **Removed:** Legal Review (A09) duty; ANCHOR ACCESS; DATA SOURCES; INPUT; BOUNDARIES (when legal_review_required / recovery_flagged must be true; no new facts).
- **Retained:** one-line role; output schema keys/types.

### analytics
- **Removed:** Analytics (A10) duty; ANCHOR ACCESS; DATA SOURCES; INPUT; BOUNDARIES (total must trace to A06/A05; no invented metrics/causality).
- **Retained:** one-line role; output schema keys/types (including `cycle_metrics` skeleton).

## Freeze

This map and `min.py` are frozen after commit 1 of spec_study_t3. Profile injection
(e.g. P5 upstream-record appendages applied at runtime by Benchmark 6
`apply_profile`) is **not** part of this strip map — those appendages are
failure-profile machinery, identical across `rich` and `min` arms.
