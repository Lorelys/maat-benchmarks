"""Rich (Benchmark 6 / T2) specialist prompts — documentation pointer.

Full rich prompt text is vendored for analysis fixtures at
``code/benchmarks/controlled_insurance_claims/agents.py`` (``SYSTEM_PROMPTS``).
SPEC-MIN ablation prompts are in ``min.py``; see ``STRIP_MAP.md``.
"""
from __future__ import annotations

# Intentional: do not duplicate the large rich prompt corpus here.
RICH_PROMPTS_LOCATION = (
    "code/benchmarks/controlled_insurance_claims/agents.py :: SYSTEM_PROMPTS"
)
