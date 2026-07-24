# Analysis code (standalone recompute)

Stdlib-only Python that regenerates `ANALYSIS.md` / `.csv` from banked
`trials.jsonl` files. **No Maat engine, no LLM calls, no network.**

```bash
cd kim-comparison
./code/verify.sh
# or:
PYTHONPATH=code python3 -m benchmarks.topology_study_t2.analyze \
  --model claude-haiku-4.5 --output-dir topology_study_t2/results
```

## Included

| Path | Role |
|---|---|
| `benchmarks/topology_study_t2/analyze.py` | T2 tables from JSONL |
| `benchmarks/topology_study_t2/defect_match.py` | P2 corrupt-€ math + profile names |
| `benchmarks/topology_study_t2/models.py` | Pinned model registry (IDs/slugs) |
| `benchmarks/spec_study_t3/analyze.py` | T3 rich∪min tables |
| `benchmarks/controlled_insurance_claims/{anchor_fixture,mock_sources,agents,failure_profiles}.py` | Seed fixtures for honest/corrupt € |

## Not included

- `conductor/`, gate/REQ implementations, live runners (`run.py`, `executor.py`, `llm.py`, `maat_plan.py`)
- Live re-execution requires the Maat engine (available under license). All
  **published numbers** in this experiment are reproducible from the JSONLs alone.
