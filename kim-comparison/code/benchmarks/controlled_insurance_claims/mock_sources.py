"""Mock sources for controlled insurance claims benchmark.

Planned mock sources:
- Claim documents (claim form, receipts, prior auth letters)
- Medical reports (diagnosis/procedure notes)
- Provider invoices
- Per-seed claim-type rotation:
  - seed0: outpatient
  - seed1: inpatient
  - seed2: mixed + dependent
"""

from __future__ import annotations

from datetime import date
from typing import Any

from .anchor_fixture import VAT_RATES_PCT, build_anchor, claim_scenario


def build_mock_sources(seed: int = 0) -> dict[str, Any]:
    anchor = build_anchor(seed)
    scenario = claim_scenario(seed=seed, anchor=anchor)

    policy = anchor["policy_and_parties"]
    jurisdiction = str(policy["jurisdiction"])
    vat_rate_pct = int(VAT_RATES_PCT[jurisdiction])

    provider_id = str(scenario["provider_id"])
    category = str(scenario["category"])
    billed = float(scenario["billed_amount_eur"])

    # Invoice uses VAT-inclusive totals (benchmark simplification).
    net = round(billed / (1.0 + vat_rate_pct / 100.0), 2)
    vat = round(billed - net, 2)

    claim = {
        "claim_id": scenario["claim_id"],
        "policyholder_id": scenario["policyholder_id"],
        "claimant": {
            "type": scenario["claimant_type"],
            "id": scenario["claimant_id"],
        },
        "event_date": scenario["event_date"],
        "category": category,
        "provider_id": provider_id,
        "billed_amount_eur": round(billed, 2),
        "treatment_description": scenario["treatment_description"],
    }

    medical_report = {
        "summary": f"Clinical summary for {category} claim.",
        "findings": [
            "Symptoms and presentation consistent with reported event.",
            "No contraindications noted in report.",
        ],
    }

    provider_invoice = {
        "provider_id": provider_id,
        "invoice_id": f"INV_{scenario['claim_id']}",
        "line_items": [
            {
                "description": scenario["treatment_description"],
                "net_eur": net,
                "vat_rate_pct": vat_rate_pct,
                "vat_eur": vat,
                "gross_eur": round(billed, 2),
            }
        ],
        "tax_treatment": {
            "jurisdiction": jurisdiction,
            "vat_rate_pct": vat_rate_pct,
            "vat_included": True,
        },
        "total_eur": round(billed, 2),
    }

    supporting_documents = [
        {"type": "claim_form", "id": f"DOC_{scenario['claim_id']}_FORM", "status": "submitted"},
        {"type": "invoice_pdf", "id": f"DOC_{scenario['claim_id']}_INV", "status": "attached"},
        {"type": "medical_report", "id": f"DOC_{scenario['claim_id']}_MED", "status": "attached"},
    ]

    out = {
        "claim": claim,
        "medical_report": medical_report,
        "provider_invoice": provider_invoice,
        "supporting_documents": supporting_documents,
    }

    verify_consistency(anchor=anchor, mock_sources=out)
    return out


def verify_consistency(*, anchor: dict[str, Any], mock_sources: dict[str, Any]) -> None:
    claim = mock_sources.get("claim") or {}
    policy = anchor.get("policy_and_parties") or {}
    coverage = anchor.get("coverage_terms") or {}
    provider = anchor.get("provider_and_payment") or {}

    # Category exists in coverage categories
    categories = {row.get("category") for row in (coverage.get("coverage_categories") or [])}
    if claim.get("category") not in categories:
        raise ValueError(f"claim.category {claim.get('category')!r} not in anchor coverage categories")

    # Provider exists in anchor network
    providers = {row.get("provider_id") for row in (provider.get("eligible_provider_network") or [])}
    if claim.get("provider_id") not in providers:
        raise ValueError(f"claim.provider_id {claim.get('provider_id')!r} not in anchor provider network")

    # Claimant is policyholder or dependent
    policyholder_id = policy.get("policyholder_id")
    dependents = policy.get("dependents") or []
    dependent_ids = {d.get("dependent_id") for d in dependents}
    claimant = claim.get("claimant") or {}
    claimant_id = claimant.get("id")
    claimant_type = claimant.get("type")
    if claimant_type == "policyholder":
        if claimant_id != policyholder_id:
            raise ValueError("claim.claimant.id must match anchor policyholder_id for policyholder claim")
    elif claimant_type == "dependent":
        if claimant_id not in dependent_ids:
            raise ValueError("claim.claimant.id must match one of anchor dependents for dependent claim")
    else:
        raise ValueError("claim.claimant.type must be 'policyholder' or 'dependent'")

    # event_date within policy period
    period = policy.get("policy_period") or {}
    start = date.fromisoformat(period["start_date"])
    end = date.fromisoformat(period["end_date"])
    ev = date.fromisoformat(str(claim["event_date"]))
    if not (start <= ev <= end):
        raise ValueError("claim.event_date must be within policy_period")

    # Amounts align with invoice total
    inv = mock_sources.get("provider_invoice") or {}
    billed = float(claim.get("billed_amount_eur") or 0.0)
    total = float(inv.get("total_eur") or 0.0)
    if round(billed, 2) != round(total, 2):
        raise ValueError("claim.billed_amount_eur must equal provider_invoice.total_eur")

