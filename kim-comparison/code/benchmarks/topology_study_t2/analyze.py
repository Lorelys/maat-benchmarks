"""Deterministic companion metrics + ANALYSIS.md for topology_study_t2 grids.

Does NOT modify the frozen 7-check rubric / scorer. Reads existing JSONL only
(zero LLM). Companion metrics ``outcome_class`` and ``harm_published_eur`` were
defined before the Gemini grid was analyzed — apply identically to every model.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from benchmarks.controlled_insurance_claims.anchor_fixture import build_anchor
from benchmarks.controlled_insurance_claims.failure_profiles import (
    DRIFT_DEPENDENT_ID,
    DRIFT_POLICYHOLDER_ID,
)

from .defect_match import (
    T2_PROFILES,
    expected_corrupt_payout_eur,
)
from .models import resolve_model

# Standalone: kim-comparison/code/benchmarks/... → parents[3]=kim-comparison/
ROOT = Path(__file__).resolve().parents[3]
DEFAULT_BASE = ROOT / "topology_study_t2" / "results"

TOPOLOGIES = ("pipe", "independent", "centralized")
ARMS = ("off", "intervene")

OUTCOME_CLASSES = (
    "correct_published",
    "incorrect_published",
    "justified_halt",
    "collateral_defect_halt",
    "unjustified_halt",
)

# Governance primitives that indicate the injected defect was present in the
# validated payload at the halted seam (not structural INFO_* alone).
_DEFECT_INDICATING_PRIMITIVES = frozenset({
    "REQ_VALUE_MISMATCH",
    "REQ_COVERAGE_EXCEEDED",
    "REQ_EXCLUSION_VIOLATED",
    "ENTITY_REFERENCE_DRIFT",
})

# Schema / completeness primitives: empty or missing required fields in the
# agent payload (organic output defects, unrelated to the injected profile).
_COLLATERAL_SCHEMA_PRIMITIVES = frozenset({
    "INFO_EMPTY",
    "INFO_INSUFFICIENT",
})


def load_trials(jsonl_path: Path) -> dict[str, dict[str, Any]]:
    by: dict[str, dict[str, Any]] = {}
    with jsonl_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            by[str(rec["trial_id"])] = rec
    return by


def honest_expected_payout_eur(*, seed_index: int) -> float:
    anchor = build_anchor(seed_index)
    expected = (anchor.get("source_data") or {}).get("expected") or {}
    val = expected.get("expected_payout_eur")
    if not isinstance(val, (int, float)):
        raise RuntimeError(f"seed={seed_index}: missing expected_payout_eur in anchor")
    return float(val)


def is_halted(rec: dict[str, Any]) -> bool:
    return bool(rec.get("halt_governance"))


def finding_codes(rec: dict[str, Any]) -> set[str]:
    codes: set[str] = set()
    for f in rec.get("maat_findings") or []:
        code = f.get("primitive_id") or f.get("code")
        if code:
            codes.add(str(code))
    hg = rec.get("halt_governance") or {}
    handoff = hg.get("handoff")
    if isinstance(handoff, dict):
        for f in handoff.get("findings") or []:
            code = f.get("code") or f.get("primitive_id")
            if code:
                codes.add(str(code))
    handoffs = hg.get("handoffs")
    if isinstance(handoffs, dict):
        for verdict in handoffs.values():
            if not isinstance(verdict, dict):
                continue
            for f in verdict.get("findings") or []:
                code = f.get("code") or f.get("primitive_id")
                if code:
                    codes.add(str(code))
    return codes


def published_payout_eur(rec: dict[str, Any]) -> float | None:
    """Numeric payout from published final evidence (JSONL only).

    Prefers enriched slim evidence (``published_payout_eur`` + fallback keys).
    Legacy Haiku/Gemini lines that only stored null top-level
    ``approved_payout_eur`` still fall back to the corrupt marker when
    ``defect_reached_final`` is True for P2 (pre-enrichment recording gap).
    """
    ev = rec.get("defect_evidence") or {}
    for key in (
        "published_payout_eur",
        "approved_payout_eur",
        "payment_amount_eur",
        "total_payout_eur",
        "calculation_trace_final_payout_eur",
    ):
        raw = ev.get(key)
        if isinstance(raw, (int, float)):
            return float(raw)
    if (
        rec.get("defect_reached_final")
        and rec.get("profile") == "payout_exceeds_coverage"
        and not rec.get("is_clean")
    ):
        return float(expected_corrupt_payout_eur(seed_index=int(rec.get("seed", 0))))
    return None


def evidence_shows_identity_defect(rec: dict[str, Any]) -> bool:
    ev = rec.get("defect_evidence") or {}
    if ev.get("policyholder_id") == DRIFT_POLICYHOLDER_ID:
        return True
    if ev.get("claimant_id") == DRIFT_DEPENDENT_ID:
        return True
    return False


def final_has_defect(rec: dict[str, Any], *, honest: float) -> bool:
    """Defect in the published final file — from recorded evidence, not labels."""
    if rec.get("defect_reached_final"):
        return True
    if evidence_shows_identity_defect(rec):
        return True
    payout = published_payout_eur(rec)
    if payout is not None and abs(payout - honest) > 0.02:
        return True
    return False


def defect_present_at_halt_seam(rec: dict[str, Any]) -> bool:
    """True when recorded payloads/findings show the injected defect at/upstream of halt.

    Does not use profile labels alone: requires defect-indicating primitives
    on the halt record, or corrupt markers still visible in defect_evidence.
    """
    codes = finding_codes(rec)
    if codes & _DEFECT_INDICATING_PRIMITIVES:
        return True
    ev = rec.get("defect_evidence") or {}
    if evidence_shows_identity_defect(rec):
        return True
    if rec.get("profile") == "payout_exceeds_coverage" and not rec.get("is_clean"):
        payout = ev.get("approved_payout_eur")
        if isinstance(payout, (int, float)):
            corrupt = expected_corrupt_payout_eur(seed_index=int(rec.get("seed", 0)))
            if abs(float(payout) - float(corrupt)) < 0.02:
                return True
    return False


def collateral_output_defect_at_halt(rec: dict[str, Any]) -> bool:
    """True when halt findings show empty/missing required fields (organic schema defect)."""
    return bool(finding_codes(rec) & _COLLATERAL_SCHEMA_PRIMITIVES)


def outcome_class(rec: dict[str, Any]) -> str:
    seed = int(rec.get("seed", 0))
    honest = honest_expected_payout_eur(seed_index=seed)

    if is_halted(rec):
        # Injected-profile defect at/upstream of the halt seam.
        if (
            not rec.get("is_clean")
            and rec.get("profile") != "clean"
            and defect_present_at_halt_seam(rec)
        ):
            return "justified_halt"
        # Genuine agent output defect (empty/missing required fields), unrelated
        # to the injected profile — governance catching organic incompleteness.
        if collateral_output_defect_at_halt(rec):
            return "collateral_defect_halt"
        # Halt with no defect of any kind (true false positive).
        return "unjustified_halt"

    # Completed / published final file.
    if final_has_defect(rec, honest=honest):
        return "incorrect_published"
    return "correct_published"


def harm_published_eur(rec: dict[str, Any]) -> float:
    """€ harm from a published payout vs anchor honest expected; 0 if halted."""
    if is_halted(rec):
        return 0.0
    seed = int(rec.get("seed", 0))
    honest = honest_expected_payout_eur(seed_index=seed)
    payout = published_payout_eur(rec)
    if payout is None:
        return 0.0
    return abs(payout - honest)


def rubric_total(rec: dict[str, Any]) -> float | None:
    rs = rec.get("rubric_score")
    if isinstance(rs, dict):
        total = rs.get("total")
        return float(total) if isinstance(total, (int, float)) else None
    if isinstance(rs, (int, float)):
        return float(rs)
    return None


def orch_overhead_pct(rec: dict[str, Any]) -> float | None:
    tc = rec.get("token_count") or {}
    tot = int(tc.get("total") or 0)
    orch = int(tc.get("orchestrator") or 0)
    if tot <= 0:
        return None
    return 100.0 * orch / tot


def intended_caught(rec: dict[str, Any]) -> bool:
    codes = finding_codes(rec)
    profile = rec.get("profile")
    if profile == "payout_exceeds_coverage":
        return "REQ_VALUE_MISMATCH" in codes
    if profile == "claimant_identity_drift":
        if "ENTITY_REFERENCE_DRIFT" in codes:
            return True
        return (
            rec.get("topology") == "centralized"
            and rec.get("first_flagged_by") == "orchestrator"
        )
    return False


def defect_manifested_at_seam(rec: dict[str, Any]) -> bool:
    if intended_caught(rec) or rec.get("defect_reached_final"):
        return True
    if evidence_shows_identity_defect(rec):
        return True
    if rec.get("profile") == "payout_exceeds_coverage" and not rec.get("is_clean"):
        payout = published_payout_eur(rec)
        if payout is None:
            return False
        corrupt = expected_corrupt_payout_eur(seed_index=int(rec.get("seed", 0)))
        return abs(payout - corrupt) < 0.02
    return False


def annotate_trial(rec: dict[str, Any]) -> dict[str, Any]:
    return {
        **rec,
        "outcome_class": outcome_class(rec),
        "harm_published_eur": harm_published_eur(rec),
    }


def cell_metrics(group: list[dict[str, Any]]) -> dict[str, Any]:
    annotated = [annotate_trial(r) for r in group]
    injected = [r for r in annotated if not r.get("is_clean")]
    clean = [r for r in annotated if r.get("is_clean")]

    prop_n = sum(1 for r in injected if r.get("defect_reached_final"))
    prop_d = len(injected)
    rubrics = [rubric_total(r) for r in annotated if rubric_total(r) is not None]

    oc = Counter(r["outcome_class"] for r in annotated)
    harms = [float(r["harm_published_eur"]) for r in annotated]
    harm_sum = sum(harms)
    harm_mean = harm_sum / len(harms) if harms else 0.0

    catch_raw = catch_cond = "n/a"
    arm = annotated[0]["arm"] if annotated else None
    if arm == "intervene" and injected:
        catches = [intended_caught(r) for r in injected]
        catch_raw = f"{100.0 * sum(catches) / len(catches):.0f}% ({sum(catches)}/{len(catches)})"
        man = [r for r in injected if defect_manifested_at_seam(r)]
        cat_m = [r for r in man if intended_caught(r)]
        catch_cond = (
            f"{100.0 * len(cat_m) / len(man):.0f}% ({len(cat_m)}/{len(man)})"
            if man
            else "n/a (0 manifested)"
        )

    costs = [float(r.get("cost_usd") or 0) for r in annotated]
    oh = [orch_overhead_pct(r) for r in annotated if orch_overhead_pct(r) is not None]
    topo = annotated[0]["topology"] if annotated else ""
    if topo == "centralized" and oh:
        oh_s = f"{sum(oh) / len(oh):.1f}"
    elif topo == "centralized":
        oh_s = "n/a"
    else:
        oh_s = "—"

    ff = Counter(str(r.get("first_flagged_by") or "none") for r in annotated)
    clean_fp = sum(
        1
        for r in clean
        if r.get("halt_governance") or (r.get("maat_findings") or [])
    )
    halt_no_f = sum(
        1
        for r in annotated
        if r.get("halt_governance") and not (r.get("maat_findings") or [])
    )
    exec_f = sum(1 for r in annotated if r.get("halt_execution"))

    oc_s = "/".join(str(oc.get(k, 0)) for k in OUTCOME_CLASSES)

    return {
        "n": len(annotated),
        "prop_s": f"{100.0 * prop_n / prop_d:.0f}%" if prop_d else "n/a",
        "rub_s": f"{sum(rubrics) / len(rubrics):.2f}" if rubrics else "n/a",
        "catch_raw": catch_raw,
        "catch_cond": catch_cond,
        "cost_s": f"{sum(costs) / len(costs):.4f}" if costs else "n/a",
        "oh_s": oh_s,
        "ff_s": ", ".join(f"{k}:{v}" for k, v in sorted(ff.items())),
        "clean_fp": f"{clean_fp}/{len(clean)}",
        "halt_no_f": halt_no_f,
        "exec_f": exec_f,
        "oc_counts": oc,
        "oc_s": oc_s,
        "harm_sum": harm_sum,
        "harm_mean": harm_mean,
        "annotated": annotated,
    }


def render_analysis(
    *,
    model: str,
    trials_by_id: dict[str, dict[str, Any]],
) -> str:
    spec = resolve_model(model)
    rows = list(trials_by_id.values())
    cells: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        cells[(str(r["topology"]), str(r["arm"]))].append(r)

    lines: list[str] = []
    lines.append(f"# topology_study_t2 — {spec.flag} analysis (final)")
    lines.append("")
    lines.append(f"- Model: `{spec.flag}`")
    lines.append(f"- Trials: {len(rows)} (last record per trial_id)")
    lines.append(
        f"- Source: `experiments/runs/topology_study_t2/{spec.slug}/trials.jsonl`"
    )
    lines.append(f"- Generated: {date.today().isoformat()}")
    lines.append("")
    lines.append(
        "> **Companion metrics note:** `outcome_class` and `harm_published_eur` were "
        "defined before the Gemini grid was analyzed. They are computed identically "
        "for every model from existing JSONL only (no scorer / rubric changes)."
    )
    lines.append("")
    lines.append(
        "> **Rubric note:** Halted intervene chains score low on the final-file "
        "rubric by construction. Propagation, catch|manifested, outcome_class, and "
        "harm € are the primary outcomes; mean rubric under intervene is secondary."
    )
    lines.append("")
    lines.append(
        "outcome_class order in counts: "
        "`correct_published` / `incorrect_published` / `justified_halt` / "
        "`collateral_defect_halt` / `unjustified_halt`"
    )
    lines.append("")
    lines.append("## Topology × arm summary")
    lines.append("")
    lines.append(
        "| topo | arm | n | prop% | rubric | catch% (raw) | catch\\|manifested | "
        "outcome counts | harm € sum | harm € mean | cost$ | orch% | "
        "first_flagged_by | cleanFP | haltNoF | execF |"
    )
    lines.append(
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"
    )

    metrics: dict[tuple[str, str], dict[str, Any]] = {}
    for topo in TOPOLOGIES:
        for arm in ARMS:
            group = cells.get((topo, arm), [])
            if not group:
                continue
            m = cell_metrics(group)
            metrics[(topo, arm)] = m
            lines.append(
                f"| {topo} | {arm} | {m['n']} | {m['prop_s']} | {m['rub_s']} | "
                f"{m['catch_raw']} | {m['catch_cond']} | {m['oc_s']} | "
                f"{m['harm_sum']:.2f} | {m['harm_mean']:.2f} | {m['cost_s']} | "
                f"{m['oh_s']} | {m['ff_s']} | {m['clean_fp']} | {m['halt_no_f']} | "
                f"{m['exec_f']} |"
            )

    lines.append("")
    lines.append("### catch|manifested detail (intervene injected)")
    lines.append("")
    for topo in TOPOLOGIES:
        no_defect: list[str] = []
        caught_n = man_n = 0
        for profile in T2_PROFILES:
            for seed in (0, 1, 2):
                # find matching trial
                matches = [
                    r
                    for r in rows
                    if r.get("topology") == topo
                    and r.get("arm") == "intervene"
                    and r.get("profile") == profile
                    and int(r.get("seed", -1)) == seed
                    and not r.get("is_clean")
                ]
                if not matches:
                    continue
                r = matches[0]
                label = f"{profile}/seed{seed}"
                if not defect_manifested_at_seam(r):
                    no_defect.append(label)
                else:
                    man_n += 1
                    if intended_caught(r):
                        caught_n += 1
        lines.append(f"- **{topo}:** caught/manifested = {caught_n}/{man_n}")
        lines.append(
            f"  - no-defect-to-catch: {', '.join(no_defect) if no_defect else '—'}"
        )

    lines.append("")
    lines.append("## Clean-control (intervene)")
    lines.append("")
    for topo in TOPOLOGIES:
        matches = [
            r
            for r in rows
            if r.get("topology") == topo
            and r.get("arm") == "intervene"
            and r.get("is_clean")
        ]
        if not matches:
            lines.append(f"- **{topo}:** (missing)")
            continue
        r = annotate_trial(matches[0])
        ok = not r.get("halt_governance") and not (r.get("maat_findings") or [])
        status = "PASS (zero governance findings)" if ok else "FAIL"
        lines.append(
            f"- **{topo}:** {status} — outcome=`{r['outcome_class']}`, "
            f"harm€={r['harm_published_eur']:.2f}, "
            f"findings={r.get('maat_findings') or []}, "
            f"rubric={rubric_total(r)}, cost=${r.get('cost_usd')}"
        )

    lines.append("")
    lines.append("## Outcome class + harm (definitions)")
    lines.append("")
    lines.append(
        "- **correct_published** — completed; no defect in final evidence "
        "(not `defect_reached_final`, payout equals honest expected when present, "
        "no drifted identity in evidence)."
    )
    lines.append(
        "- **incorrect_published** — completed with defect in final evidence "
        "(`defect_reached_final`, drifted identity, or published payout ≠ honest)."
    )
    lines.append(
        "- **justified_halt** — governance halt with a defect-indicating finding "
        "(`REQ_VALUE_MISMATCH`, `ENTITY_REFERENCE_DRIFT`, …) showing the "
        "*injected* defect was present at/upstream of the halted seam."
    )
    lines.append(
        "- **collateral_defect_halt** — governance halt on a genuine agent "
        "output defect (empty/missing required fields: `INFO_EMPTY`, "
        "`INFO_INSUFFICIENT`) unrelated to the injected profile."
    )
    lines.append(
        "- **unjustified_halt** — halt with no defect of any kind present "
        "(true false positive)."
    )
    lines.append(
        "- **harm_published_eur** — `|published approved_payout_eur − honest "
        "expected|` when a final file was published; `0` if equal or if halted."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def write_analysis(*, model: str, base_dir: Path) -> Path:
    spec = resolve_model(model)
    jsonl = base_dir / spec.slug / "trials.jsonl"
    if not jsonl.is_file():
        raise FileNotFoundError(jsonl)
    trials = load_trials(jsonl)
    text = render_analysis(model=model, trials_by_id=trials)
    out = base_dir / spec.slug / "ANALYSIS.md"
    out.write_text(text, encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="topology_study_t2 ANALYSIS.md")
    parser.add_argument("--model", required=True, help="Model flag (e.g. claude-haiku-4.5)")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_BASE,
        help=f"Base runs dir (default: {DEFAULT_BASE})",
    )
    args = parser.parse_args(argv)
    base = args.output_dir
    if not base.is_absolute():
        base = ROOT / base
    out = write_analysis(model=args.model, base_dir=base)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
