"""Analysis for spec_study_t3: rich from T2 Haiku JSONL (read-only) + min live.

Produces T2-format summary tables with a self-correction count column.
Hypotheses H1–H4 were pre-registered in ``spec_study_t3/MAAT_SPEC_STUDY_T3.md``
before any live T3 trial.
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from benchmarks.topology_study_t2.analyze import (
    cell_metrics,
    defect_manifested_at_seam,
    intended_caught,
    is_halted,
    load_trials,
    outcome_class,
)
from benchmarks.topology_study_t2.defect_match import T2_PROFILES
from benchmarks.topology_study_t2.models import resolve_model

from .constants import ARMS, MODEL, TOPOLOGIES

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_BASE = ROOT / "spec_study_t3" / "results"
T2_HAIKU_JSONL = (
    ROOT / "topology_study_t2" / "results" / "claude-haiku-4.5" / "trials.jsonl"
)
# Analysis artifacts live here — never under ``min/`` (runner JSONL dir).
ANALYSIS_SUBDIR = "analysis"


def analysis_dir(base_dir: Path, model: str = MODEL) -> Path:
    return base_dir / resolve_model(model).slug / ANALYSIS_SUBDIR


def min_trials_jsonl(base_dir: Path, model: str = MODEL) -> Path:
    return base_dir / resolve_model(model).slug / "min" / "trials.jsonl"



def is_self_correction(rec: dict[str, Any]) -> bool:
    """Corrupt present by study design (injected off trial); honest value published.

    H4: off-arm self-correction = injected defect did not reach final and the
    published outcome is honest (``correct_published``). Static manifestation
    pre-checks establish that corruption is wired to its seam targets.
    """
    if rec.get("is_clean") or rec.get("profile") in (None, "clean"):
        return False
    if rec.get("arm") != "off":
        return False
    if is_halted(rec):
        return False
    if rec.get("defect_reached_final"):
        return False
    return outcome_class(rec) == "correct_published"


def self_correction_count(group: list[dict[str, Any]]) -> str:
    if not group:
        return "n/a"
    arm = group[0].get("arm")
    if arm != "off":
        return "—"
    injected = [r for r in group if not r.get("is_clean")]
    if not injected:
        return "0/0"
    n = sum(1 for r in injected if is_self_correction(r))
    return f"{n}/{len(injected)}"


def load_rich_from_t2(path: Path = T2_HAIKU_JSONL) -> list[dict[str, Any]]:
    """Read-only T2 Haiku trials filtered to T3 topologies; stamp spec_level=rich."""
    if not path.is_file():
        raise FileNotFoundError(f"T2 Haiku JSONL missing (read-only input): {path}")
    by_id = load_trials(path)
    rows: list[dict[str, Any]] = []
    for rec in by_id.values():
        if rec.get("topology") not in TOPOLOGIES:
            continue
        stamped = dict(rec)
        stamped["spec_level"] = "rich"
        stamped["spec_source"] = "T2 (reused)"
        rows.append(stamped)
    return rows


def load_min_from_t3(jsonl_path: Path) -> list[dict[str, Any]]:
    if not jsonl_path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for rec in load_trials(jsonl_path).values():
        stamped = dict(rec)
        stamped.setdefault("spec_level", "min")
        stamped["spec_source"] = "T3 live"
        rows.append(stamped)
    return rows


def manifestation_rate(group: list[dict[str, Any]]) -> str:
    """Off-arm: fraction of injected trials with defect_manifested_at_seam."""
    if not group:
        return "n/a"
    if group[0].get("arm") != "off":
        return "—"
    injected = [r for r in group if not r.get("is_clean")]
    if not injected:
        return "0/0"
    n = sum(1 for r in injected if defect_manifested_at_seam(r))
    return f"{n}/{len(injected)} ({100.0 * n / len(injected):.0f}%)"


def cell_metrics_t3(group: list[dict[str, Any]]) -> dict[str, Any]:
    m = cell_metrics(group)
    m["self_corr"] = self_correction_count(group)
    m["manif_s"] = manifestation_rate(group)
    return m


def render_analysis(
    *,
    rich_rows: list[dict[str, Any]],
    min_rows: list[dict[str, Any]],
    model: str = MODEL,
) -> tuple[str, list[dict[str, Any]]]:
    spec = resolve_model(model)
    lines: list[str] = []
    lines.append(f"# spec_study_t3 — {spec.flag} analysis")
    lines.append("")
    lines.append(
        "**Pre-registration:** Hypotheses H1–H4 were frozen in "
        "`spec_study_t3/MAAT_SPEC_STUDY_T3.md` **before any live T3 trial**."
    )
    lines.append("")
    lines.append(f"- Model: `{spec.flag}`")
    lines.append(
        f"- Rich rows: {len(rich_rows)} from "
        "`topology_study_t2/results/claude-haiku-4.5/trials.jsonl` "
        "(**T2 (reused)**, read-only; pipe+independent only)"
    )
    lines.append(
        f"- Min rows: {len(min_rows)} from "
        f"`spec_study_t3/results/{spec.slug}/min/trials.jsonl`"
    )
    lines.append(
        f"- Analysis outputs: `spec_study_t3/results/{spec.slug}/"
        f"{ANALYSIS_SUBDIR}/` (never written into the min trial JSONL dir)"
    )
    lines.append(f"- Generated: {date.today().isoformat()}")
    lines.append("")
    lines.append(
        "> **Rubric note:** Halted intervene chains score low on the final-file "
        "rubric by construction. Propagation, catch|manifested, outcome_class, "
        "self-correction, and harm € are the primary outcomes; mean rubric under "
        "intervene is secondary."
    )
    lines.append("")
    lines.append(
        "outcome_class order in counts: "
        "`correct_published` / `incorrect_published` / `justified_halt` / "
        "`collateral_defect_halt` / `unjustified_halt`"
    )
    lines.append("")
    lines.append(
        "**Self-correction (H4):** off-arm injected trials where corruption is "
        "wired to its seam (static pre-check) but the published final is honest "
        "(`correct_published`, `defect_reached_final=false`). Intervene cells: `—`."
    )
    lines.append("")
    lines.append("## Spec × topology × arm summary")
    lines.append("")
    lines.append(
        "| spec_level | source | topo | arm | n | manif (off) | prop% | "
        "catch\\|manifested | outcome counts | self-corr | "
        "harm € sum | cost$ (mean) |"
    )
    lines.append(
        "|---|---|---|---|---|---|---|---|---|---|---|---|"
    )

    csv_rows: list[dict[str, Any]] = []
    for spec_level, source_label, rows in (
        ("rich", "T2 (reused)", rich_rows),
        ("min", "T3 live", min_rows),
    ):
        cells: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for r in rows:
            cells[(str(r["topology"]), str(r["arm"]))].append(r)
        for topo in TOPOLOGIES:
            for arm in ARMS:
                group = cells.get((topo, arm), [])
                if not group:
                    lines.append(
                        f"| {spec_level} | {source_label} | {topo} | {arm} | "
                        f"0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a |"
                    )
                    csv_rows.append({
                        "spec_level": spec_level,
                        "source": source_label,
                        "topology": topo,
                        "arm": arm,
                        "n": 0,
                        "manif": "n/a",
                        "prop": "n/a",
                        "catch_manifested": "n/a",
                        "outcome_counts": "n/a",
                        "self_corr": "n/a",
                        "harm_sum": "",
                        "cost": "n/a",
                    })
                    continue
                m = cell_metrics_t3(group)
                lines.append(
                    f"| {spec_level} | {source_label} | {topo} | {arm} | "
                    f"{m['n']} | {m['manif_s']} | {m['prop_s']} | "
                    f"{m['catch_cond']} | {m['oc_s']} | {m['self_corr']} | "
                    f"{m['harm_sum']:.2f} | {m['cost_s']} |"
                )
                csv_rows.append({
                    "spec_level": spec_level,
                    "source": source_label,
                    "topology": topo,
                    "arm": arm,
                    "n": m["n"],
                    "manif": m["manif_s"],
                    "prop": m["prop_s"],
                    "catch_manifested": m["catch_cond"],
                    "outcome_counts": m["oc_s"],
                    "self_corr": m["self_corr"],
                    "harm_sum": f"{m['harm_sum']:.2f}",
                    "cost": m["cost_s"],
                })

    lines.append("")
    lines.append("### catch|manifested detail (intervene injected)")
    lines.append("")
    for spec_level, rows in (("rich", rich_rows), ("min", min_rows)):
        for topo in TOPOLOGIES:
            no_defect: list[str] = []
            caught_n = man_n = 0
            for profile in T2_PROFILES:
                for seed in (0, 1, 2):
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
            lines.append(
                f"- **{spec_level} / {topo}:** caught/manifested = "
                f"{caught_n}/{man_n}"
            )
            lines.append(
                f"  - no-defect-to-catch: "
                f"{', '.join(no_defect) if no_defect else '—'}"
            )

    lines.append("")
    lines.append("### Self-correction detail (off injected)")
    lines.append("")
    for spec_level, rows in (("rich", rich_rows), ("min", min_rows)):
        for topo in TOPOLOGIES:
            injected = [
                r
                for r in rows
                if r.get("topology") == topo
                and r.get("arm") == "off"
                and not r.get("is_clean")
            ]
            sc = [r for r in injected if is_self_correction(r)]
            lines.append(
                f"- **{spec_level} / {topo}:** self-corr = "
                f"{len(sc)}/{len(injected)}"
            )

    lines.append("")
    lines.append("## Clean-control status (min)")
    lines.append("")
    lines.append(
        "All four min clean cells (pipe/independent × off/intervene):"
    )
    lines.append("")
    for topo in TOPOLOGIES:
        for arm in ARMS:
            matches = [
                r
                for r in min_rows
                if r.get("topology") == topo
                and r.get("arm") == arm
                and r.get("is_clean")
            ]
            if not matches:
                lines.append(f"- **{topo} / {arm}:** missing")
                continue
            r = matches[0]
            oc = outcome_class(r)
            lines.append(
                f"- **{topo} / {arm}:** `{oc}` "
                f"(halt_gov={bool(r.get('halt_governance'))}, "
                f"findings={len(r.get('maat_findings') or [])}, "
                f"rubric={(r.get('rubric_score') or {}).get('total')})"
            )
    min_collateral = [
        r for r in min_rows if outcome_class(r) == "collateral_defect_halt"
    ]
    lines.append("")
    lines.append(
        f"**collateral_defect_halt under min:** {len(min_collateral)} "
        "(T2 taxonomy: organic INFO_EMPTY / INFO_INSUFFICIENT at halt)."
    )
    if min_collateral:
        for r in min_collateral:
            lines.append(f"- `{r.get('trial_id')}`")
    else:
        lines.append("- none")

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append(
        "- `spec_level=rich` is never live-run in T3; cells are labeled "
        "**T2 (reused)**."
    )
    lines.append(
        "- Maat gate/REQ/Gate7 configuration is byte-identical across rich/min "
        "(see `maat_config_hash` hermetic)."
    )
    lines.append(
        "- Full hypothesis verdicts: `spec_study_t3/results/T3_REPORT.md`."
    )
    lines.append("")
    return "\n".join(lines), csv_rows


def write_analysis(
    *,
    base_dir: Path,
    model: str = MODEL,
    t2_jsonl: Path = T2_HAIKU_JSONL,
) -> tuple[Path, Path]:
    """Write ANALYSIS.md/csv under ``<slug>/analysis/`` only.

    Never creates or modifies ``<slug>/min/trials.jsonl`` — that path is
    owned exclusively by the live runner.
    """
    slug = resolve_model(model).slug
    rich_rows = load_rich_from_t2(t2_jsonl)
    min_path = min_trials_jsonl(base_dir, model)
    min_rows = load_min_from_t3(min_path)
    md, csv_rows = render_analysis(
        rich_rows=rich_rows, min_rows=min_rows, model=model
    )
    out_dir = analysis_dir(base_dir, model)
    out_dir.mkdir(parents=True, exist_ok=True)
    # Refuse to write into the runner's trial directory.
    assert out_dir.resolve() != (base_dir / slug / "min").resolve()
    md_path = out_dir / "ANALYSIS.md"
    csv_path = out_dir / "ANALYSIS.csv"
    md_path.write_text(md + "\n", encoding="utf-8")
    fieldnames = [
        "spec_level",
        "source",
        "topology",
        "arm",
        "n",
        "manif",
        "prop",
        "catch_manifested",
        "outcome_counts",
        "self_corr",
        "harm_sum",
        "cost",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in csv_rows:
            w.writerow(row)
    return md_path, csv_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="spec_study_t3 analysis")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_BASE,
        help="Study base dir (writes <slug>/analysis/ANALYSIS.md + .csv)",
    )
    parser.add_argument("--model", default=MODEL)
    parser.add_argument(
        "--t2-jsonl",
        type=Path,
        default=T2_HAIKU_JSONL,
        help="Read-only T2 Haiku JSONL for rich rows",
    )
    args = parser.parse_args(argv)
    base = args.output_dir
    if not base.is_absolute():
        base = ROOT / base
    t2 = args.t2_jsonl
    if not t2.is_absolute():
        t2 = ROOT / t2
    md_path, csv_path = write_analysis(
        base_dir=base, model=args.model, t2_jsonl=t2
    )
    print(f"Wrote {md_path}")
    print(f"Wrote {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
