"""Constants for spec_study_t3."""
from __future__ import annotations

STUDY_ID = "spec_study_t3"
PLAN_ID = "topology_study_t2_plan"  # Maat plan reused byte-identical from T2

SPEC_LEVELS = ("rich", "min")
TOPOLOGIES = ("pipe", "independent")  # centralized out of scope for T3
ARMS = ("off", "intervene")

# Fixed model for this study.
MODEL = "claude-haiku-4.5"

EXPECTED_MIN_TRIALS = 28  # 2 topo × 2 arms × (1 clean + 2 profiles × 3 seeds)
