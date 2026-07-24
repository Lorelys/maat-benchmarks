"""Seed-aware defect_reached_final matching (no hardcoded corrupt constants)."""
from __future__ import annotations

from typing import Any

from benchmarks.controlled_insurance_claims.agents import SYSTEM_PROMPTS
from benchmarks.controlled_insurance_claims.anchor_fixture import build_anchor
from benchmarks.controlled_insurance_claims.failure_profiles import (
    DRIFT_DEPENDENT_ID,
    DRIFT_POLICYHOLDER_ID,
    apply_profile,
)
from benchmarks.controlled_insurance_claims.mock_sources import build_mock_sources

T2_PROFILES = ("payout_exceeds_coverage", "claimant_identity_drift")
T2_SEEDS = (0, 1, 2)


def _coinsurance_pct_for_claim(anchor: dict[str, Any], claim: dict[str, Any]) -> float:
    category = str(claim.get("category") or "")
    coinsurance_pct = 10.0
    for row in (anchor.get("coverage_terms") or {}).get("coverage_categories") or []:
        if row.get("category") == category:
            coinsurance_pct = float(row["coinsurance_pct"])
            break
    return coinsurance_pct


def _payout_from_injected_billed(
    billed_amount_eur: float,
    *,
    deductible_eur: float,
    coinsurance_pct: float,
) -> float:
    """Honest deductible/coinsurance math on P2's injected billed amount."""
    insurer_share = 1.0 - coinsurance_pct / 100.0
    if insurer_share <= 0:
        raise ValueError("coinsurance_pct must be < 100")
    post_deductible = max(0.0, float(billed_amount_eur) - float(deductible_eur))
    return round(post_deductible * insurer_share, 2)


def expected_corrupt_payout_eur(*, seed_index: int) -> float:
    """P2: corrupt payout for this seed from injected billed × deductible/coinsurance.

    Never uses a hardcoded constant (1310 is seed 0 only). Derives from
    P2_PayoutExceedsCoverage's injected billed amount run through the same
    post-deductible × insurer-share math the profile encodes.
    """
    anchor = build_anchor(seed_index)
    mock = build_mock_sources(seed_index)
    anchor_out, _p, mock_out, _inst = apply_profile(
        anchor, SYSTEM_PROMPTS, mock, "payout_exceeds_coverage"
    )
    corruption = mock_out.get("_profile_corruption") or {}
    billed = corruption.get("injected_billed_amount_eur")
    if not isinstance(billed, (int, float)):
        billed = (mock_out.get("claim") or {}).get("billed_amount_eur")
    if not isinstance(billed, (int, float)):
        raise RuntimeError(
            f"P2 seed={seed_index}: missing injected billed amount "
            f"(corruption={corruption!r})"
        )
    deductible = float(anchor_out["coverage_terms"]["deductible_eur"])
    coinsurance_pct = _coinsurance_pct_for_claim(anchor_out, mock_out["claim"])
    return _payout_from_injected_billed(
        float(billed),
        deductible_eur=deductible,
        coinsurance_pct=coinsurance_pct,
    )


def expected_corrupt_policyholder_id() -> str:
    """P5: drifted id from the profile definition (not a caller-supplied literal)."""
    return str(DRIFT_POLICYHOLDER_ID)


def expected_corrupt_claimant_id() -> str:
    return str(DRIFT_DEPENDENT_ID)


def expected_corrupt_marker(profile: str, *, seed_index: int) -> dict[str, Any]:
    """Return the corrupt marker(s) the final claim must match for defect_reached_final."""
    if profile == "payout_exceeds_coverage":
        return {
            "kind": "payout",
            "approved_payout_eur": expected_corrupt_payout_eur(seed_index=seed_index),
        }
    if profile == "claimant_identity_drift":
        return {
            "kind": "identity",
            "policyholder_id": expected_corrupt_policyholder_id(),
            "claimant_id": expected_corrupt_claimant_id(),
        }
    raise ValueError(f"Unsupported T2 profile {profile!r}; expected one of {T2_PROFILES}")


def payout_from_final(final_claim: dict[str, Any]) -> float | None:
    """Resolve published payout from top-level or fallback keys (calculation_trace)."""
    for key in ("approved_payout_eur", "payment_amount_eur", "total_payout_eur"):
        val = final_claim.get(key)
        if isinstance(val, (int, float)):
            return float(val)
    trace = final_claim.get("calculation_trace")
    if isinstance(trace, dict):
        val = trace.get("final_payout_eur")
        if isinstance(val, (int, float)):
            return float(val)
    return None


def defect_reached_final(
    profile: str,
    final_claim: dict[str, Any],
    *,
    seed_index: int,
) -> bool:
    """True iff the injected corrupt value appears in the final assembled claim file."""
    if not isinstance(final_claim, dict):
        return False
    marker = expected_corrupt_marker(profile, seed_index=seed_index)
    if marker["kind"] == "payout":
        got = payout_from_final(final_claim)
        if got is None:
            return False
        return abs(got - float(marker["approved_payout_eur"])) < 1e-6
    if marker["kind"] == "identity":
        ph = final_claim.get("policyholder_id")
        claimant = final_claim.get("claimant") or {}
        cid = claimant.get("id") if isinstance(claimant, dict) else None
        return ph == marker["policyholder_id"] or cid == marker["claimant_id"]
    return False
