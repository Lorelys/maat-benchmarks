"""Anchor fixture for controlled insurance claims benchmark.

Anchor sections (planned):
- Policy & Parties (including dependents)
- Coverage Terms
- Provider & Payment
- Compliance

Ground-truth expectations under source_data.expected (planned):
- expected_payout_eur
- coverage determination (covered vs denied + rationale)
- fraud truth (true/false + signal source)
- provider eligibility truth (in-network / out-of-network / sanctioned)
- tax truth (VAT treatment correctness)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


def build_anchor(seed: int = 0) -> dict[str, Any]:
    jurisdiction = {0: "DE", 1: "FR", 2: "NL"}.get(int(seed), "DE")
    vat_rate_pct = VAT_RATES_PCT[jurisdiction]

    policyholder_id = "PH_2026_001"
    dependents = [
        {
            "dependent_id": "DEP_2026_001",
            "name": "Mila Schneider",
            "relationship": "child",
            "date_of_birth": "2014-05-12",
        },
        {
            "dependent_id": "DEP_2026_002",
            "name": "Jonas Schneider",
            "relationship": "spouse",
            "date_of_birth": "1990-11-03",
        },
    ]

    anchor: dict[str, Any] = {
        "policy_and_parties": {
            "policy_id": "POL_2026_EU_001",
            "policyholder_id": policyholder_id,
            "policyholder_name": "Anna Schneider",
            "dependents": dependents,
            "policy_period": {"start_date": "2026-01-01", "end_date": "2026-12-31"},
            "jurisdiction": jurisdiction,
            "data_residency": "EU",
        },
        "coverage_terms": {
            "coverage_type": "individual_family_health",
            "annual_limit_eur": 50000,
            "deductible_eur": 300,
            "coverage_categories": _coverage_categories(),
            "exclusions": [
                "cosmetic_surgery",
                "experimental_treatment",
                "pre_existing_undeclared",
            ],
            "waiting_periods": _waiting_periods(),
        },
        "provider_and_payment": {
            "eligible_provider_network": _provider_network(),
            "reimbursement_rules": {
                "in_network": {"coinsurance_pct": 10},
                "out_of_network": {"coinsurance_pct": 30},
            },
            "payment_terms": {
                "currency": "EUR",
                "payment_method": "reimburse_policyholder",
            },
        },
        "compliance_governance": {
            "regulatory_framework": ["GDPR", "national_insurance_supervision"],
            "tax_treatment": {
                jurisdiction: {
                    "vat_rate_pct": vat_rate_pct,
                    "vat_included_in_invoice": True,
                    "note": "Medical services invoice VAT per jurisdiction rate (benchmark simplification).",
                }
            },
            "data_handling_rules": "GDPR_special_category_medical_data",
            "escalation_authority": "DPA_and_national_insurance_supervisor",
        },
    }

    scenario = claim_scenario(seed=seed, anchor=anchor)
    expected = _expected_from_scenario(seed=seed, anchor=anchor, scenario=scenario)
    anchor["source_data"] = {
        "scenario": scenario,
        "expected": expected,
    }
    return anchor


VAT_RATES_PCT: dict[str, int] = {
    "DE": 19,
    "FR": 20,
    "NL": 21,
}


def _coverage_categories() -> list[dict[str, Any]]:
    # coinsurance_pct is the insured share (insurer pays 100 - coinsurance_pct after deductible/sub-limit).
    # Sub-limits are per-category annual caps for this simplified benchmark.
    return [
        {"category": "outpatient", "covered": True, "sub_limit_eur": 5000, "coinsurance_pct": 10},
        {"category": "inpatient", "covered": True, "sub_limit_eur": 30000, "coinsurance_pct": 10},
        {"category": "diagnostics", "covered": True, "sub_limit_eur": 2000, "coinsurance_pct": 10},
        {"category": "prescription", "covered": True, "sub_limit_eur": 1500, "coinsurance_pct": 15},
        {"category": "dental", "covered": True, "sub_limit_eur": 1200, "coinsurance_pct": 20},
        {"category": "optical", "covered": True, "sub_limit_eur": 800, "coinsurance_pct": 20},
        {"category": "maternity", "covered": True, "sub_limit_eur": 10000, "coinsurance_pct": 10},
        {"category": "mental_health", "covered": True, "sub_limit_eur": 5000, "coinsurance_pct": 10},
    ]


def _waiting_periods() -> list[dict[str, Any]]:
    # Waiting periods in days from policy start for selected categories (simplified).
    return [
        {"category": "dental", "waiting_days": 90},
        {"category": "optical", "waiting_days": 90},
        {"category": "maternity", "waiting_days": 180},
        {"category": "mental_health", "waiting_days": 30},
    ]


def _provider_network() -> list[dict[str, Any]]:
    return [
        {"provider_id": "PRV_DE_001", "name": "Berlin Klinik Mitte", "country": "DE", "in_network": True},
        {"provider_id": "PRV_FR_001", "name": "Clinique Saint-Louis", "country": "FR", "in_network": True},
        {"provider_id": "PRV_NL_001", "name": "Amsterdam Medisch Centrum", "country": "NL", "in_network": True},
        {"provider_id": "PRV_EU_004", "name": "EU Diagnostics Lab", "country": "DE", "in_network": True},
        {"provider_id": "PRV_OON_999", "name": "Private Specialist Out-of-Network", "country": "DE", "in_network": False},
    ]


@dataclass(frozen=True)
class ClaimScenario:
    claim_id: str
    policyholder_id: str
    claimant_type: str  # policyholder | dependent
    claimant_id: str
    event_date: str
    category: str
    provider_id: str
    billed_amount_eur: float
    treatment_description: str


def claim_scenario(*, seed: int = 0, anchor: dict[str, Any]) -> dict[str, Any]:
    """Deterministic per-seed claim generator used by both anchor and mock sources."""
    seed_i = int(seed) % 3
    policyholder_id = anchor["policy_and_parties"]["policyholder_id"]
    dependents = anchor["policy_and_parties"]["dependents"]

    if seed_i == 0:
        # Outpatient, policyholder
        claimant_type = "policyholder"
        claimant_id = policyholder_id
        category = "outpatient"
        provider_id = "PRV_DE_001"
        event_date = "2026-03-14"
        billed = 1200.00
        desc = "GP consultation + minor procedure (outpatient)"
    elif seed_i == 1:
        # Inpatient, policyholder
        claimant_type = "policyholder"
        claimant_id = policyholder_id
        category = "inpatient"
        provider_id = "PRV_FR_001"
        event_date = "2026-06-02"
        billed = 8000.00
        desc = "Short inpatient stay with surgical procedure"
    else:
        # Mixed + dependent: diagnostics claim for dependent child (simple single-claim trial)
        claimant_type = "dependent"
        claimant_id = str(dependents[0]["dependent_id"])
        category = "diagnostics"
        provider_id = "PRV_NL_001"
        event_date = "2026-09-21"
        billed = 900.00
        desc = "Diagnostic imaging and lab panel for dependent"

    scenario = ClaimScenario(
        claim_id=f"CLM_2026_{seed_i:03d}",
        policyholder_id=policyholder_id,
        claimant_type=claimant_type,
        claimant_id=claimant_id,
        event_date=event_date,
        category=category,
        provider_id=provider_id,
        billed_amount_eur=float(billed),
        treatment_description=desc,
    )
    return {
        "claim_id": scenario.claim_id,
        "policyholder_id": scenario.policyholder_id,
        "claimant_type": scenario.claimant_type,
        "claimant_id": scenario.claimant_id,
        "event_date": scenario.event_date,
        "category": scenario.category,
        "provider_id": scenario.provider_id,
        "billed_amount_eur": scenario.billed_amount_eur,
        "treatment_description": scenario.treatment_description,
    }


def _expected_from_scenario(*, seed: int, anchor: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    _ = seed
    policy = anchor["policy_and_parties"]
    coverage = anchor["coverage_terms"]
    provider_section = anchor["provider_and_payment"]

    category = str(scenario["category"])
    billed = float(scenario["billed_amount_eur"])
    deductible = float(coverage["deductible_eur"])

    cat = _category_cfg(coverage, category)
    sub_limit = float(cat["sub_limit_eur"])

    provider_id = str(scenario["provider_id"])
    provider = _provider_cfg(provider_section, provider_id)
    provider_ok = bool(provider["in_network"])

    coinsurance_pct = float(cat["coinsurance_pct"])
    if not provider_ok:
        coinsurance_pct = float(provider_section["reimbursement_rules"]["out_of_network"]["coinsurance_pct"])

    adjudicable = max(0.0, billed - deductible)
    adjudicable_capped = min(adjudicable, sub_limit)
    insurer_share = adjudicable_capped * (1.0 - coinsurance_pct / 100.0)

    annual_limit = float(coverage["annual_limit_eur"])
    payout = min(insurer_share, annual_limit)

    coverage_det = "covered"
    if category in set(coverage["exclusions"]):
        coverage_det = "excluded"
        payout = 0.0
    elif adjudicable > sub_limit:
        coverage_det = "partial"

    tax_truth = anchor["compliance_governance"]["tax_treatment"][policy["jurisdiction"]]

    return {
        "expected_payout_eur": round(payout, 2),
        "expected_coverage_determination": coverage_det,
        "fraud_ground_truth": False,
        "provider_eligibility_ground_truth": provider_ok,
        "tax_ground_truth": tax_truth,
    }


def _category_cfg(coverage_terms: dict[str, Any], category: str) -> dict[str, Any]:
    for row in coverage_terms["coverage_categories"]:
        if row.get("category") == category:
            return row
    raise KeyError(f"Unknown category {category!r}")


def _provider_cfg(provider_and_payment: dict[str, Any], provider_id: str) -> dict[str, Any]:
    for row in provider_and_payment["eligible_provider_network"]:
        if row.get("provider_id") == provider_id:
            return row
    raise KeyError(f"Unknown provider_id {provider_id!r}")

